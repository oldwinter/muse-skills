"""CLI contract tests for scripts/build_catalog.py.

Each test drives the script in a throwaway copy of the archive so the real
catalog/ directory is never touched. Sentinel bytes stand in for generated
output to prove a run did not write.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SENTINEL = b"STALE-SENTINEL\n"


class CatalogCliTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.work = Path(cls.tmp.name)
        shutil.copytree(REPO / "scripts", cls.work / "scripts")
        shutil.copytree(REPO / "skills", cls.work / "skills", symlinks=True)
        shutil.copytree(REPO / "config", cls.work / "config")
        shutil.copytree(REPO / "runtime", cls.work / "runtime")
        cls.catalog = cls.work / "catalog"
        cls.catalog.mkdir()
        cls.script = cls.work / "scripts" / "build_catalog.py"

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            capture_output=True,
            text=True,
        )

    def stamp_sentinels(self):
        self.catalog.mkdir(parents=True, exist_ok=True)
        (self.catalog / "skills.json").write_bytes(SENTINEL)
        (self.catalog / "INDEX.md").write_bytes(SENTINEL)

    def assert_sentinels_intact(self):
        self.assertEqual((self.catalog / "skills.json").read_bytes(), SENTINEL)
        self.assertEqual((self.catalog / "INDEX.md").read_bytes(), SENTINEL)

    def test_help_exits_zero_and_writes_nothing(self):
        for flag in ("--help", "-h"):
            with self.subTest(flag=flag):
                self.stamp_sentinels()
                result = self.run_cli(flag)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout)
                self.assertIn("--check", result.stdout)
                self.assert_sentinels_intact()

    def test_unknown_arguments_rejected_without_writes(self):
        for args in (("--chek",), ("--bogus",), ("check",), ("--check", "extra")):
            with self.subTest(args=args):
                self.stamp_sentinels()
                result = self.run_cli(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("usage:", result.stderr)
                self.assert_sentinels_intact()

    def test_check_reports_stale_without_writes(self):
        self.stamp_sentinels()
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("stale", result.stderr)
        self.assert_sentinels_intact()

    def test_check_reports_missing_outputs_as_stale_without_writes(self):
        for missing in (("skills.json",), ("INDEX.md",), ("skills.json", "INDEX.md")):
            with self.subTest(missing=missing):
                self.stamp_sentinels()
                for name in missing:
                    (self.catalog / name).unlink()
                result = self.run_cli("--check")
                self.assertEqual(result.returncode, 1)
                self.assertIn("stale", result.stderr)
                for name in missing:
                    self.assertFalse((self.catalog / name).exists())
        self.stamp_sentinels()

    def test_rebuild_then_check_is_clean(self):
        self.stamp_sentinels()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        check = self.run_cli("--check")
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertRegex(check.stdout, r"ok \d+ skills")

    def test_rebuild_creates_missing_catalog_directory(self):
        shutil.rmtree(self.catalog)
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.catalog / "skills.json").is_file())
        self.assertTrue((self.catalog / "INDEX.md").is_file())

    def test_rebuild_matches_committed_catalog_byte_for_byte(self):
        self.stamp_sentinels()
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ("skills.json", "INDEX.md"):
            with self.subTest(name=name):
                self.assertEqual(
                    (self.catalog / name).read_bytes(),
                    (REPO / "catalog" / name).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
