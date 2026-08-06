#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"
APPIMAGE_TOOL="${APPIMAGE_TOOL:-appimagetool}"
APPIMAGE_TOOL_ARGS="${APPIMAGE_TOOL_ARGS:-}"
APPDIR="$ROOT_DIR/build/AppDir"
OUTPUT_DIR="$ROOT_DIR/dist"

command -v "$PYTHON_BIN" >/dev/null || {
    echo "Python was not found: $PYTHON_BIN" >&2
    exit 1
}
command -v "$APPIMAGE_TOOL" >/dev/null || {
    echo "appimagetool was not found. Use packaging/build-appimage-docker.sh or install it." >&2
    exit 1
}

"$PYTHON_BIN" -m PyInstaller --noconfirm --clean packaging/safelauncher.spec

rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" \
    "$APPDIR/usr/share/applications" \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps"

install -m 0755 dist/SafeLauncher "$APPDIR/usr/bin/SafeLauncher"
install -m 0755 packaging/AppRun "$APPDIR/AppRun"
install -m 0644 packaging/safelauncher.desktop "$APPDIR/usr/share/applications/safelauncher.desktop"
install -m 0644 assets/logo.png "$APPDIR/usr/share/icons/hicolor/256x256/apps/safelauncher.png"
install -m 0644 packaging/safelauncher.desktop "$APPDIR/safelauncher.desktop"
install -m 0644 assets/logo.png "$APPDIR/safelauncher.png"

mkdir -p "$OUTPUT_DIR"
read -r -a APPIMAGE_TOOL_ARGS_ARRAY <<< "$APPIMAGE_TOOL_ARGS"
"$APPIMAGE_TOOL" "${APPIMAGE_TOOL_ARGS_ARRAY[@]}" "$APPDIR" "$OUTPUT_DIR/SafeLauncher-x86_64.AppImage"
chmod +x "$OUTPUT_DIR/SafeLauncher-x86_64.AppImage"
echo "Built $OUTPUT_DIR/SafeLauncher-x86_64.AppImage"
