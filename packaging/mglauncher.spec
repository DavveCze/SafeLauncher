# PyInstaller one-file build used as the payload inside the AppImage.
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules


ROOT = Path(SPEC).parent.parent

hiddenimports = [
    "PyQt6.QtNetwork",
    "PyQt6.QtPrintSupport",
    *collect_submodules("ui"),
    *collect_submodules("core"),
]

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[(str(ROOT / "assets"), "assets")],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="MGLauncher",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)
