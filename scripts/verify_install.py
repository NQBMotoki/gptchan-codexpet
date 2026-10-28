"""End-to-end package/install/outfit checks in isolated directories."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import petctl
ROOT = Path(__file__).resolve().parents[1]

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gptchan install ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "source package"
        for directory in ("scripts", "output/gpt-chan", "docs"):
            shutil.copytree(ROOT / directory, self.root / directory, ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("outfits.json", "VERSION", "NOTICE.md", "README.md", "INSTALL.md", "CHANGELOG.md", "requirements.txt"):
            shutil.copy2(ROOT / name, self.root / name)
        self.home = self.base / "codex home"
        self.target = self.home / "pets/gpt-chan"
        self.other = self.home / "pets/another-pet/sentinel.txt"
        self.other.parent.mkdir(parents=True)
        self.other.write_text("preserve", encoding="utf-8")

    def cli(self, *args, success=True, root=None):
        result = subprocess.run([sys.executable, str((root or self.root) / "scripts/petctl.py"), *args],
                                capture_output=True, text=True, encoding="utf-8",
                                env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result

    def install(self):
        return self.cli("install", "--codex-home", str(self.home))

    def snapshot(self):
        return {p.name: p.read_bytes() for p in self.target.iterdir() if p.is_file()}

    def test_install_idempotence_doctor_and_unrelated_pet(self):
        self.assertEqual(self.install()["status"], "installed")
        first = self.snapshot()
        self.assertEqual(self.install()["status"], "unchanged")
        self.assertEqual(first, self.snapshot())
        self.assertEqual(petctl.backup_list(self.home), [])
        result = self.cli("doctor", "--codex-home", str(self.home))
        self.assertTrue(result["integrityMatchesRecord"])
        self.assertEqual(result["releaseInfo"]["outfitId"], "classic")
        self.assertIn("unverified", result["activeDisplaySource"])
        self.assertEqual(self.other.read_text(), "preserve")

    def test_invalid_sources_preserve_existing_package(self):
        self.install()
        before = self.snapshot()
        manifest = self.root / "output/gpt-chan/pet.json"
        sheet = self.root / "output/gpt-chan/spritesheet.webp"
        original_manifest, original_sheet = manifest.read_bytes(), sheet.read_bytes()
        invalid_manifests = [b"not json", b"[]", json.dumps({"id": "wrong"}).encode()]
        for value in invalid_manifests:
            manifest.write_bytes(value)
            self.cli("install", "--codex-home", str(self.home), success=False)
            self.assertEqual(before, self.snapshot())
        manifest.write_bytes(original_manifest)
        for value in (b"", original_sheet[:100], original_sheet[:-1]):
            sheet.write_bytes(value)
            self.cli("install", "--codex-home", str(self.home), success=False)
            self.assertEqual(before, self.snapshot())
        self.assertEqual(petctl.backup_list(self.home), [])

    def test_modified_valid_source_rejected_by_catalog_hash(self):
        self.install()
        before = self.snapshot()
        manifest = self.root / "output/gpt-chan/pet.json"
        value = petctl.read_json(manifest)
        value["description"] = "unexpected unregistered change"
        petctl.write_json(manifest, value)
        result = self.cli("install", "--codex-home", str(self.home), success=False)
        self.assertIn("hash", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_backup_restore_and_uninstall(self):
        self.install()
        original = self.snapshot()
        petctl.write_json(self.target / "pet.json", {"existing": "legacy invalid config"})
        self.install()
        backups = petctl.backup_list(self.home)
        self.assertEqual(len(backups), 1)
        self.assertEqual(petctl.read_json(self.home / ".pet-backups/gpt-chan" / backups[0] / "pet.json"), {"existing": "legacy invalid config"})
        result = self.cli("uninstall", "--codex-home", str(self.home))
        self.assertFalse(self.target.exists())
        self.cli("restore", Path(result["backup"]).name, "--codex-home", str(self.home))
        self.assertEqual(original, self.snapshot())
        self.assertEqual(self.other.read_text(), "preserve")

    def test_outfit_registration_switch_and_return_same_pet_id(self):
        self.install()
        source = self.base / "TEST ONLY outfit"
        shutil.copytree(self.root / "output/gpt-chan", source)
        shutil.copy2(self.root / "NOTICE.md", source / "NOTICE.md")
        value = petctl.read_json(source / "pet.json")
        value["description"] = "TEST ONLY alternate package, not new artwork"
        petctl.write_json(source / "pet.json", value)
        self.cli("import-outfit", "test-dress", "--source", str(source), "--name", "TEST ONLY outfit")
        self.cli("install", "--outfit", "test-dress", "--codex-home", str(self.home))
        self.assertEqual(petctl.read_json(self.target / "pet.json")["id"], "gpt-chan")
        self.assertEqual(petctl.read_json(self.target / "release-info.json")["outfitId"], "test-dress")
        backup = petctl.backup_list(self.home)[0]
        self.cli("restore", backup, "--codex-home", str(self.home))
        self.assertEqual(petctl.read_json(self.target / "release-info.json")["outfitId"], "classic")
        self.assertEqual(len(list((self.home / "pets").iterdir())), 2)

    def test_failure_between_directory_moves_restores_original(self):
        self.install()
        before = self.snapshot()
        folder, metadata = petctl.source_pack(root=self.root)
        metadata["version"] = "test-failure"
        original_rename = Path.rename
        def fail_stage(path, destination):
            if path.parent.name == ".pet-staging":
                raise OSError("injected staging rename failure")
            return original_rename(path, destination)
        with patch.object(Path, "rename", fail_stage):
            with self.assertRaisesRegex(OSError, "injected"):
                petctl.swap_pack(folder, self.home, metadata, self.root / "NOTICE.md")
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.home / ".gpt-chan.lock").exists())
        self.assertEqual(list((self.home / ".pet-staging").iterdir()), [])

    def test_doctor_read_only_detects_modified_install(self):
        self.install()
        manifest = self.target / "pet.json"
        value = petctl.read_json(manifest)
        value["description"] = "local edit"
        petctl.write_json(manifest, value)
        before = self.snapshot()
        result = self.cli("doctor", "--codex-home", str(self.home), success=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(before, self.snapshot())

    def test_source_path_escape_and_backup_traversal_rejected(self):
        info = petctl.read_json(self.root / "outfits.json")
        info["outfits"]["classic"]["path"] = "../outside"
        petctl.write_json(self.root / "outfits.json", info)
        self.cli("install", "--codex-home", str(self.home), success=False)
        self.cli("restore", "../outside", "--codex-home", str(self.home), success=False)
        self.assertFalse(self.target.exists())

    def test_lock_blocks_writes(self):
        self.home.mkdir(exist_ok=True)
        (self.home / ".gpt-chan.lock").write_text("held")
        self.cli("install", "--codex-home", str(self.home), success=False)
        self.assertFalse(self.target.exists())

    def test_native_wrapper(self):
        env = {**os.environ, "CODEX_HOME": str(self.home), "GPTCHAN_PYTHON": sys.executable,
               "PYTHONIOENCODING": "utf-8"}
        if os.name == "nt":
            command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                       str(self.root / "scripts/install.ps1"), "-Python", sys.executable]
        else:
            command = ["bash", str(self.root / "scripts/install.sh")]
        result = subprocess.run(command, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.target.is_dir())

    def test_release_archive_install_and_repeatable_build(self):
        command = [sys.executable, str(self.root / "scripts/build.py"), "--no-previews"]
        for _ in range(2):
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            digest = petctl.sha256(self.root / "dist/gptchan-codexpet.zip")
            if _ == 0:
                first = digest
        self.assertEqual(first, digest)
        release = self.base / "extracted release"
        shutil.unpack_archive(self.root / "dist/gptchan-codexpet.zip", release)
        self.cli("install", "--codex-home", str(self.home), root=release)
        self.assertTrue(petctl.read_json(self.target / "release-info.json")["version"])
        self.assertTrue((release / "scripts/install.ps1").is_file())
        self.assertTrue((release / "CHANGELOG.md").is_file())

if __name__ == "__main__":
    unittest.main(verbosity=2)
