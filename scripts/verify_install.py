"""Exercise the native installer against isolated paths, including replacement."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="gptchan install ") as temporary:
    home = Path(temporary) / "codex home"
    pets = home / "pets"
    unrelated = pets / "another-pet" / "sentinel.txt"
    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("preserve", encoding="utf-8")
    command = (["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "scripts/install.ps1")]
               if os.name == "nt" else ["bash", str(ROOT / "scripts/install.sh")])
    env = {**os.environ, "CODEX_HOME": str(home)}
    subprocess.run(command, env=env, check=True)
    target = pets / "gpt-chan"
    target.joinpath("pet.json").write_text("existing configuration", encoding="utf-8")
    subprocess.run(command, env=env, check=True)
    backups = list(pets.glob("gpt-chan.backup.*/original"))
    assert len(backups) == 1
    assert (backups[0] / "pet.json").read_text(encoding="utf-8") == "existing configuration"
    for filename in ("pet.json", "spritesheet.webp"):
        assert (target / filename).read_bytes() == (ROOT / "output/gpt-chan" / filename).read_bytes()
    assert unrelated.read_text(encoding="utf-8") == "preserve"
    print("Verified install, backup, paths with spaces, and preservation of other pets.")
