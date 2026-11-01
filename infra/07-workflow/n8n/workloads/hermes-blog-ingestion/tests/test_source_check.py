"""Source page text and per-item quote, number and name checks."""

import sys
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
from publisher.source_check import check_item, page_text  # noqa: E402
from publisher.source_fetch import FetchResult  # noqa: E402

Q = "the quick brown fox jumps over"  # a realistic quote, 30 chars


def result(body, content_type="text/html; charset=utf-8"):
    if isinstance(body, str):
        body = body.encode()
    return FetchResult("https://example.com/a", 200, "0" * 64, "t", content_type, body)


def item(**over):
    base = {
        "item_id": "i1",
        "kind": "news",
        "title": "제목",
        "body": "본문",
        "source_url": "https://example.com/a",
        "source_quotes": [Q],
    }
    base.update(over)
    return base


def check(page, body="본문", title="제목", **over):
    return check_item(item(title=title, body=body, **over), f"{Q} {page}")


class PageTextTests(unittest.TestCase):
    def test_html_text_skips_script_style_and_decodes_entities(self):
        html = (
            "<html><head><style>.x{}</style><script>var a='SECRET';</script></head>"
            "<body><noscript>NOJS</noscript><p>Tom &amp; Jerry</p><p>next</p>"
            "<b>Op</b>enAI</body></html>"
        )
        self.assertEqual("Tom & Jerry next OpenAI", page_text(result(html)))

    def test_charset_from_header_and_meta(self):
        body = "<p>삼성전자 발표</p>".encode("euc-kr")
        for ct, doc in (
            ("text/html; charset=EUC-KR", body),
            ("text/html", b'<meta charset="euc-kr">' + body),
            (
                "text/html",
                b'<meta http-equiv="Content-Type" content="text/html; charset=euc-kr">'
                + body,
            ),
        ):
            self.assertIn("삼성전자 발표", page_text(result(doc, ct)), ct)

    def test_unknown_charset_falls_back_to_utf8(self):
        text = page_text(result("<p>한글</p>".encode(), "text/html; charset=nope-9"))
        self.assertEqual("한글", text)

    def test_hostile_charset_does_not_crash(self):
        for name in ("zlib", "rot13", "base64", "idna", "hex"):
            for ct, doc in (
                (f"text/html; charset={name}", "<p>한글</p>".encode()),
                ("text/html", f'<meta charset="{name}"><p>한글</p>'.encode()),
            ):
                self.assertIn("한글", page_text(result(doc, ct)), name)

    def test_text_plain_is_not_html_parsed(self):
        text = page_text(result("a <b> c &amp; d", "text/plain"))
        self.assertEqual("a <b> c &amp; d", text)

    def test_missing_or_other_content_type_is_parsed_as_html(self):
        html = "<script>$9 billion</script><img alt=Zeta><p>ok</p>"
        for ct in ("", "application/octet-stream", "application/xhtml+xml"):
            self.assertEqual("ok", page_text(result(html, ct)), ct)


