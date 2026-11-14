"""Current SemVer/changelog/publication guarantees, with no remote mutations."""

from __future__ import annotations

import hashlib
import inspect
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lib.document_governance import semver
from scripts.operations import release

CHANGELOG = """# Changelog

## [Unreleased]

## [1.2.3-rc.1+build.7] - 2026-10-07

### Fixed

- Preserve the main release target.

## [1.2.2] - 2026-10-06

### Added

- Previous changes.
"""
SHA = "a" * 40
REPOSITORY = "owner/repository"


class FakeCommands:
    def __init__(
        self,
        *,
        duplicate=False,
        tag=False,
        upload_error=False,
        assets=True,
        wrong_digest=False,
        publication_fault=None,
        immutable=False,
    ):
        self.calls = []
        self.duplicate = duplicate
        self.tag = tag
        self.upload_error = upload_error
        self.assets = assets
        self.wrong_digest = wrong_digest
        self.publication_fault = publication_fault
        self.immutable = immutable
        self.published = False
        self.uploaded = []

    def __call__(self, argv):
        self.calls.append(tuple(argv))
        if argv[:2] == ["git", "rev-parse"]:
            return SHA
        if argv[:2] == ["git", "show"]:
            return CHANGELOG
        if argv[:3] == ["git", "merge-base", "--is-ancestor"]:
            return ""
        if argv[:3] == ["gh", "api", f"repos/{REPOSITORY}/git/ref/heads/main"]:
            return json.dumps({"object": {"sha": SHA, "type": "commit"}})
        if argv[:3] == ["gh", "api", f"repos/{REPOSITORY}/releases"]:
            rows = (
                [{"tag_name": "v1.2.3-rc.1+build.7", "draft": False}]
                if self.duplicate
                else []
            )
            return json.dumps([rows])
        if argv[:3] == ["git", "ls-remote", "--tags"]:
            return f"{SHA}\trefs/tags/v1.2.3-rc.1+build.7" if self.tag else ""
        if argv[:3] == ["gh", "api", f"repos/{REPOSITORY}/git/refs"]:
            return json.dumps({"object": {"sha": SHA, "type": "commit"}})
        if argv[:3] == [
            "gh",
            "api",
            f"repos/{REPOSITORY}/git/ref/tags/v1.2.3-rc.1+build.7",
        ]:
            if self.published and self.publication_fault == "tag":
                return json.dumps({"object": {"sha": "b" * 40, "type": "commit"}})
            return json.dumps({"object": {"sha": SHA, "type": "commit"}})
        if argv[:3] == ["gh", "release", "upload"]:
            if self.upload_error:
                raise release.ReleaseError("upload failed")
            self.uploaded = [
                {
                    "name": Path(p).name,
                    "size": Path(p).stat().st_size,
                    "state": "uploaded",
                    "digest": "sha256:"
                    + (
                        "0" * 64
                        if self.wrong_digest
                        else hashlib.sha256(Path(p).read_bytes()).hexdigest()
                    ),
                }
                for p in argv[4:-2]
            ]
        if argv[:3] == [
            "gh",
            "api",
            f"repos/{REPOSITORY}/releases/tags/v1.2.3-rc.1+build.7",
        ]:
            assets = [dict(asset) for asset in self.uploaded] if self.assets else []
            if self.published and self.publication_fault == "digest":
                assets[0]["digest"] = "sha256:" + "0" * 64
            return json.dumps(
                {
                    "draft": not self.published or self.publication_fault == "draft",
                    "tag_name": "v1.2.3-rc.1+build.7",
                    "assets": assets,
                    "immutable": None
                    if self.published and self.publication_fault == "immutable"
                    else self.immutable,
                }
            )
        if argv[:3] == ["gh", "release", "edit"]:
            self.published = True
            if self.publication_fault == "publish-command":
                raise release.ReleaseError("publication response lost")
        return ""


