"""Theme management for TrueFocus Timer."""

THEMES = {
    "light": {
        "main_bg": "#F5EBDD",
        "settings_bg": "#1F3A5F",
        "frame_bg": "#FFFDF8",
        "button_inactive": "#0EA5A4",
        "button_active": "#E85D04",
        "button_stop": "#C1121F",
        "button_reset": "#6B7280",
        "warning_medium": "#D97706",
        "warning_critical": "#B91C1C",
        "text_light": "#F8F5EE",
        "text_dark": "#1A2333",
        "text_muted": "#6B7280",
        "title_text": "#1F3A5F"
    },
    "dark": {
        "main_bg": "#111827",
        "settings_bg": "#0F2A3A",
        "frame_bg": "#1F2937",
        "button_inactive": "#06B6D4",
        "button_active": "#F59E0B",
        "button_stop": "#EF4444",
        "button_reset": "#6B7280",
        "warning_medium": "#FB923C",
        "warning_critical": "#F87171",
        "text_light": "#E5E7EB",
        "text_dark": "#E5E7EB",
        "text_muted": "#9CA3AF",
        "title_text": "#67E8F9"
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