class ItemCheckTests(unittest.TestCase):
    def test_quote_match_normalises_nfkc_whitespace_and_curly_quotes(self):
        text = page_text(result("<p>He said “it’s  fine”\n\nok</p>"))
        quotes = ['He said "it\'s fine" ok']
        self.assertEqual([], check_item(item(source_quotes=quotes), text))
        self.assertEqual(
            [],
            check_item(
                item(source_quotes=["Ｈe said it is fine today"]),
                "He said it is fine today",
            ),
        )

    def test_missing_or_altered_quote_fails(self):
        text = "The company grew strongly."
        for quotes in (
            ["The company shrank strongly."],
            ["The company grew strongly.", "absent from the page entirely"],
            ["the company grew strongly."],
        ):
            self.assertEqual(
                ["quote_not_found"], check_item(item(source_quotes=quotes), text)
            )

    def test_short_quote_fails(self):
        self.assertEqual(
            ["quote_not_found"], check_item(item(source_quotes=["a"]), "a b c")
        )
        short = "x" * 19
        self.assertEqual(
            ["quote_not_found"], check_item(item(source_quotes=[short]), short)
        )
        ok = "x" * 20
        self.assertEqual([], check_item(item(source_quotes=[ok]), ok))

    def test_numbers_match_by_value(self):
        page = "Revenue hit $3 billion, up 30 percent, announced Oct 31."
        self.assertEqual(
            [],
            check(
                page,
                body="매출 30억 달러, 30% 증가, 10월 31일 발표",
                title="매출 30억 달러",
            ),
        )

    def test_plain_number_matches_any_form(self):
        for page in ("30억", "3 billion", "$3bn", "$3m"[:0] + "3,000,000,000"):
            self.assertEqual([], check(page, body="3,000,000,000 달러"), page)

    def test_compound_korean_number(self):
        self.assertEqual([], check("3,200,000,000,000", body="3조 2천억 원"))
        self.assertEqual(["number_not_found"], check("3조", body="3조 2천억 원"))

    def test_number_absent_from_page_fails(self):
        self.assertEqual(["number_not_found"], check("grew 30%", body="25% 증가"))
        self.assertEqual(["number_not_found"], check("grew 25", body="25% 증가"))

    def test_unparseable_number_expression_fails(self):
        for body in ("수십억 달러", "several billion dollars", "a million users"):
            self.assertEqual(["number_not_found"], check("10 billion", body=body), body)

    def test_spaced_korean_unit_is_not_dropped(self):
        self.assertEqual(["number_not_found"], check("30", body="30 억 달러"))
        self.assertEqual([], check("30억", body="30 억 달러"))

    def test_unrecognised_latin_scale_fails(self):
        for body in ("5M users", "5K users", "5 mn users", "5 bil users"):
            self.assertEqual(["number_not_found"], check("5 users", body=body), body)
        self.assertEqual([], check("5 million", body="$5m raised"))

    def test_digits_inside_identifiers_do_not_count(self):
        for page in ("H100", "A320neo", "GPT-4", "COVID-19", "B2B"):
            num = "".join(c for c in page.split("-")[-1] if c.isdigit())
            self.assertEqual(
                ["number_not_found"], check(page, body=f"{num}대 판매"), page
            )
        self.assertEqual([], check("sold 100 units", body="100대 판매"))

    def test_scale_only_and_digit_free_claims_fail(self):
        for body in (
            "백만 명", "천만 원", "십억 달러", "삼십억 달러", "수천 명",
            "thirty percent growth", "billions of dollars", "millions of users",
            "퍼센트 증가", "growth in %",
        ):  # fmt: skip
            self.assertEqual(
                ["number_not_found"], check("100 1000000 30 percent", body=body), body
            )

    def test_korean_words_with_unit_syllables_are_not_flagged(self):
        self.assertEqual([], check("x", body="만약 성공하면 만나서 조사하고 기억한다"))

    def test_latin_proper_noun_must_appear(self):
        self.assertEqual(["name_not_found"], check("Anthropic", body="OpenAI가 발표"))
        self.assertEqual([], check("OpenAI", body="OpenAI가 발표"))
        self.assertEqual(["name_not_found"], check("openai", body="OpenAI가 발표"))

    def test_plain_capitalised_first_words_are_not_names(self):
        # Grammar capitalises a field or sentence start; that is no evidence of a name.
        for body in (
            "Centrally discover and govern agents",
            "Use new visibility fields",
            "Includes security fixes",
            "Nvidia beats estimates",
            "The company grew. However it rests",
        ):
            self.assertEqual([], check("x", body=body), body)
        self.assertEqual([], check("x", title="Fast mode deprecated"))

    def test_mixed_case_first_words_are_still_names(self):
        self.assertEqual(["name_not_found"], check("x", body="AlloyDB adds insights"))
        self.assertEqual([], check("AlloyDB", body="AlloyDB adds insights"))
        self.assertEqual(["name_not_found"], check("x", body="Shipped. OpenAI beats"))

    def test_names_after_the_first_word_are_still_checked(self):
        self.assertEqual(["name_not_found"], check("x", body="Then Apple sued"))
        self.assertEqual(["name_not_found"], check("beats", body="Nvidia beats Intel"))

    def test_required_fields(self):
        self.assertEqual(["field_missing"], check_item(item(source_url=""), Q))
        self.assertEqual(["field_missing"], check_item(item(title=None), Q))
        no_url = item()
        del no_url["source_url"]
        self.assertEqual(["field_missing"], check_item(no_url, Q))
        no_quotes = item()
        del no_quotes["source_quotes"]
        self.assertEqual(["quotes_missing"], check_item(no_quotes, Q))
        self.assertEqual(["quotes_missing"], check_item(item(source_quotes=[]), Q))

    def test_all_checks_run_in_fixed_order(self):
        it = item(title=None, body="OpenAI 25%", source_quotes=["nope"])
        self.assertEqual(
            ["field_missing", "quote_not_found", "number_not_found", "name_not_found"],
            check_item(it, "text"),
        )


if __name__ == "__main__":
    unittest.main()
