FROM python:3.11-bookworm

ARG APPIMAGE_TOOL_URL=https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage

RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates curl file fuse3 \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL "$APPIMAGE_TOOL_URL" -o /usr/local/bin/appimagetool \
    && chmod +x /usr/local/bin/appimagetool

WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pyinstaller
COPY . .

CMD ["bash", "-lc", "APPIMAGE_TOOL_ARGS=--appimage-extract-and-run packaging/build-appimage.sh && cp dist/SafeLauncher-x86_64.AppImage /out/"]
