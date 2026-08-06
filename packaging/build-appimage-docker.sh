#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT_DIR/dist"

docker build -f "$ROOT_DIR/packaging/Dockerfile" -t mglauncher-appimage-builder "$ROOT_DIR"
docker run --rm -v "$ROOT_DIR/dist:/out" mglauncher-appimage-builder

echo "Built $ROOT_DIR/dist/MGLauncher-x86_64.AppImage"
