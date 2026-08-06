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

- Python 3.9+
- PyQt6
- Firejail (for sandboxing)
- Wine or UMU (for running Windows games)

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

### For developers: build the AppImage

You only need Docker and internet access. From the repository root, run:

```bash
./packaging/build-appimage-docker.sh
```

That command installs the build dependencies inside Docker, builds the
application, and creates `dist/MGLauncher-x86_64.AppImage`. Share that single
file with users; they do not need Docker, Python, PyQt6, or the source tree.

### Optional: run from source

This is only needed for development. It is not required to use the AppImage.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

To add an application-menu shortcut for the source checkout:

```bash
./install_desktop_entry.sh
```

## Usage

### Launch the Application

```bash
python main.py
```

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

## Project Structure

```
MGLauncher/
├── main.py                 # Entry point - launches PyQt6 app
├── database.py             # SQLite database management
├── requirements.txt        # Python dependencies
├── core/
│   ├── __init__.py
│   ├── interfaces.py       # Abstract base classes
│   ├── firejail_runner.py  # Sandbox execution
│   └── zip_backup.py       # Save import/export
└── ui/
    ├── __init__.py
    └── main_window.py      # PyQt6 UI components
```

## Configuration

Games are stored in an SQLite database (`library.db`) in the project directory.

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
