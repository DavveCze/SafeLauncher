#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT_DIR/dist"

docker build -f "$ROOT_DIR/packaging/Dockerfile" -t safelauncher-appimage-builder "$ROOT_DIR"
docker run --rm -v "$ROOT_DIR/dist:/out" safelauncher-appimage-builder

echo "Built $ROOT_DIR/dist/SafeLauncher-x86_64.AppImage"
