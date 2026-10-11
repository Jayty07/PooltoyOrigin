#!/usr/bin/env python3
"""Builds dist/Pooltoy-<version>.jar (Forge/NeoForge + Fabric mod) plus the
standalone dist/Pooltoy-datapack.zip and dist/Pooltoy-resourcepack.zip."""
import zipfile
from pathlib import Path

VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def files(folder):
    return [p for p in sorted((ROOT / folder).rglob("*")) if p.is_file()]


def build_pack(zip_name, folder):
    out = DIST / zip_name
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(ROOT / "pack.mcmeta", "pack.mcmeta")
        for path in files(folder):
            z.write(path, path.relative_to(ROOT).as_posix())
    print(f"built {out.relative_to(ROOT)}")


def build_jar():
    out = DIST / f"Pooltoy-{VERSION}.jar"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("META-INF/MANIFEST.MF", "Manifest-Version: 1.0\n")
        z.write(ROOT / "pack.mcmeta", "pack.mcmeta")
        for path in files("mod"):
            text = path.read_text(encoding="utf-8").replace("${version}", VERSION)
            z.writestr(path.relative_to(ROOT / "mod").as_posix(), text)
        for folder in ("data", "assets"):
            for path in files(folder):
                z.write(path, path.relative_to(ROOT).as_posix())
    print(f"built {out.relative_to(ROOT)}")


DIST.mkdir(exist_ok=True)
for old in DIST.glob("Pooltoy-*.jar"):
    old.unlink()
build_jar()
build_pack("Pooltoy-datapack.zip", "data")
build_pack("Pooltoy-resourcepack.zip", "assets")
