"""Synthetic, offline contract tests for the Hermes v1 candidate preflight."""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts/validation/check-hermes-candidate.py"
RUN_ID = "a" * 32
JOB = "6eabd835f969"
SOURCE = f"cron/output/{JOB}/2026-10-29_08-00-00.md"


def candidate():
    return {
        "schema_version": "1.0.0",
        "producer": "hermes",
        "job_id": JOB,
        "run_id": RUN_ID,
        "report_kind": "strategy-news",
        "generated_at": "2026-10-29T08:00:03+09:00",
        "source_ref": SOURCE,
        "source_sha256": hashlib.sha256(b"synthetic report\n").hexdigest(),
        "items": [
            {
                "title": "Example",
                "summary": "Unconfirmed source",
                "region_or_scope": "국내",
                "category": "Tech",
                "source_url": "https://example.org/item",
                "collection_evidence": "https://example.org/item",
                "verification_status": "source_cited_unverified",
            }
        ],
        "state": {
            "run_completed": True,
            "source_file_ready": True,
            "email_delivery": "unknown",
            "blog_data_ingested": "unknown",
        },
        "export_status": "ready_for_review",
        "privacy_classification": "unreviewed",
        "warnings": [],
    }


def run(tmp_path, document, *options):
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(CLI), str(path), *map(str, options)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=10,
        check=False,
    )


def test_valid_candidate_is_preflight_not_approval(tmp_path):
    result = run(tmp_path, candidate())
    assert result.returncode == 0, result.stderr
    assert "VALID" in result.stdout
    assert "not checked" in result.stdout
    assert "approved" not in result.stdout.lower()


def test_non_idea_root_is_not_claimed_as_checked(tmp_path):
    result = run(tmp_path, candidate(), "--item-root", tmp_path)
    assert result.returncode == 0
    assert "idea bytes not checked" in result.stdout


def test_devops_producer_uncertainty_and_type(tmp_path):
    doc = candidate()
    doc.update(
        job_id="25674fbc0bf3",
        report_kind="devops-brief",
        source_ref="cron/output/25674fbc0bf3/2026-10-29_08-00-00.md",
    )
    doc["items"][0].update(
        product="Example",
        version=None,
        release_date=None,
        impact_scope="Unknown",
        uncertainty=["version: unverified"],
    )
    assert run(tmp_path, doc).returncode == 0
    doc["items"][0]["uncertainty"] = [42]
    assert run(tmp_path, doc).returncode == 1


def test_invalid_identity_or_status_fails(tmp_path):
    for field, value in [
        ("job_id", "25674fbc0bf3"),
        ("report_kind", "infra-github-report"),
        ("run_id", "a" * 31),
        ("run_id", "g" * 32),
        ("source_sha256", "x" * 64),
        ("export_status", "approved"),
    ]:
        doc = candidate()
        doc[field] = value
        result = run(tmp_path, doc)
        assert result.returncode == 1, (field, result.stderr)
        assert "INVALID" in result.stderr


def test_unearned_state_claim_fails(tmp_path):
    for field, value in [
        ("blog_data_ingested", "complete"),
        ("email_delivery", "delivered"),
        ("source_file_ready", False),
    ]:
        doc = candidate()
        doc["state"][field] = value
        assert run(tmp_path, doc).returncode == 1, field


def test_unknown_write_or_approval_claim_fails(tmp_path):
    for extra in ["approved", "idempotent_write", "blog_data_written"]:
        doc = candidate()
        doc[extra] = True
        assert run(tmp_path, doc).returncode == 1, extra


def test_october_29_url_with_unverified_marker_stays_unverified(tmp_path):
    doc = candidate()
    doc["items"][0]["collection_evidence"] += " [출처 확인 불가]"
    doc["items"][0]["verification_status"] = "unverified"
    assert run(tmp_path, doc).returncode == 0
    doc["items"][0]["verification_status"] = "source_cited_unverified"
    assert run(tmp_path, doc).returncode == 1


def test_url_without_evidence_is_not_verified(tmp_path):
    doc = candidate()
    doc["items"][0]["source_url"] = None
    doc["items"][0]["verification_status"] = "source_cited_unverified"
    assert run(tmp_path, doc).returncode == 1
    doc["items"][0]["verification_status"] = "unverified"
    assert run(tmp_path, doc).returncode == 0


def test_optional_staged_cron_source_hash_matches_bytes(tmp_path):
    root = tmp_path / "staged"
    source = root / SOURCE
    source.parent.mkdir(parents=True)
    source.write_bytes(b"synthetic report\n")
    assert run(tmp_path, candidate(), "--source-root", root).returncode == 0
    source.write_bytes(b"different report\n")
    assert run(tmp_path, candidate(), "--source-root", root).returncode == 1
    source.unlink()
    assert run(tmp_path, candidate(), "--source-root", root).returncode == 1


def test_staged_source_ref_cannot_escape_or_follow_symlink(tmp_path):
    root = tmp_path / "staged"
    source = root / SOURCE
    source.parent.mkdir(parents=True)
    source.symlink_to(tmp_path / "elsewhere")
    assert run(tmp_path, candidate(), "--source-root", root).returncode == 1
    doc = candidate()
    doc["source_ref"] = "../outside.md"
    assert run(tmp_path, doc, "--source-root", root).returncode == 1


