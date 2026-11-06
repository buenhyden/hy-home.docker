"""The operator scripts stay site-neutral and feed the unit what it reads."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

WORKLOAD = Path(__file__).resolve().parents[1]
DEPLOY = WORKLOAD / "deploy"
SCRIPTS = ("install-attester.sh", "update-hermes-plugin.sh", "update-cron-prompts.sh")


class DeployScriptTests(unittest.TestCase):
    def test_scripts_parse(self):
        for name in SCRIPTS:
            result = subprocess.run(
                ["bash", "-n", str(DEPLOY / name)], capture_output=True, check=False
            )
            self.assertEqual(0, result.returncode, (name, result.stderr))

    def test_scripts_carry_no_site_values(self):
        for name in SCRIPTS:
            text = (DEPLOY / name).read_text()
            self.assertNotIn("/home/", text, name)
            self.assertIsNone(re.search(r"\b\d{1,3}(\.\d{1,3}){3}\b", text), name)
            self.assertNotIn("hy.home.arpa", text, name)

    def test_environment_file_holds_what_the_attester_reads(self):
        unit = (DEPLOY / "hermes-attester.service").read_text()
        install = (DEPLOY / "install-attester.sh").read_text()
        fetch = (WORKLOAD / "publisher/source_fetch.py").read_text()
        (printf,) = re.findall(r"printf '([^']*)'.*environment\.new", install, re.S)
        written = set(re.findall(r"([A-Z_]+)=", printf))
        read = set(re.findall(r"\$\{([A-Z_]+)\}", unit))
        read |= set(re.findall(r'os\.environ\.get\("([A-Z_]+)"', fetch))
        self.assertEqual(read, written)
        self.assertIn("EnvironmentFile=/etc/hermes-attester/environment", unit)
        self.assertIn("/etc/hermes-attester/environment.new", install)

    def test_failed_install_stops_the_timer(self):
        install = (DEPLOY / "install-attester.sh").read_text()
        failure = install.split("else", 1)[1]
        self.assertIn("systemctl disable --now hermes-attester.timer", failure)


class CronPromptTests(unittest.TestCase):
    """The tracked prompt asks for exactly what the plugin accepts."""

    def setUp(self):
        sys.path.insert(0, str(WORKLOAD / "hermes-plugin"))
        import tools  # type: ignore

        self.tools = tools
        self.prompt = (DEPLOY / "research-submission-prompt.txt").read_text()

    def test_prompt_names_the_fields_the_tool_sets_and_accepts(self):
        parameters = self.tools.SUBMIT_RESEARCH_REPORT_SCHEMA["parameters"]
        self.assertIn(
            "exactly payload, source_receipts and report_markdown", self.prompt
        )
        self.assertEqual(
            set(parameters["properties"]),
            {"payload", "source_receipts", "report_markdown"},
        )
        self.assertIn('payload has schema_version "1.0" and items', self.prompt)
        self.assertIn("exactly item_id and source_url", self.prompt)
        for trusted in (
            "identity",
            "timestamps",
            "source text",
            "source digest",
            "idempotency key",
        ):
            self.assertIn(trusted, self.prompt)
        item = re.search(r"Each item has exactly (.*?)\.", self.prompt)[1]
        self.assertEqual(
            self.tools._ITEM_FIELDS, set(re.findall(r"[a-z_]+", item)) - {"and"}
        )

    def sentences(self):
        return [x.strip() for x in re.split(r"(?<=[.;:])\s+", self.prompt)]

    def test_prompt_finalizes_the_report_before_one_submission_and_sending(self):
        self.assertTrue(self.prompt.startswith("DIRECT RESEARCH SUBMISSION"))
        self.assertEqual(self.prompt.count("DIRECT RESEARCH SUBMISSION"), 1)
        order = [
            self.prompt.index(step)
            for step in ("Step 1. Write the complete report", "Step 2.", "Step 3.")
        ]
        order.append(self.prompt.index("Step 4."))
        self.assertEqual(order, sorted(order))
        self.assertIn("call submit_research_report once", self.prompt)
        self.assertIn("Do not send the email or Telegram before step 3", self.prompt)
        for path in ("email_path", "telegram_path", "report_sha256"):
            self.assertIn(path, self.prompt)
        self.assertIn("never resend an email", self.prompt)
        self.assertIn(
            "record the email, Telegram and Gateway results separately", self.prompt
        )
        self.assertIn("mktemp -d", self.prompt)
        self.assertIn("report BLOCKED instead of shortening it", self.prompt)
        self.assertNotIn("not preserved", self.prompt)
        self.assertNotIn("does not keep the full report", self.prompt)

    def test_prompt_never_uses_the_shared_scratch_file_or_disables_the_verifier(self):
        for sentence in self.sentences():
            if "email_body.html" in sentence:
                self.assertTrue(sentence.startswith("Never write"), sentence)
            if re.search(r"\bdisabl", sentence, re.IGNORECASE):
                self.assertTrue(sentence.startswith("Never ask to disable"), sentence)
        self.assertNotIn(
            "/scratch/",
            self.prompt.replace("~/.hermes/cache/scratch/email_body.html", ""),
        )

    def test_prompt_carries_the_owner_item_rules(self):
        # SPEC-0265 criterion 9: H, D-03, G-02 and G-03 as producer prompt text.
        for rule in (
            "never item-1, D6 or G7",  # H: semantic stable ids
            "One item per article, event or change",
            "product and version, CVE or GHSA, or final URL",  # H/G-01: dedupe
            "an earlier day's report",
            "a real new version, event or official correction is an update",
            "Never delete or rewrite earlier reports, acknowledgements or item ids",
            "A name you coined",  # H: titles
            "never merge several release-note changes into one item",
            "stitch separate sentences",  # H: quotes
            "a relative time is never the source time",
            "Keep the page's publish date apart from the fetch date",  # H, D-04
            "list, portal, changelog index, release list",  # D-03, G-02
            "unless the specific version or paragraph is identified",
            "Do not add scope, field, country, industry or stack fields",  # G-03
            "claim no automatic classification",
        ):
            self.assertIn(rule, self.prompt)

    def test_script_reads_the_plugin_job_list(self):
        script = (DEPLOY / "update-cron-prompts.sh").read_text()
        (expr,) = re.findall(r"sed -n '([^']*)'", script)
        source = (WORKLOAD / "hermes-plugin/tools.py").read_text()
        out = subprocess.run(
            ["sed", "-n", expr],
            input=source,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(set(self.tools._ALLOWED_JOBS), set(out.stdout.split()))


class CronPromptScriptRunTests(unittest.TestCase):
    """Run update-cron-prompts.sh against a throwaway repo, HOME and hermes."""

    JOBS = ("6eabd835f969", "25674fbc0bf3", "8d0925bc571d")

    def run_script(self, prompts):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        repo, home, bin_dir = tmp / "repo", tmp / "home", tmp / "bin"
        wl = repo / "infra/07-workflow/n8n/workloads/hermes-blog-ingestion"
        for rel in (
            "deploy/update-cron-prompts.sh",
            "deploy/research-submission-prompt.txt",
            "hermes-plugin/tools.py",
        ):
            (wl / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(WORKLOAD / rel, wl / rel)

        def git(*a):
            return subprocess.run(
                ["git", "-C", str(repo), *a], check=True, capture_output=True
            )

        git("init", "-q", "-b", "main")
        git(
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "commit",
            "-qm",
            "x",
            "--allow-empty",
        )
        git("add", ".")
        git(
            "-c",
            "user.name=t",
            "-c",
            "user.email=t@example.invalid",
            "commit",
            "-qm",
            "y",
        )
        git("remote", "add", "origin", str(repo))
        (home / ".hermes/cron").mkdir(parents=True)
        jobs = home / ".hermes/cron/jobs.json"
        jobs.write_text(
            json.dumps({"jobs": [{"id": i, "prompt": p} for i, p in prompts.items()]})
        )
        bin_dir.mkdir()
        log = tmp / "edits.jsonl"
        (bin_dir / "hermes").write_text(
            "#!/usr/bin/env python3\nimport json, sys\n"
            f"open({str(log)!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"
        )
        (bin_dir / "hermes").chmod(0o755)
        env = {
            **os.environ,
            "HOME": str(home),
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
        }
        result = subprocess.run(
            ["bash", str(wl / "deploy/update-cron-prompts.sh")],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        edits = (
            [json.loads(x) for x in log.read_text().splitlines()]
            if log.exists()
            else []
        )
        return result, edits

    def test_paragraph_is_replaced_and_the_job_text_before_it_kept(self):
        prompts = {
            i: f"Job {i} work.\n\n\nDIRECT RESEARCH SUBMISSION old text"
            for i in self.JOBS
        }
        result, edits = self.run_script(prompts)
        self.assertEqual(0, result.returncode, result.stderr)
        block = (DEPLOY / "research-submission-prompt.txt").read_text().rstrip("\n")
        self.assertEqual(
            {i: f"Job {i} work.\n\n\n{block}" for i in self.JOBS},
            {
                e[2]: e[4]
                for e in edits
                if e[:2] == ["cron", "edit"] and e[3] == "--prompt"
            },
        )

    def test_rerun_with_the_current_block_edits_nothing(self):
        block = (DEPLOY / "research-submission-prompt.txt").read_text().rstrip("\n")
        prompts = {i: f"Job {i} work.\n\n{block}" for i in self.JOBS}
        result, edits = self.run_script(prompts)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], edits)
        self.assertEqual(3, result.stdout.count(" unchanged"))

    def test_a_repeated_marker_stops_naming_the_job_and_count(self):
        prompts = {i: "work.\n\nDIRECT RESEARCH SUBMISSION old" for i in self.JOBS}
        prompts[self.JOBS[1]] = (
            "work that mentions DIRECT RESEARCH SUBMISSION early.\n\n"
            "DIRECT RESEARCH SUBMISSION old"
        )
        result, edits = self.run_script(prompts)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual([], edits)
        self.assertIn(
            f"{self.JOBS[1]}: 2 DIRECT RESEARCH SUBMISSION markers, expected exactly 1",
            result.stderr,
        )

    def test_a_job_without_the_paragraph_stops_before_any_edit(self):
        prompts = {i: "work.\n\nDIRECT RESEARCH SUBMISSION old" for i in self.JOBS}
        prompts[self.JOBS[2]] = "work without the paragraph"
        result, edits = self.run_script(prompts)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual([], edits)
        self.assertIn("backup:", result.stdout)
        self.assertIn(
            f"{self.JOBS[2]}: 0 DIRECT RESEARCH SUBMISSION markers", result.stderr
        )


if __name__ == "__main__":
    unittest.main()
