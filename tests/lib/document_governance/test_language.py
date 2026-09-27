from __future__ import annotations

import unittest
from typing import ClassVar

from scripts.lib.document_governance.language import (
    hangul_ratio,
    language_mismatch,
)

KOREAN = """---
title: "Example"
---

# Example Service

## Overview

이 문서는 `infra/04-data/postgresql-cluster/` 서비스의 운영 범위와 책임을
설명합니다. 실행 명령과 경로는 원래 형태를 유지하고, 설명과 안내 문장은
한국어로 작성합니다. 자세한 절차는 RUN-0031과 [정책](../policies/0031-x.md)을
참고합니다.

```bash
docker compose config --quiet
```
"""

ENGLISH = """# Example Service

## Overview

This document explains the operating scope and ownership of the service.
Commands and paths keep their original form, and the guidance prose is
written in English for every reader of this stage.
"""


class LanguageJudgeTests(unittest.TestCase):
    def test_korean_prose_with_english_structure_tokens_reads_as_korean(self) -> None:
        self.assertIsNone(language_mismatch(KOREAN, "ko"))

    def test_english_prose_fails_as_korean_and_passes_as_english(self) -> None:
        self.assertIsNotNone(language_mismatch(ENGLISH, "ko"))
        self.assertIsNone(language_mismatch(ENGLISH, "en"))

    def test_korean_prose_fails_as_english(self) -> None:
        self.assertIsNotNone(language_mismatch(KOREAN, "en"))

    def test_too_little_prose_is_not_judged(self) -> None:
        self.assertIsNone(hangul_ratio("# Title\n\nSee `a/b.md`.\n"))
        self.assertIsNone(language_mismatch("# Title\n\nShort.\n", "ko"))

    def test_identifier_only_table_is_ignored(self) -> None:
        table = "| ID | Path |\n| --- | --- |\n" + "".join(
            f"| GDE-{n:04d} | `guides/{n:04d}-x.md` |\n" for n in range(40)
        )
        self.assertIsNone(language_mismatch(KOREAN + table, "ko"))


class TemplateLanguageProjectionTests(unittest.TestCase):
    """SPEC-0184 rule 8: a filled template reads in its profile's language."""

    SAMPLES: ClassVar[dict[str, str]] = {
        "ko": "이 문단은 템플릿을 채운 예시이며, 설명 문장은 모두 한국어로 씁니다. ",
        "en": "This paragraph fills the template, and every sentence is English prose. ",
    }

    def test_filled_templates_pass_in_their_language_and_fail_in_the_other(
        self,
    ) -> None:
        import pathlib
        import re

        from scripts.lib.document_governance.registry import load_registry

        root = pathlib.Path(__file__).resolve().parents[3]
        registry = load_registry()
        checked = 0
        for role_id, role in registry.template_roles.items():
            languages = {
                registry.profiles[profile_id].get("language")
                for profile_id in role.get("profiles", ())
                if profile_id in registry.profiles
            }
            declared = languages.pop() if len(languages) == 1 else None
            source = role.get("source")
            if declared is None or not str(source).endswith(".md"):
                continue
            text = (root / str(source)).read_text(encoding="utf-8")
            other = "en" if declared == "ko" else "ko"
            for language, expect_pass in ((declared, True), (other, False)):
                filled = re.sub(r"\{\{[A-Z0-9_]+\}\}", self.SAMPLES[language] * 3, text)
                with self.subTest(role=role_id, language=language):
                    reason = language_mismatch(filled, declared)
                    self.assertEqual(expect_pass, reason is None, reason)
            checked += 1
        self.assertGreater(checked, 10)

    def test_every_language_template_tells_its_author_the_language(self) -> None:
        import pathlib

        from scripts.lib.document_governance.registry import load_registry

        root = pathlib.Path(__file__).resolve().parents[3]
        registry = load_registry()
        words = {
            "ko": "Write body prose in Korean",
            "en": "Write body prose in English",
        }
        for role_id, role in registry.template_roles.items():
            languages = {
                registry.profiles[profile_id].get("language")
                for profile_id in role.get("profiles", ())
                if profile_id in registry.profiles
            }
            declared = languages.pop() if len(languages) == 1 else None
            source = str(role.get("source"))
            if declared is None or not source.endswith(".md"):
                continue
            with self.subTest(role=role_id):
                self.assertIn(
                    words[declared], (root / source).read_text(encoding="utf-8")
                )


if __name__ == "__main__":
    unittest.main()
