"""Минимальные end-to-end проверки публичного skill-пакета."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


class SkillSmokeTests(unittest.TestCase):
    def run_command(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [PYTHON, *args], cwd=ROOT, text=True, encoding="utf-8",
            capture_output=True, check=False, env=env,
        )

    def test_skill_frontmatter_and_references(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---"))
        self.assertIn("name: BeandsAnalystik", skill)
        for path in (
            "references/workflows/router.md",
            "references/workflows/interview.md",
            "references/agents/product-owner.md",
            "references/skills/openapi-spec.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_installer_verify_and_dry_run(self) -> None:
        verified = self.run_command("scripts/install.py", "--verify")
        self.assertEqual(verified.returncode, 0, verified.stderr)
        with tempfile.TemporaryDirectory() as temp_dir:
            installed = self.run_command(
                "scripts/install.py", "--target", "both", "--workspace", temp_dir, "--dry-run"
            )
        self.assertEqual(installed.returncode, 0, installed.stderr)

    def test_installer_real_workspace_install_for_both_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            installed = self.run_command(
                "scripts/install.py", "--target", "both", "--workspace", temp_dir
            )
            self.assertEqual(installed.returncode, 0, installed.stderr)
            self.assertTrue((Path(temp_dir) / ".hermes" / "skills" / "BeandsAnalystik" / "SKILL.md").is_file())
            self.assertTrue((Path(temp_dir) / ".openclaw" / "skills" / "BeandsAnalystik" / "SKILL.md").is_file())

    def test_export_pdf_and_docx_with_cyrillic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exported = self.run_command(
                "scripts/export_report.py", "examples/sample-report.md", "--format", "both",
                "--output-dir", temp_dir,
            )
            self.assertEqual(exported.returncode, 0, exported.stderr)
            self.assertTrue((Path(temp_dir) / "sample-report.pdf").is_file())
            self.assertTrue((Path(temp_dir) / "sample-report.docx").is_file())

    def test_export_missing_input_fails_cleanly(self) -> None:
        result = self.run_command("scripts/export_report.py", "reports/does-not-exist.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR:", result.stderr)


if __name__ == "__main__":
    unittest.main()
