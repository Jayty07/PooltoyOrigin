#!/usr/bin/env python3
"""Builds dist/Pooltoy-datapack.zip and dist/Pooltoy-resourcepack.zip."""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"


def build(zip_name, folder):
    DIST.mkdir(exist_ok=True)
    out = DIST / zip_name
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(ROOT / "pack.mcmeta", "pack.mcmeta")
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file():
                z.write(path, path.relative_to(ROOT).as_posix())
    print(f"built {out.relative_to(ROOT)}")


build("Pooltoy-datapack.zip", "data")
build("Pooltoy-resourcepack.zip", "assets")
