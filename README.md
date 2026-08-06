# MGLauncher - Game Sandbox Launcher

A PyQt6-based GUI launcher for sandboxed games using Firejail. Manage your game library and launch games in isolated sandboxes with Wine/UMU support.

## Features

✨ **Game Library Management**
- Add games with custom paths and executables
- Remove games from library
- Launch games with a double-click or button

🎮 **Sandbox Support**
- UMU (Unified Multi-platform Utility) with Firejail
- Wine with Firejail
- No network isolation option available

💾 **Save Management**
- Export game saves as ZIP archives
- Import saves from ZIP archives
- Automatic save directory detection

🗄️ **Database**
- SQLite database for persistent game library
- Game metadata: name, path, executable, launch mode

## Requirements

- Linux desktop
- Firejail for sandboxing
- Wine or UMU for Windows games
- Steam and graphics drivers as required by your games

## Installation

### For users: download and run the AppImage

There is no Python setup or `pip` command needed. Download the latest
`MGLauncher-x86_64.AppImage`, make it executable once, and launch it:

```bash
chmod +x MGLauncher-x86_64.AppImage
./MGLauncher-x86_64.AppImage
```

The AppImage includes MGLauncher, Python, PyQt6, requests, and Pillow. You
still need Firejail and Wine or UMU installed for Windows game launching.
Steam, graphics drivers, and game files are provided by the host system.

Install the host game dependencies once:

```bash
sudo apt install firejail wine       # Ubuntu/Debian
# sudo dnf install firejail wine      # Fedora
# sudo pacman -S firejail wine        # Arch
```

MGLauncher will tell you when a required host tool is missing.

## Usage

### Add a Game

1. Click **Add Game** button
2. Enter game name
3. Click **Browse...** and select the game directory
4. Enter the executable filename (e.g., `game.exe`)
5. Select launch mode (UMU or Wine)
6. Click **Add**

### Launch a Game

- Double-click a game in the library, OR
- Select a game and click **▶ Launch Selected Game**

### Export Saves

1. Select a game
2. Click **💾 Export Save**
3. Choose location and filename
4. Save is packaged as ZIP

### Import Saves

1. Select a game
2. Click **📂 Import Save**
3. Select a ZIP file with save data
4. Save is extracted to game directory

## Configuration

Your library and settings are stored in `~/.local/share/mglauncher/`.
Downloaded artwork is cached in `~/.cache/mglauncher/`.

## Troubleshooting

**Firejail Permission Denied:**
```bash
sudo chmod u+s /usr/bin/firejail
```

**Wine Prefix Issues:**
Games automatically create Wine prefix in `<game_path>/prefix`

**UMU Not Found:**
Install UMU from the official repository or use Wine mode instead

## License

Created for personal use
