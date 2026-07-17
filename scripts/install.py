#!/usr/bin/env python3
"""One-click install for meeting-notes dependencies. Idempotent.

Usage:
    python install.py           # Install everything
    python install.py --check   # Check status only
"""

import sys
import subprocess
import importlib
import urllib.request
import zipfile, io, shutil, os
from pathlib import Path

REQUIRED_PIP = ["requests", "pyyaml"]
SCRIPT_DIR = Path(__file__).resolve().parent


def check_pip(pkg):
    try:
        importlib.import_module(pkg.replace("-", "_"))
        return True
    except ImportError:
        return False


def install_pip():
    missing = [p for p in REQUIRED_PIP if not check_pip(p)]
    if not missing:
        print("[OK] pip packages: all installed")
        return
    print(f"Installing: {' '.join(missing)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    print("[OK] pip packages installed")


def check_ffmpeg():
    ff = SCRIPT_DIR / ("ffmpeg.exe" if os.name == "nt" else "ffmpeg")
    if ff.exists():
        print(f"[OK] ffmpeg: {ff}")
        return True
    # Also check PATH
    if shutil.which("ffmpeg"):
        print("[OK] ffmpeg: in PATH")
        return True
    return False


def install_ffmpeg():
    if check_ffmpeg():
        return

    if sys.platform == "darwin":
        print("Installing ffmpeg via Homebrew...")
        subprocess.check_call(["brew", "install", "ffmpeg"])
        print("[OK] ffmpeg installed")
        return

    # Windows: download BtbN portable
    print("Downloading ffmpeg (BtbN portable, ~70MB)...")
    url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    with urllib.request.urlopen(url) as r:
        data = r.read()
    tmp = Path(os.environ.get("TEMP", "/tmp")) / "ffmpeg_install"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        z.extractall(tmp)
    inner = next(tmp.iterdir())
    shutil.copy2(inner / "bin" / "ffmpeg.exe", SCRIPT_DIR / "ffmpeg.exe")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[OK] ffmpeg: {SCRIPT_DIR / 'ffmpeg.exe'}")


def main():
    check_only = "--check" in sys.argv
    if check_only:
        print("=== Dependency Check ===")
        ok = True
        for p in REQUIRED_PIP:
            status = "OK" if check_pip(p) else "MISSING"
            if status == "MISSING": ok = False
            print(f"  {p}: {status}")
        ff = "OK" if check_ffmpeg() else "MISSING"
        if ff == "MISSING": ok = False
        print(f"  ffmpeg: {ff}")
        sys.exit(0 if ok else 1)

    print("=== Meeting Notes — Install ===")
    install_pip()
    install_ffmpeg()
    print()
    print("All dependencies ready.")
    print("Set WHISPER_API_KEY env var if using audio transcription.")


if __name__ == "__main__":
    main()
