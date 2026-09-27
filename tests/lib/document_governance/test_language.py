from __future__ import annotations

import unittest

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
        table = (
            "| ID | Path |\n| --- | --- |\n"
            + "".join(f"| GDE-{n:04d} | `guides/{n:04d}-x.md` |\n" for n in range(40))
        )
        self.assertIsNone(language_mismatch(KOREAN + table, "ko"))


if __name__ == "__main__":
    unittest.main()