def test_staged_idea_item_missing_or_hash_mismatch(tmp_path):
    doc = candidate()
    doc["job_id"] = "8d0925bc571d"
    doc["report_kind"] = "solo-dev-ideas"
    doc["source_ref"] = f"cron/output/{doc['job_id']}/2026-10-29_08-00-00.md"
    item = doc["items"][0]
    item.update(
        {
            field: None
            for field in (
                "customer_segment",
                "problem",
                "differentiation",
                "pricing",
                "revenue_model",
                "mvp_duration",
                "competitors",
                "alternatives",
                "market_size_claim",
                "regulation",
                "expected_revenue",
                "profitability_claim",
            )
        }
    )
    item["uncertainty"] = []
    item["source_ref"] = "storage/research/solo-dev-ideas/2026-10-29/kr/item.md"
    item["source_sha256"] = hashlib.sha256(b"idea\n").hexdigest()
    root = tmp_path / "home"
    assert run(tmp_path, doc, "--item-root", root).returncode == 1
    source = root / item["source_ref"]
    source.parent.mkdir(parents=True)
    source.write_bytes(b"wrong\n")
    assert run(tmp_path, doc, "--item-root", root).returncode == 1
    source.write_bytes(b"idea\n")
    assert run(tmp_path, doc, "--item-root", root).returncode == 0


def test_idea_path_requires_date_region_and_single_filename(tmp_path):
    doc = candidate()
    doc.update(
        job_id="8d0925bc571d",
        report_kind="solo-dev-ideas",
        source_ref="cron/output/8d0925bc571d/2026-10-29_08-00-00.md",
    )
    doc["items"][0].update(
        {
            field: None
            for field in (
                "customer_segment",
                "problem",
                "differentiation",
                "pricing",
                "revenue_model",
                "mvp_duration",
                "competitors",
                "alternatives",
                "market_size_claim",
                "regulation",
                "expected_revenue",
                "profitability_claim",
            )
        }
    )
    doc["items"][0].update(
        uncertainty=[],
        source_ref="storage/research/solo-dev-ideas/2026-10-29/kr/item.md",
        source_sha256="a" * 64,
    )
    assert run(tmp_path, doc).returncode == 0
    for path in (
        "storage/research/solo-dev-ideas/not-a-date/kr/item.md",
        "storage/research/solo-dev-ideas/2026-02-30/kr/item.md",
        "storage/research/solo-dev-ideas/2026-10-29/kr/nested/item.md",
    ):
        doc["items"][0]["source_ref"] = path
        assert run(tmp_path, doc).returncode == 1
    doc["items"][0]["source_ref"] = (
        "storage/research/solo-dev-ideas/2026-10-29/kr/item.md"
    )
    doc["items"][0]["regulation"] = ["invalid"]
    assert run(tmp_path, doc).returncode == 1


def test_cron_filename_requires_real_date_and_time(tmp_path):
    for name in (
        "2026-02-30_08-00-00.md",
        "2026-10-29_25-00-00.md",
        "2026-10-29_08-60-00.md",
    ):
        doc = candidate()
        doc["source_ref"] = f"cron/output/{JOB}/{name}"
        assert run(tmp_path, doc).returncode == 1


def test_replaced_staged_directory_cannot_escape_root(tmp_path):
    spec = importlib.util.spec_from_file_location("hermes_validator", CLI)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    root = tmp_path / "root"
    parent = root / "dir"
    parent.mkdir(parents=True)
    (parent / "file.md").write_bytes(b"inside")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "file.md").write_bytes(b"outside")
    original_open = os.open
    swapped = False

    def swap_then_open(path, flags, *args, **kwargs):
        nonlocal swapped
        if not swapped:
            swapped = True
            parent.rename(root / "original-dir")
            parent.symlink_to(outside, target_is_directory=True)
        return original_open(path, flags, *args, **kwargs)

    with mock.patch.object(module.os, "open", side_effect=swap_then_open):
        with unittest.TestCase().assertRaises(module.InvalidCandidate):
            module.staged_digest(
                root,
                PurePosixPath("dir/file.md"),
                hashlib.sha256(b"outside").hexdigest(),
            )


def test_infra_is_always_blocked_even_with_valid_structure(tmp_path):
    doc = candidate()
    doc.update(
        job_id="3c3f81a925e0",
        report_kind="infra-github-report",
        source_ref="cron/output/3c3f81a925e0/2026-10-29_08-00-00.md",
        export_status="blocked_private_source",
        privacy_classification="internal_restricted",
        items=[],
    )
    result = run(tmp_path, doc)
    assert result.returncode == 2
    assert "BLOCKED" in result.stdout
    doc["items"] = candidate()["items"]
    assert run(tmp_path, doc).returncode == 1


def test_malformed_json_and_unexpected_item_field_fail(tmp_path):
    doc = candidate()
    doc["items"][0]["approval"] = "granted"
    assert run(tmp_path, doc).returncode == 1
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(CLI), str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1


class TestHermesCandidate(unittest.TestCase):
    """Expose the focused cases to the repository's stdlib unittest gate."""

    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.path = Path(self.scratch.name)

    def tearDown(self):
        self.scratch.cleanup()


for _name, _function in list(globals().items()):
    if _name.startswith("test_") and callable(_function):
        setattr(TestHermesCandidate, _name, lambda self, fn=_function: fn(self.path))
