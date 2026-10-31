"""Deterministic page text and per-item checks against a fetched source.

An item that fails any check is held, so every doubtful case fails closed.
"""

import codecs
import re
import unicodedata
from decimal import Decimal
from html.parser import HTMLParser

_QUOTES = str.maketrans({c: "'" for c in "‘’‚′"} | {c: '"' for c in "“”„«»″"})
_SKIP = {"script", "style", "noscript", "template"}
_BLOCK = {
    "p", "div", "br", "li", "ul", "ol", "tr", "td", "th", "table", "section",
    "article", "header", "footer", "nav", "aside", "blockquote", "pre", "hr",
    "title", "head", "body", "form", "dd", "dt", "dl", "figure", "figcaption",
    "main", "h1", "h2", "h3", "h4", "h5", "h6",
}  # fmt: skip


def _norm(s):
    s = unicodedata.normalize("NFKC", s).translate(_QUOTES)
    return re.sub(r"\s+", " ", s).strip()


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP:
            self.skip += 1
        if tag in _BLOCK:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in _SKIP and self.skip:
            self.skip -= 1
        if tag in _BLOCK:
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def _charset(content_type, body):
    name = None
    if m := re.search(r"charset\s*=\s*[\"']?([\w.:\-]+)", content_type, re.I):
        name = m[1]
    elif "html" in content_type.lower() and (
        m := re.search(rb"<meta[^>]+charset\s*=\s*[\"']?([\w.:\-]+)", body[:4096], re.I)
    ):
        name = m[1].decode("ascii")
    try:
        return codecs.lookup(name).name if name else "utf-8"
    except LookupError:
        return "utf-8"


def page_text(result):
    ctype = result.content_type or ""
    text = result.body.decode(_charset(ctype, result.body), errors="replace")
    if "html" in ctype.lower():
        parser = _Text()
        parser.feed(text)
        parser.close()
        text = "".join(parser.parts)
    return _norm(text)


# --- numbers ---------------------------------------------------------------

_MONTHS = {}
for _i, _names in enumerate(
    ("January Jan", "February Feb", "March Mar", "April Apr", "May", "June Jun",
     "July Jul", "August Aug", "September Sep Sept", "October Oct",
     "November Nov", "December Dec"),
    1,
):  # fmt: skip
    for _n in _names.split():
        _MONTHS[_n] = _i
_MON = "|".join(sorted(_MONTHS, key=len, reverse=True))
_N = r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?"
_TOKEN = re.compile(
    rf"(?P<kd>(?P<kdm>\d{{1,2}})\s*월\s*(?P<kdd>\d{{1,2}})\s*일)"
    rf"|(?P<e1>\b(?P<e1m>{_MON})\.?\s+(?P<e1d>\d{{1,2}})(?:st|nd|rd|th)?\b)"
    rf"|(?P<e2>\b(?P<e2d>\d{{1,2}})(?:st|nd|rd|th)?\s+(?:of\s+)?(?P<e2m>{_MON})\b)"
    rf"|(?P<bad>(?<![가-힣])수\s?(?:십|백|천)?(?:만|억|조)"
    rf"|\b(?i:thousand|million|billion|trillion)\b)"
    rf"|(?P<num>{_N})",
    re.ASCII,
)
_PCT = re.compile(r"\s*(?:%|(?i:percent)\b|퍼센트)", re.ASCII)
_KUNIT = re.compile(r"(천|백)?(만|억|조)?")
_KCHAIN = re.compile(rf"\s*({_N})(천|백)?(만|억|조)?", re.ASCII)
_EUNIT = re.compile(r"\s*(?i:(thousand|million|billion|trillion|bn|m))\b", re.ASCII)
_SMALL = {"천": 10**3, "백": 10**2}
_BIG = {"만": 10**4, "억": 10**8, "조": 10**12}
_RANK = {"만": 1, "억": 2, "조": 3}
_ESCALE = {
    "thousand": 10**3, "million": 10**6, "billion": 10**9, "trillion": 10**12,
    "bn": 10**9, "m": 10**6,
}  # fmt: skip
BAD = ("bad",)


def _dec(s):
    return Decimal(s.replace(",", ""))


def _date(month, day):
    return ("date", month, day) if 1 <= month <= 12 and 1 <= day <= 31 else BAD


def _numbers(s):
    """Comparable tokens in s; BAD marks an expression we cannot value."""
    out, pos = [], 0
    while m := _TOKEN.search(s, pos):
        pos = m.end()
        if m["kd"]:
            out.append(_date(int(m["kdm"]), int(m["kdd"])))
        elif m["e1"]:
            out.append(_date(_MONTHS[m["e1m"]], int(m["e1d"])))
        elif m["e2"]:
            out.append(_date(_MONTHS[m["e2m"]], int(m["e2d"])))
        elif m["bad"]:
            out.append(BAD)
        else:
            value = _dec(m["num"])
            if p := _PCT.match(s, pos):
                out.append(("pct", value))
                pos = p.end()
            elif (k := _KUNIT.match(s, pos)) and (k[1] or k[2]):
                value *= _SMALL.get(k[1], 1) * _BIG.get(k[2], 1)
                pos, rank = k.end(), _RANK.get(k[2], 0)
                while rank and (c := _KCHAIN.match(s, pos)):
                    r = _RANK.get(c[3], 0)
                    if not (c[2] or c[3]) or r >= rank:
                        break
                    value += _dec(c[1]) * _SMALL.get(c[2], 1) * _BIG.get(c[3], 1)
                    pos, rank = c.end(), r
                out.append(("num", value))
            elif (e := _EUNIT.match(s, pos)) and (
                e[1].lower() != "m" or s[m.start() - 1 : m.start()] == "$"
            ):
                out.append(("num", value * _ESCALE[e[1].lower()]))
                pos = e.end()
            else:
                out.append(("num", value))
    return out


# --- names -----------------------------------------------------------------

_NAME = re.compile(r"\b[A-Z][A-Za-z0-9&.\-]{1,}\b", re.ASCII)
_SENT_END = re.compile(r"[A-Za-z0-9)\"'][.!?] $")


def _names(s):
    for m in _NAME.finditer(s):
        if m[0] in _MONTHS:
            continue
        before = s[: m.start()]
        if (not before or _SENT_END.search(before)) and re.match(
            r" [A-Za-z]", s[m.end() :]
        ):
            continue  # first word of an English sentence
        yield m[0]


# --- item ------------------------------------------------------------------

_REQUIRED = ("item_id", "kind", "title", "body", "source_url")


def _text(v):
    return v if isinstance(v, str) else ""


def check_item(item, text):
    """Failure codes in fixed order; an empty list means verified."""
    text = _norm(text)
    codes = []
    if any(not _text(item.get(k)).strip() for k in _REQUIRED):
        codes.append("field_missing")
    quotes = item.get("source_quotes")
    if not isinstance(quotes, list) or not quotes:
        codes.append("quotes_missing")
    elif len(quotes) > 3 or any(
        not isinstance(q, str)
        or not 0 < len(q) <= 500
        or not (n := _norm(q))
        or n not in text
        for q in quotes
    ):
        codes.append("quote_not_found")
    fields = [_norm(_text(item.get(k))) for k in ("title", "body")]
    have = set(_numbers(text))
    if any(t == BAD or t not in have for f in fields for t in _numbers(f)):
        codes.append("number_not_found")
    if any(
        not re.search(rf"(?<![A-Za-z0-9]){re.escape(n)}(?![A-Za-z0-9])", text)
        for f in fields
        for n in _names(f)
    ):
        codes.append("name_not_found")
    return codes