class ReleaseTests(unittest.TestCase):
    def test_semver_accepts_stable_prerelease_and_build(self):
        for version in (
            "0.0.1",
            "12.30.4",
            "1.2.3-rc.1",
            "1.2.3+001",
            "1.2.3-alpha-beta+build.7",
            "1.0.0-rc.1",
            "1.2.3+build.007",
            "1.2.3-rc.1+sha.abc",
            "1.0.0-0",
        ):
            with self.subTest(version=version):
                self.assertEqual("v" + version, release.release_tag(version))

    def test_semver_rejects_prefixes_leading_zeroes_and_shell_input(self):
        for version in (
            "v1.2.3",
            "1.2",
            "01.2.3",
            "1.2.03",
            "1.2.3-01",
            "1.2.3-",
            "1.2.3+",
            "1.2.3\n",
            "1.2.3;echo x",
            "",
            "-1.2.3",
            "1.02.3",
            "1.2.3.4",
            "1.2.3-rc.01",
            "1.2.3-rc..1",
            "1.2.3+build..1",
        ):
            with self.subTest(version=version), self.assertRaises(release.ReleaseError):
                release.release_tag(version)

    def test_release_reuses_the_one_semver_implementation(self):
        # Precedence, malformed-value and version-change cases live with the
        # shared module in tests/lib/document_governance/test_semver.py.
        self.assertIs(semver.SEMVER, release.SEMVER)
        self.assertIs(semver.compare_semver, release.compare_semver)
        self.assertFalse(hasattr(release, "parse_semver"))
        self.assertIs(semver.check_version_change, release.check_version_change)

    def test_equal_precedence_release_cannot_reissue_a_published_version(self):
        commands = FakeCommands()

        def tampered(argv):
            if argv[:3] == ["gh", "api", f"repos/{REPOSITORY}/releases"]:
                return json.dumps([[{"tag_name": "v1.2.3-rc.1+build.1"}]])
            return commands(argv)

        with self.assertRaisesRegex(release.ReleaseError, "same precedence"):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=tampered)
        self.assertFalse(any("POST" in call for call in commands.calls))

    def test_equal_precedence_remote_tag_blocks_a_new_version(self):
        commands = FakeCommands()

        def tagged(argv):
            if argv[:3] == ["git", "ls-remote", "--tags"]:
                return f"{SHA}\trefs/tags/v1.2.3-rc.1+build.1\n{SHA}\trefs/tags/nightly"
            return commands(argv)

        with self.assertRaisesRegex(release.ReleaseError, "same precedence"):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=tagged)
        self.assertFalse(any("POST" in call for call in commands.calls))

    def _publish_against(self, *, releases=(), tags=(), **options):
        commands = FakeCommands()

        def existing(argv):
            if argv[:3] == ["gh", "api", f"repos/{REPOSITORY}/releases"]:
                return json.dumps([[{"tag_name": name} for name in releases]])
            if argv[:3] == ["git", "ls-remote", "--tags"]:
                return "\n".join(f"{SHA}\trefs/tags/{name}" for name in tags)
            return commands(argv)

        try:
            return release.publish(
                "1.2.3-rc.1+build.7", SHA, REPOSITORY, run=existing, **options
            ), commands
        except release.ReleaseError as error:
            return error, commands

    def test_version_below_highest_published_is_always_refused(self):
        for source in ("releases", "tags"):
            with self.subTest(source=source, case="downgrade"):
                result, commands = self._publish_against(**{source: ["v2.0.0"]})
                self.assertIsInstance(result, release.ReleaseError)
                self.assertIn("lower", str(result))
                self.assertNotIn("backport", str(result))
                self.assertFalse(any("POST" in call for call in commands.calls))
            with self.subTest(source=source, case="prerelease of a published release"):
                result, commands = self._publish_against(
                    **{source: ["v1.2.3-rc.2", "v1.2.3"]}
                )
                self.assertIn("lower", str(result))
                self.assertFalse(any("POST" in call for call in commands.calls))
            with self.subTest(source=source, case="higher"):
                result, _ = self._publish_against(**{source: ["v1.2.2", "1.0.0"]})
                self.assertEqual("v1.2.3-rc.1+build.7", result["tag"])
            with self.subTest(source=source, case="unchanged"):
                result, commands = self._publish_against(
                    **{source: ["v1.2.3-rc.1+build.1"]}
                )
                self.assertIn("same precedence", str(result))
                self.assertFalse(any("POST" in call for call in commands.calls))

    def test_old_and_new_published_version_against_old_and_new_release(self):
        """Old and new producer values, each as the published and the new release."""

        old, new = "1.2.0", "1.3.0-rc.1+build.7"
        expected = {
            (old, old): "already has a release",
            (old, new): None,
            (new, old): "lower",
            (new, new): "already has a release",
        }
        for (published, version), refusal in expected.items():

            def existing(argv, published=published):
                if argv[:3] == ["gh", "api", f"repos/{REPOSITORY}/releases"]:
                    return json.dumps([[{"tag_name": f"v{published}"}]])
                return ""  # no remote tags

            with self.subTest(published=published, version=version):
                if refusal is None:
                    release._new_version(existing, REPOSITORY, f"v{version}")
                else:
                    with self.assertRaisesRegex(release.ReleaseError, refusal):
                        release._new_version(existing, REPOSITORY, f"v{version}")

    def test_unprefixed_highest_tag_blocks_a_lower_version(self):
        for source in ("releases", "tags"):
            with self.subTest(source=source):
                result, commands = self._publish_against(**{source: ["3.0.0"]})
                self.assertIsInstance(result, release.ReleaseError)
                self.assertIn("lower", str(result))
                self.assertFalse(any("POST" in call for call in commands.calls))

    def test_tampered_release_with_another_tag_is_refused_after_the_draft(self):
        commands = FakeCommands()

        def tampered(argv):
            body = commands(argv)
            if argv[:3] == [
                "gh",
                "api",
                f"repos/{REPOSITORY}/releases/tags/v1.2.3-rc.1+build.7",
            ]:
                return json.dumps({**json.loads(body), "tag_name": "v9.9.9"})
            return body

        with self.assertRaisesRegex(release.ReleaseError, "tag differs"):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=tampered)
        self.assertFalse(commands.published)

    def test_cli_has_no_backport_option(self):
        with patch("sys.argv", ["release.py", "publish", "--help"]):
            with self.assertRaises(SystemExit), patch("sys.stdout") as stdout:
                release.main()
        self.assertNotIn(
            "backport", "".join(c.args[0] for c in stdout.write.mock_calls)
        )
        with patch("sys.argv", ["release.py", "publish", "--allow-backport"]):
            with self.assertRaises(SystemExit), patch("sys.stderr"):
                release.main()
        self.assertNotIn(
            "allow_backport", inspect.signature(release.publish).parameters
        )

    def test_changelog_entries_of_equal_precedence_are_duplicates(self):
        text = CHANGELOG.replace(
            "## [1.2.2] - 2026-10-06", "## [1.2.3-rc.1+build.8] - 2026-10-06"
        )
        with self.assertRaisesRegex(release.ReleaseError, "duplicate"):
            release.validate_changelog(text)

    def test_unrelated_existing_tags_do_not_block_a_new_version(self):
        commands = FakeCommands()

        def mixed(argv):
            if argv[:3] == ["gh", "api", f"repos/{REPOSITORY}/releases"]:
                rows = [{"tag_name": "v1.2.2"}, {"tag_name": "nightly"}]
                return json.dumps([rows])
            return commands(argv)

        receipt = release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=mixed)
        self.assertEqual("v1.2.3-rc.1+build.7", receipt["tag"])

    def test_exact_dated_heading_supplies_only_requested_notes(self):
        notes = release.release_notes(CHANGELOG, "1.2.3-rc.1+build.7")
        self.assertIn("## [1.2.3-rc.1+build.7] - 2026-10-07", notes)
        self.assertNotIn("Previous changes", notes)
        self.assertNotIn("Unreleased", notes)

    def test_substring_or_invalid_date_or_duplicate_or_empty_heading_refused(self):
        for text in (
            CHANGELOG.replace("[1.2.3-rc.1+build.7]", "[11.2.3-rc.1+build.7]"),
            CHANGELOG.replace("2026-10-07", "2026-02-30"),
            CHANGELOG
            + "\n## [1.2.3-rc.1+build.7] - 2026-10-07\n\n### Fixed\n\n- Duplicate.\n",
            CHANGELOG.replace("- Preserve the main release target.", ""),
        ):
            with self.subTest(text=text), self.assertRaises(release.ReleaseError):
                release.release_notes(text, "1.2.3-rc.1+build.7")

    def test_unreleased_only_is_valid_and_unrecognized_categories_refused(self):
        release.validate_changelog("# Changelog\n\n## [Unreleased]\n")
        with self.assertRaises(release.ReleaseError):
            release.validate_changelog(
                CHANGELOG.replace("### Fixed", "### Miscellaneous")
            )

    def test_duplicate_published_version_refused_before_mutation(self):
        commands = FakeCommands(duplicate=True)
        with self.assertRaises(release.ReleaseError):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=commands)
        self.assertFalse(
            any(
                "POST" in call or call[1:3] == ("release", "create")
                for call in commands.calls
            )
        )

    def test_existing_tag_refused_without_force_or_draft_overwrite(self):
        commands = FakeCommands(tag=True)
        with self.assertRaises(release.ReleaseError):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=commands)
        self.assertFalse(any("POST" in call for call in commands.calls))

    def test_legacy_bare_semver_tag_or_release_cannot_be_reissued_with_v_prefix(self):
        for legacy_kind in ("tag", "release"):
            commands = FakeCommands()

            def legacy(argv, legacy_kind=legacy_kind, commands=commands):
                if legacy_kind == "release" and argv[:3] == [
                    "gh",
                    "api",
                    f"repos/{REPOSITORY}/releases",
                ]:
                    return json.dumps(
                        [[{"tag_name": "1.2.3-rc.1+build.7", "draft": False}]]
                    )
                if legacy_kind == "tag" and argv[:3] == ["git", "ls-remote", "--tags"]:
                    if "refs/tags/1.2.3-rc.1+build.7" in argv or "refs/tags/*" in argv:
                        return f"{SHA}\trefs/tags/1.2.3-rc.1+build.7"
                    return ""
                return commands(argv)

            with (
                self.subTest(kind=legacy_kind),
                self.assertRaises(release.ReleaseError),
            ):
                release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=legacy)

    def test_main_ancestry_and_exact_head_required_before_mutation(self):
        commands = FakeCommands()

        def unrelated(argv):
            if argv[:3] == ["git", "merge-base", "--is-ancestor"]:
                raise release.ReleaseError("not on main")
            return commands(argv)

        with self.assertRaises(release.ReleaseError):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=unrelated)
        self.assertFalse(any("POST" in call for call in commands.calls))
        with self.assertRaises(release.ReleaseError):
            release.publish("1.2.3-rc.1+build.7", "b" * 40, REPOSITORY, run=commands)

    def test_tag_draft_complete_assets_then_publication(self):
        commands = FakeCommands()
        release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=commands)
        calls = commands.calls
        create = next(
            i for i, call in enumerate(calls) if call[1:3] == ("release", "create")
        )
        upload = next(
            i for i, call in enumerate(calls) if call[1:3] == ("release", "upload")
        )
        view = next(
            i
            for i, call in enumerate(calls)
            if call[:3]
            == ("gh", "api", f"repos/{REPOSITORY}/releases/tags/v1.2.3-rc.1+build.7")
        )
        edit = next(
            i for i, call in enumerate(calls) if call[1:3] == ("release", "edit")
        )
        self.assertLess(create, upload)
        self.assertLess(upload, view)
        self.assertLess(view, edit)
        self.assertIn("--draft", calls[create])
        self.assertIn("--verify-tag", calls[create])
        self.assertIn("--prerelease", calls[create])
        self.assertEqual(
            {"CHANGELOG.md", "SOURCE_REVISION.txt", "SHA256SUMS"},
            {asset["name"] for asset in commands.uploaded},
        )
        self.assertIn("--draft=false", calls[edit])
        self.assertFalse(
            any("--force" in call or "--clobber" in call for call in calls)
        )

    def test_upload_failure_or_missing_asset_never_publishes(self):
        for commands in (FakeCommands(upload_error=True), FakeCommands(assets=False)):
            with (
                self.subTest(commands=commands),
                self.assertRaises(release.ReleaseError),
            ):
                release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=commands)
            self.assertFalse(
                any(call[1:3] == ("release", "edit") for call in commands.calls)
            )

    def test_same_size_asset_with_wrong_bytes_digest_never_publishes(self):
        commands = FakeCommands(wrong_digest=True)
        with self.assertRaises(release.ReleaseError):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=commands)
        self.assertFalse(
            any(call[1:3] == ("release", "edit") for call in commands.calls)
        )

    def test_absent_malformed_digest_and_incomplete_upload_never_publish(self):
        for fault in ("absent", "malformed", "wrong-algorithm", "uploading"):
            commands = FakeCommands()

            def incomplete(argv, fault=fault, commands=commands):
                if argv[:3] == [
                    "gh",
                    "api",
                    f"repos/{REPOSITORY}/releases/tags/v1.2.3-rc.1+build.7",
                ]:
                    assets = [dict(asset) for asset in commands.uploaded]
                    if fault == "absent":
                        assets[0].pop("digest")
                    elif fault == "malformed":
                        assets[0]["digest"] = "sha256:not-a-digest"
                    elif fault == "wrong-algorithm":
                        assets[0]["digest"] = "md5:" + "0" * 32
                    else:
                        assets[0]["state"] = "uploading"
                    return json.dumps(
                        {
                            "draft": True,
                            "tag_name": "v1.2.3-rc.1+build.7",
                            "assets": assets,
                        }
                    )
                return commands(argv)

            with self.subTest(fault=fault), self.assertRaises(release.ReleaseError):
                release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=incomplete)
            self.assertFalse(
                any(call[1:3] == ("release", "edit") for call in commands.calls)
            )

    def test_publication_readback_requires_published_target_and_verified_bytes(self):
        for fault in ("draft", "tag", "digest", "immutable", "publish-command"):
            commands = FakeCommands(publication_fault=fault)
            with (
                self.subTest(fault=fault),
                self.assertRaisesRegex(release.ReleaseError, "manual recovery"),
            ):
                release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=commands)
            self.assertTrue(commands.published)

    def test_observed_immutable_state_is_reported_without_enabling_settings(self):
        for immutable in (False, True):
            commands = FakeCommands(immutable=immutable)
            result = release.publish(
                "1.2.3-rc.1+build.7", SHA, REPOSITORY, run=commands
            )
            self.assertEqual(
                {
                    "tag": "v1.2.3-rc.1+build.7",
                    "commit": SHA,
                    "published": True,
                    "immutable": immutable,
                },
                result,
            )
            self.assertFalse(
                any(
                    "rulesets" in argument or "immutable" in argument
                    for call in commands.calls
                    for argument in call
                )
            )

    def test_changed_tag_before_publish_never_publishes(self):
        commands = FakeCommands()

        def changed(argv):
            if argv[:3] == [
                "gh",
                "api",
                f"repos/{REPOSITORY}/git/ref/tags/v1.2.3-rc.1+build.7",
            ]:
                return json.dumps({"object": {"sha": "b" * 40}})
            return commands(argv)

        with self.assertRaises(release.ReleaseError):
            release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=changed)
        self.assertFalse(
            any(call[1:3] == ("release", "edit") for call in commands.calls)
        )

    def test_deleted_release_ref_is_not_candidate_acceptance(self):
        """QA-13: a vanished main or tag ref never counts; nothing publishes."""
        for deleted in (
            f"repos/{REPOSITORY}/git/ref/heads/main",
            f"repos/{REPOSITORY}/git/ref/tags/v1.2.3-rc.1+build.7",
        ):
            commands = FakeCommands()

            def gone(argv, deleted=deleted, commands=commands):
                if argv[:3] == ["gh", "api", deleted]:
                    commands.calls.append(tuple(argv))
                    raise release.ReleaseError("release command failed")
                return commands(argv)

            with self.subTest(deleted=deleted):
                with self.assertRaises(release.ReleaseError):
                    release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=gone)
                self.assertFalse(
                    any(call[1:3] == ("release", "edit") for call in commands.calls)
                )

    def test_annotated_tag_and_malformed_asset_metadata_refused(self):
        for invalid_kind in (
            "annotated-tag",
            "asset-name",
            "asset-size",
            "published-draft",
        ):
            commands = FakeCommands()

            def invalid(argv, invalid_kind=invalid_kind, commands=commands):
                if invalid_kind == "annotated-tag" and argv[:3] == [
                    "gh",
                    "api",
                    f"repos/{REPOSITORY}/git/ref/tags/v1.2.3-rc.1+build.7",
                ]:
                    return json.dumps({"object": {"sha": SHA, "type": "tag"}})
                if argv[:3] == [
                    "gh",
                    "api",
                    f"repos/{REPOSITORY}/releases/tags/v1.2.3-rc.1+build.7",
                ]:
                    if invalid_kind == "asset-name":
                        return json.dumps(
                            {
                                "draft": True,
                                "tag_name": "v1.2.3-rc.1+build.7",
                                "assets": [{"name": [], "size": 1}],
                            }
                        )
                    if invalid_kind == "asset-size":
                        return json.dumps(
                            {
                                "draft": True,
                                "tag_name": "v1.2.3-rc.1+build.7",
                                "assets": [{"name": "CHANGELOG.md", "size": True}],
                            }
                        )
                    if invalid_kind == "published-draft":
                        return json.dumps(
                            {
                                "draft": False,
                                "tag_name": "v1.2.3-rc.1+build.7",
                                "assets": commands.uploaded,
                            }
                        )
                return commands(argv)

            with (
                self.subTest(kind=invalid_kind),
                self.assertRaises(release.ReleaseError),
            ):
                release.publish("1.2.3-rc.1+build.7", SHA, REPOSITORY, run=invalid)
            self.assertFalse(
                any(call[1:3] == ("release", "edit") for call in commands.calls)
            )

    def test_command_failure_has_no_raw_output_or_arguments(self):
        with patch("subprocess.run") as process:
            process.return_value.returncode = 1
            process.return_value.stderr = "sensitive detail"
            with self.assertRaisesRegex(
                release.ReleaseError, "release command failed"
            ) as error:
                release.run_command(["gh", "secret-argument"])
            self.assertNotIn("sensitive", str(error.exception))
            self.assertNotIn("secret-argument", str(error.exception))


if __name__ == "__main__":
    unittest.main()
