"""
Icon helper module for SafeLauncher providing crisp Phosphor & FontAwesome vector icons
via QtAwesome with automatic fallback handling.
"""

from typing import Optional
from PyQt6.QtGui import QIcon

try:
    import qtawesome as qta
    _QTA_AVAILABLE = True
except ImportError:
    _QTA_AVAILABLE = False


def get_icon(name: str, color: str = "#ffffff", active_color: Optional[str] = None) -> QIcon:
    """Get high-resolution vector QIcon.
    
    Examples:
        get_icon('ph.game-controller-bold', color='#ffffff')
        get_icon('ph.arrows-clockwise-bold', color='#64b5f6')
    """
    if not _QTA_AVAILABLE:
        return QIcon()
    
    try:
        kwargs = {"color": color}
        if active_color:
            kwargs["color_active"] = active_color
            kwargs["color_selected"] = active_color
        return qta.icon(name, **kwargs)
    except Exception as e:
        print(f"Icon load warning for '{name}': {e}")
        return QIcon()


# Pre-defined Icon Key Mappings for SafeLauncher
ICONS = {
    "library": ("ph.game-controller-bold", "#ffffff"),
    "sandbox": ("ph.folder-open-bold", "#ffffff"),
    "sync": ("ph.arrows-clockwise-bold", "#64b5f6"),
    "launch": ("fa5s.play", "#ffffff"),
    "add": ("ph.plus-bold", "#ffffff"),
    "edit": ("ph.pencil-bold", "#ffffff"),
    "remove": ("ph.trash-bold", "#ffffff"),
    "export": ("ph.floppy-disk-bold", "#ffffff"),
    "import": ("ph.download-bold", "#ffffff"),
    "minimize": ("fa5s.minus", "#aaaaaa"),
    "maximize": ("fa5s.square", "#aaaaaa"),
    "restore": ("fa5s.clone", "#aaaaaa"),
    "close": ("fa5s.times", "#aaaaaa"),
    "search": ("ph.magnifying-glass-bold", "#ffffff"),
    "shield": ("fa5s.shield-alt", "#ffffff"),
    "globe": ("fa5s.globe", "#ffffff"),
    "wine": ("fa5s.wine-glass", "#ffffff"),
    "terminal": ("fa5s.terminal", "#ffffff"),
}


def get_app_icon(key: str, color: Optional[str] = None) -> QIcon:
    """Retrieve pre-configured icon by key name."""
    if key in ICONS:
        name, default_color = ICONS[key]
        return get_icon(name, color=color or default_color)
    return QIcon()
