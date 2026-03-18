"""Theme management for TrueFocus Timer."""

THEMES = {
    "light": {
        "main_bg": "#2c3e50",
        "settings_bg": "#34495e",
        "frame_bg": "#ecf0f1",
        "button_inactive": "#3498db",
        "button_active": "#00d977",  # More vibrant emerald green
        "button_stop": "#ff4757",    # Brighter, warmer red
        "button_reset": "#95a5a6",
        "warning_medium": "#ffb000", # Brighter, more saturated amber
        "warning_critical": "#ff4757",
        "text_light": "white",
        "text_dark": "black",
        "text_muted": "#7f8c8d",
        "title_text": "#5f6b78",
        "accent_primary": "#00d4ff", # Cyan accent for highlights
        "accent_secondary": "#ff6b35" # Coral accent for depth
    },
    "dark": {
        "main_bg": "#1a1a1a",
        "settings_bg": "#252525",
        "frame_bg": "#2d2d2d",
        "button_inactive": "#2196f3",   # More vibrant blue
        "button_active": "#00e676",     # Brighter green
        "button_stop": "#ef5350",       # More vibrant red
        "button_reset": "#757575",      # Slightly lighter gray
        "warning_medium": "#ffb74d",    # Warmer, brighter orange
        "warning_critical": "#ef5350",
        "text_light": "white",
        "text_dark": "#e0e0e0",
        "text_muted": "#9e9e9e",
        "title_text": "#7a7a7a",
        "accent_primary": "#00d4ff",   # Cyan accent for highlights
        "accent_secondary": "#ff6b35"  # Coral accent for depth
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
