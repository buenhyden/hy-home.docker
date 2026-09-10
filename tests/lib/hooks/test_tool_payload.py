from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts.lib.hooks.tool_payload import PayloadError, decode_payload, edit_targets


class NativeEditPayloadTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def test_claude_absolute_and_relative_paths_share_identity(self) -> None:
        for path in ("file name.txt", str(self.root / "file name.txt")):
            with self.subTest(path=path):
                self.assertEqual(
                    (("file name.txt", "updated"),),
                    edit_targets(
                        self.root,
                        {
                            "tool_name": "Edit",
                            "tool_input": {"file_path": path, "new_string": "updated"},
                        },
                    ),
                )

    def test_decoded_multifile_patch_keeps_each_replacement_and_move(self) -> None:
        patch = (
            "*** Begin Patch\n*** Add File: first.txt\n+first\n"
            "*** Update File: old.txt\n*** Move to: new name.txt\n@@\n-old\n+new\n"
            "*** Delete File: deleted.txt\n*** End Patch"
        )
        data = decode_payload(
            json.dumps(
                {
                    "tool_name": "apply_patch",
                    "tool_input": {"command": patch},
                }
            )
        )
        self.assertEqual(
            (
                ("first.txt", "first"),
                ("old.txt", "new"),
                ("new name.txt", "new"),
                ("deleted.txt", ""),
            ),
            edit_targets(self.root, data),
        )

    def test_unsafe_paths_fail_before_consumers_can_write(self) -> None:
        outside = self.root.parent / "outside.txt"
        (self.root / "link").symlink_to(self.root.parent, target_is_directory=True)
        (self.root / "file.txt").write_text("unchanged")
        os.link(self.root / "file.txt", self.root / "hardlink.txt")
        (self.root / "directory").mkdir()
        for path in (
            str(outside),
            "../escape",
            "./file.txt",
            "a/../b",
            "a//b",
            "bad\\path",
            "bad\npath",
            "link/outside",
            "hardlink.txt",
            "directory",
            str(self.root / "link/outside"),
        ):
            with self.subTest(path=path), self.assertRaises(PayloadError):
                edit_targets(
                    self.root,
                    {
                        "tool_name": "Write",
                        "tool_input": {"file_path": path},
                    },
                )
        self.assertEqual("unchanged", (self.root / "file.txt").read_text())

    def test_matched_edit_tools_fail_closed_without_targets(self) -> None:
        for name in ("Write", "Edit", "MultiEdit", "apply_patch", "ApplyPatch"):
            with self.subTest(name=name), self.assertRaises(PayloadError):
                edit_targets(self.root, {"tool_name": name, "tool_input": {}})
        self.assertEqual((), edit_targets(self.root, {"tool_name": "Bash"}))

    def test_invalid_json_and_payload_bounds_fail_closed(self) -> None:
        for raw in ("{", "[]", "x" * (1024 * 1024 + 1)):
            with self.subTest(size=len(raw)), self.assertRaises(PayloadError):
                decode_payload(raw)
        for command in (
            "",
            "*** Begin Patch\n*** End Patch",
            "*** Begin Patch\n*** Add File: a\n+x\n*** Unknown: b\n*** End Patch",
        ):
            with self.subTest(command=command), self.assertRaises(PayloadError):
                edit_targets(
                    self.root,
                    {
                        "tool_name": "apply_patch",
                        "tool_input": {"command": command},
                    },
                )

    def test_nested_edits_keep_path_text_pairing(self) -> None:
        self.assertEqual(
            (("a", "one"), ("b", "two")),
            edit_targets(
                self.root,
                {
                    "tool_name": "MultiEdit",
                    "tool_input": {
                        "edits": [
                            {"file_path": "a", "new_string": "one"},
                            {"path": "b", "new_text": "two"},
                        ],
                    },
                },
            ),
        )

    def test_invalid_record_cannot_hide_behind_a_valid_edit(self) -> None:
        for invalid in (
            None,
            42,
            {},
            {"file_path": 42},
            {"file_path": "bad", "new_string": 42},
        ):
            with self.subTest(invalid=invalid), self.assertRaises(PayloadError):
                edit_targets(
                    self.root,
                    {
                        "tool_name": "MultiEdit",
                        "tool_input": {
                            "edits": [
                                {"file_path": "safe", "new_string": "ok"},
                                invalid,
                            ],
                        },
                    },
                )
        for value in ("", None, 42):
            with self.subTest(inherited=value), self.assertRaises(PayloadError):
                edit_targets(
                    self.root,
                    {
                        "tool_name": "MultiEdit",
                        "tool_input": {
                            "file_path": "parent",
                            "edits": [{"file_path": value, "new_string": "no"}],
                        },
                    },
                )
        self.assertEqual(
            (("parent", ""), ("parent", "yes")),
            edit_targets(
                self.root,
                {
                    "tool_name": "MultiEdit",
                    "tool_input": {
                        "file_path": "parent",
                        "edits": [{"new_string": "yes"}],
                    },
                },
            ),
        )

    def test_patch_uses_lf_records_and_preserves_unicode_filename(self) -> None:
        path = "compose\u2028*** Update File: ordinary.yml"
        self.assertEqual(
            ((path, "value"),),
            edit_targets(
                self.root,
                {
                    "tool_name": "apply_patch",
                    "tool_input": {
                        "command": f"*** Begin Patch\n*** Add File: {path}\n+value\n*** End Patch\n"
                    },
                },
            ),
        )

    def test_native_patch_envelope_allows_outer_whitespace(self) -> None:
        for before, after in (
            ("\n", "\n\n"),
            ("  ", " \n \n"),
            ("\t", "\t"),
            ("\v", "\f"),
            ("\u00a0", "\u00a0"),
        ):
            with self.subTest(before=before, after=after):
                self.assertEqual(
                    (("a", "new"),),
                    edit_targets(
                        self.root,
                        {
                            "tool_name": "apply_patch",
                            "tool_input": {
                                "command": before
                                + "*** Begin Patch\n*** Add File: a\n+new\n*** End Patch"
                                + after,
                            },
                        },
                    ),
                )

    def test_native_patch_envelope_rejects_non_native_controls(self) -> None:
        for control in ("\x1c", "\x1d", "\x1e", "\x1f"):
            with self.subTest(control=control), self.assertRaises(PayloadError):
                edit_targets(
                    self.root,
                    {
                        "tool_name": "apply_patch",
                        "tool_input": {
                            "command": control
                            + "*** Begin Patch\n*** Add File: a\n+new\n*** End Patch"
                            + control
                        },
                    },
                )

    def test_target_limit_is_checked_before_expansion(self) -> None:
        for count in (256, 257):
            payload = {
                "tool_name": "Write",
                "tool_input": {"files": [f"file-{i}" for i in range(count)]},
            }
            if count == 256:
                self.assertEqual(count, len(edit_targets(self.root, payload)))
            else:
                with self.assertRaises(PayloadError):
                    edit_targets(self.root, payload)
            patch = (
                "*** Begin Patch\n"
                + "".join(
                    f"*** Add File: file-{index}\n+value\n" for index in range(count)
                )
                + "*** End Patch"
            )
            payload = {"tool_name": "apply_patch", "tool_input": {"command": patch}}
            if count == 256:
                self.assertEqual(count, len(edit_targets(self.root, payload)))
            else:
                with self.assertRaises(PayloadError):
                    edit_targets(self.root, payload)
        with self.assertRaises(PayloadError):
            edit_targets(
                self.root,
                {
                    "tool_name": "apply_patch",
                    "tool_input": {
                        "command": "*** Begin Patch\n*** Update File: old\n"
                        + "*** Move to: new\n" * 400
                        + "+a\n+b\n*** End Patch",
                    },
                },
            )

    def test_patch_operation_grammar_rejects_empty_or_misplaced_records(self) -> None:
        for body in (
            "*** Update File: a\n*** Add File: b\n+x",
            "*** Delete File: a\n-old",
            "*** Update File: a\n@@\n-old\n+new\n*** Move to: b",
            "*** Update File: a\n*** Move to: b",
            "*** Update File: a\n@@",
            "*** Update File: a\n*** End of File",
            "*** Add File: a\n-old",
            "*** Update File: a\n@@foo\n-old\n+new",
            "*** Update File: a\n@@@\n-old\n+new",
            "*** Update File: a\n@@\n@@\n-old\n+new",
            "*** Update File: a\n-old\n+new\n@@",
            "*** Update File: a\n-old\n+new\n@@\n*** End of File",
            "*** Update File: a\n-old\n+new\n*** End of File\n*** End of File",
        ):
            with self.subTest(body=body), self.assertRaises(PayloadError):
                edit_targets(
                    self.root,
                    {
                        "tool_name": "apply_patch",
                        "tool_input": {
                            "command": f"*** Begin Patch\n{body}\n*** End Patch",
                        },
                    },
                )
        for body in (
            "-old\n+new",
            " old",
            "+new",
            "*** Move to: b\n-old\n+new",
            "@@\n-old\n+new\n\n end",
        ):
            with self.subTest(valid=body):
                self.assertTrue(
                    edit_targets(
                        self.root,
                        {
                            "tool_name": "apply_patch",
                            "tool_input": {
                                "command": f"*** Begin Patch\n*** Update File: a\n{body}\n*** End Patch",
                            },
                        },
                    )
                )
