import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_catalog


class CatalogAliasTests(unittest.TestCase):
    manifest_aliases = {
        "facebook": "facebook-cli",
        "meta-threads": "threads",
    }
    no_manifest_aliases = {
        "podcast": "generate_podcast",
        "voice-calls": "voice-selector",
    }

    def setUp(self):
        scratch = Path(__file__).resolve().parents[1] / ".agent"
        scratch.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skills = self.root / "skills"
        for alias, target in {**self.manifest_aliases, **self.no_manifest_aliases}.items():
            canonical = self.skills / target
            canonical.mkdir(parents=True)
            (canonical / "SKILL.md").write_text(
                f"---\nname: {target}\ndescription: Test skill\n---\n",
                encoding="utf-8",
            )
            entry = self.skills / alias
            entry.mkdir()
            (entry / "SKILL.md").symlink_to(f"../{target}/SKILL.md")
            if alias in self.manifest_aliases:
                (canonical / "manifest.yaml").write_text(
                    f"connector: {target}\n", encoding="utf-8"
                )
                (entry / "manifest.yaml").symlink_to(f"../{target}/manifest.yaml")
        config = self.root / "skills.yaml"
        config.write_text("skills:\n", encoding="utf-8")
        scopes = self.root / "skill-scopes.conf"
        scopes.write_text("", encoding="utf-8")
        catalog = self.root / "catalog"
        catalog.mkdir()
        self.outputs = (catalog / "skills.json", catalog / "INDEX.md")
        globals_patch = patch.multiple(
            build_catalog,
            SKILLS=self.skills,
            CONFIG=config,
            SCOPES=scopes,
            OUT_JSON=self.outputs[0],
            OUT_INDEX=self.outputs[1],
            GROUPS={
                "social": list(self.manifest_aliases.values()),
                "media": list(self.no_manifest_aliases.values()),
            },
            GROUP_TITLES={"social": "Social", "media": "Media"},
        )
        globals_patch.start()
        self.addCleanup(globals_patch.stop)
        result, _, errors = self.run_catalog()
        self.assertEqual(result, 0, errors)

    def run_catalog(self, check=False):
        stdout, stderr = io.StringIO(), io.StringIO()
        argv = ["build_catalog.py"] + (["--check"] if check else [])
        with patch.object(build_catalog.sys, "argv", argv):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                result = build_catalog.main()
        return result, stdout.getvalue(), stderr.getvalue()

    def snapshot_outputs(self):
        return {
            path.name: (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.outputs
            if path.exists()
        }

    def assert_rejected(self, aliases, diagnostic):
        before = self.snapshot_outputs()
        for check in (True, False):
            with self.subTest(check=check):
                result, stdout, stderr = self.run_catalog(check=check)
                self.assertEqual(self.snapshot_outputs(), before)
                self.assertEqual(result, 1, stderr)
                self.assertEqual(stdout, "")
                for alias, target in aliases.items():
                    with self.subTest(alias=alias):
                        self.assertTrue(
                            any(
                                line.startswith(f"{alias}/manifest.yaml ")
                                and f"{target}/manifest.yaml" in line.partition(" ")[2]
                                and diagnostic in line
                                for line in stderr.splitlines()
                            ),
                            stderr,
                        )

    def test_valid_aliases_with_and_without_manifests(self):
        result, stdout, stderr = self.run_catalog(check=True)
        self.assertEqual(result, 0, stderr)
        self.assertEqual(stdout, "ok 4 skills\n")
        self.assertEqual(stderr, "")
        catalog = json.loads(self.outputs[0].read_text(encoding="utf-8"))
        self.assertEqual(
            catalog["aliases"], {**self.manifest_aliases, **self.no_manifest_aliases}
        )
        self.assertEqual(catalog["with_manifest"], 2)
        for alias, target in self.no_manifest_aliases.items():
            self.assertFalse((self.skills / alias / "manifest.yaml").exists())
            self.assertFalse((self.skills / target / "manifest.yaml").exists())

    def test_missing_manifests(self):
        for alias in self.manifest_aliases:
            (self.skills / alias / "manifest.yaml").unlink()
        self.assert_rejected(self.manifest_aliases, "missing")

    def test_copied_manifests(self):
        for alias in self.manifest_aliases:
            manifest = self.skills / alias / "manifest.yaml"
            contents = manifest.read_bytes()
            manifest.unlink()
            manifest.write_bytes(contents)
        self.assert_rejected(self.manifest_aliases, "not a symlink")

    def test_dangling_manifests(self):
        for alias in self.manifest_aliases:
            manifest = self.skills / alias / "manifest.yaml"
            manifest.unlink()
            manifest.symlink_to("../missing/manifest.yaml")
        self.assert_rejected(self.manifest_aliases, "dangling symlink")

    def test_incorrect_manifest_targets(self):
        for alias, target in (("facebook", "threads"), ("meta-threads", "facebook-cli")):
            manifest = self.skills / alias / "manifest.yaml"
            manifest.unlink()
            manifest.symlink_to(f"../{target}/manifest.yaml")
        self.assert_rejected(self.manifest_aliases, "does not point at")

    def test_dangling_links_to_missing_canonical_manifests(self):
        for alias, target in self.no_manifest_aliases.items():
            (self.skills / alias / "manifest.yaml").symlink_to(f"../{target}/manifest.yaml")
        self.assert_rejected(self.no_manifest_aliases, "dangling symlink")

    def test_invalid_aliases_do_not_create_outputs(self):
        for alias in self.manifest_aliases:
            (self.skills / alias / "manifest.yaml").unlink()
        for output in self.outputs:
            output.unlink()
        self.assert_rejected(self.manifest_aliases, "missing")


if __name__ == "__main__":
    unittest.main()
