"""Configuration file handling for TrueFocus Timer."""

import os
import json

DEFAULT_RESET_TIME = 600  # Default reset time in seconds (10 minutes)

def get_config_path():
    """Get the config file path."""
    config_dir = os.path.join(os.path.expanduser("~"), ".productivity_clock")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, "config.json")


def load_config(available_themes):
    """Load theme preference from config file."""
    try:
        config_path = get_config_path()
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                theme = config.get("theme", "dark")
                if theme in available_themes:
                    return theme
    except Exception as e:
        print(f"Error loading config: {e}")
    return "dark"


def save_config(theme):
    """Save theme preference to config file."""
    try:
        config_path = get_config_path()
        config = {"theme": theme}
        with open(config_path, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")
