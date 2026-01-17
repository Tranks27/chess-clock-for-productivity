"""Theme management for TrueFocus Timer."""

THEMES = {
    "light": {
        "main_bg": "#2c3e50",
        "settings_bg": "#34495e",
        "frame_bg": "#ecf0f1",
        "button_inactive": "#3498db",
        "button_active": "#2ecc71",
        "button_stop": "#e74c3c",
        "button_reset": "#95a5a6",
        "warning_medium": "#f39c12",
        "warning_critical": "#e74c3c",
        "text_light": "white",
        "text_dark": "black",
        "text_muted": "#7f8c8d"
    },
    "dark": {
        "main_bg": "#1a1a1a",
        "settings_bg": "#252525",
        "frame_bg": "#2d2d2d",
        "button_inactive": "#1e88e5",
        "button_active": "#4caf50",
        "button_stop": "#d32f2f",
        "button_reset": "#616161",
        "warning_medium": "#ff6f00",
        "warning_critical": "#d32f2f",
        "text_light": "white",
        "text_dark": "#e0e0e0",
        "text_muted": "#9e9e9e"
    }
}


class ThemeManager:
    """Manages application themes."""

    def __init__(self, initial_theme="light"):
        self.current_theme = initial_theme
        self.themes = THEMES

    def get_color(self, key):
        """Get a color value from the current theme."""
        return self.themes[self.current_theme].get(key, "#000000")

    def get_theme_icon(self):
        """Get the theme toggle button icon."""
        return "☀️" if self.current_theme == "dark" else "🌙"

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
