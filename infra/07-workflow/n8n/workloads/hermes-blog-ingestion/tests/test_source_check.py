"""Source page text and per-item quote, number and name checks."""

import sys
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKLOAD))
from publisher.source_check import check_item, page_text  # noqa: E402
from publisher.source_fetch import FetchResult  # noqa: E402


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
        "source_quotes": ["quote"],
    }
    base.update(over)
    return base


class PageTextTests(unittest.TestCase):
    def test_html_text_skips_script_style_and_decodes_entities(self):
        html = (
            "<html><head><style>.x{}</style><script>var a='SECRET';</script></head>"
            "<body><noscript>NOJS</noscript><p>Tom &amp; Jerry</p><p>next</p>"
            "<b>Op</b>enAI</body></html>"
        )
        text = page_text(result(html))
        self.assertEqual("Tom & Jerry next OpenAI", text)

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

    def test_text_plain_is_not_html_parsed(self):
        text = page_text(result("a <b> c &amp; d", "text/plain"))
        self.assertEqual("a <b> c &amp; d", text)


class ItemCheckTests(unittest.TestCase):
    def test_quote_match_normalises_nfkc_whitespace_and_curly_quotes(self):
        text = page_text(result("<p>He said “it’s  fine”\n\nok</p>"))
        quotes = ['He said "it\'s fine" ok']
        self.assertEqual([], check_item(item(source_quotes=quotes), text))
        self.assertEqual([], check_item(item(source_quotes=["Ｈe said"]), "He said hi"))

    def test_missing_or_altered_quote_fails(self):
        text = "The company grew."
        self.assertEqual(
            ["quote_not_found"],
            check_item(item(source_quotes=["The company shrank."]), text),
        )
        self.assertEqual(
            ["quote_not_found"],
            check_item(item(source_quotes=["The company grew.", "absent"]), text),
        )
        self.assertEqual(
            ["quote_not_found"],
            check_item(item(source_quotes=["the company grew."]), text),
        )

    def test_numbers_match_by_value(self):
        page = "Revenue hit $3 billion, up 30 percent, announced Oct 31."
        it = item(
            title="매출 30억 달러",
            body="매출 30억 달러, 30% 증가, 10월 31일 발표",
            source_quotes=["Revenue"],
        )
        self.assertEqual([], check_item(it, page))

    def test_plain_number_matches_any_form(self):
        it = item(title="t", body="3,000,000,000 달러", source_quotes=["x"])
        self.assertEqual([], check_item(it, "x 30억 y"))
        self.assertEqual([], check_item(it, "x 3 billion y"))
        self.assertEqual([], check_item(it, "x $3bn y"))

    def test_compound_korean_number(self):
        it = item(title="t", body="3조 2천억 원", source_quotes=["x"])
        self.assertEqual([], check_item(it, "x 3,200,000,000,000 y"))
        self.assertEqual(["number_not_found"], check_item(it, "x 3조 y"))

    def test_number_absent_from_page_fails(self):
        it = item(title="t", body="25% 증가", source_quotes=["x"])
        self.assertEqual(["number_not_found"], check_item(it, "x grew 30% y"))
        self.assertEqual(["number_not_found"], check_item(it, "x grew 25 y"))

    def test_unparseable_number_expression_fails(self):
        for body in ("수십억 달러", "several billion dollars", "a million users"):
            it = item(title="t", body=body, source_quotes=["x"])
            self.assertEqual(["number_not_found"], check_item(it, "x 10 billion"), body)

    def test_latin_proper_noun_must_appear(self):
        it = item(title="t", body="OpenAI가 발표", source_quotes=["x"])
        self.assertEqual(["name_not_found"], check_item(it, "x Anthropic"))
        self.assertEqual([], check_item(it, "x OpenAI y"))
        self.assertEqual(["name_not_found"], check_item(it, "x openai y"))

    def test_sentence_initial_english_word_is_not_a_name(self):
        it = item(title="t", body="Today we ship. Then Apple sued", source_quotes=["x"])
        self.assertEqual(["name_not_found"], check_item(it, "x Today then"))
        it = item(title="t", body="Today we ship. Then it rests", source_quotes=["x"])
        self.assertEqual([], check_item(it, "x"))

    def test_required_fields(self):
        text = "quote"
        self.assertEqual(["field_missing"], check_item(item(source_url=""), text))
        self.assertEqual(["field_missing"], check_item(item(title=None), text))
        no_url = item()
        del no_url["source_url"]
        self.assertEqual(["field_missing"], check_item(no_url, text))
        no_quotes = item()
        del no_quotes["source_quotes"]
        self.assertEqual(["quotes_missing"], check_item(no_quotes, text))
        self.assertEqual(["quotes_missing"], check_item(item(source_quotes=[]), text))

    def test_all_checks_run_in_fixed_order(self):
        it = item(title=None, body="OpenAI 25%", source_quotes=["nope"])
        self.assertEqual(
            ["field_missing", "quote_not_found", "number_not_found", "name_not_found"],
            check_item(it, "text"),
        )


if __name__ == "__main__":
    unittest.main()
