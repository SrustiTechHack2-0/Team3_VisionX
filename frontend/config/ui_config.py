
# UI Configuration and Constants

# Theme Colors
COLORS = {
    "background": "#1a1a1a",
    "primary": "#00ff00",
    "secondary": "#2a2a2a",
    "text_primary": "#ffffff",
    "text_secondary": "#cccccc",
    "alert_red": "#ff4444",
    "warning_yellow": "#ffaa00",
    "info_blue": "#4488ff",
    "pet_orange": "#ff8800",
    "success_green": "#00cc00"
}

# Layout Constraints
LAYOUT = {
    "min_width": 1280,
    "max_width": 1920,
    "padding": "1rem",
}

# App Config
APP_TITLE = "SurakshaSetu - Smart Security System"
APP_ICON = "🛡️"

# Alert Types
ALERT_TYPES = {
    "TAILGATING": {"color": COLORS["alert_red"], "icon": "⚠️"},
    "WEAPON": {"color": COLORS["alert_red"], "icon": "🔫"},
    "PET": {"color": COLORS["pet_orange"], "icon": "🐕"},
    "CROWD": {"color": COLORS["warning_yellow"], "icon": "👥"},
    "UNAUTHORIZED": {"color": COLORS["alert_red"], "icon": "🚫"},
}
