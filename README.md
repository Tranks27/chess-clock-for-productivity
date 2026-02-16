<img width="891" height="680" alt="image" src="https://github.com/user-attachments/assets/ad5c6d87-d2e9-4806-a879-cb44e079cb78" />

# Productivity Timer

A desktop timer to track productivity vs. slack time.

# Very Quick Start
1. Download Executable (Windows): Download the `.exe` file from the [Releases](https://github.com/Tranks27/chess-clock-for-productivity/releases) page and run. 

## Features
- Productivity clock (counts down)
- Slack clock (counts up)
- Customizable time presets (1 hour, 2 hours, or custom)
- Editable timer names (@todo)
- Alarm sound when timer finishes
- Color warnings for low time
- Session statistics tracking with monthly file organization
- Interactive calendar view of work history
- **Idle detection** - Automatically detects when you haven't moved the mouse for 5 minutes and prompts you to switch to Slack timer (auto-switches after 3 minutes if no response)

## Data Storage Locations

### When Running the Executable (.exe)
All configuration and data files are stored in your user home directory for portability:
```
C:\Users\{YourUsername}\.productivity_clock\
├── config.json          # Theme preference (light/dark)
└── stats\
    ├── 2025-01.json     # Session history for January 2025
    ├── 2025-02.json     # Session history for February 2025
    └── ...
```
Stats are organized by month (YYYY-MM.json) to keep files manageable.

### When Running from Source (Python Script)
- **Stats:** Saved in the project directory: `project_root/stats/` with monthly files (2025-01.json, 2025-02.json, etc.)
- **Config:** Saved in user home directory: `C:\Users\{YourUsername}\.productivity_clock\config.json` (same as .exe)

### Accessing Your Data
- To view raw session data, open the monthly files (e.g., `2025-01.json`) in a text editor
- Theme preference and app settings are stored in `config.json`
- Delete these files to reset the app to default settings

## Idle Detection

The app automatically detects when you haven't moved your mouse for **5 minutes** and prompts you to switch to the Slack timer:

1. **Idle Alert** - A custom dialog box appears asking if you want to switch to Slack timer
   - Click **Yes** to immediately switch to Slack timer
   - Click **No** to dismiss and continue (but auto-switch timer still counts down)

2. **Auto-Switch Confirmation** - If you don't respond within **3 minutes**:
   - The prompt dialog automatically closes
   - The Slack timer is automatically activated
   - A confirmation popup notifies you: *"Auto-Switched to Slack"*
   - The session now accurately tracks your interruption time

3. **Activity Reset** - Moving your mouse while the timer is running cancels the idle detection and resets the counter

This helps catch unproductive breaks and ensures accurate time tracking without requiring user interaction.

## Installation

### Option 1: Download Executable (Windows)
Download the `.exe` file from the [Releases](https://github.com/Tranks27/chess-clock-for-productivity/releases) page.

### Option 2: Run from Source
1. Install Python 3.7+
2. $ python -m venv venv
2. $ pip install -r requirements.txt
3. Go into the environment- $ venv/Scripts/activate
4. $ python main.py


## Building Executable
```powershell
pip install pyinstaller
$version = python -c "from src import __version__; print(__version__)"
pyinstaller --onefile --windowed --name "TrueFocusTimer_v$version" --icon "assets/media/app_icon.ico" --add-data "assets;assets" --add-data "src;src" main.py
```
## Notes
If your desired custom sound file doesn't work, use online wav converter tool to convert the sound file. https://www.freeconvert.com/wav-converter

## License

This project is licensed under the **Creative Commons Attribution–NonCommercial 4.0
International License (CC BY-NC 4.0)**.

You are free to:
- Use the software for personal and educational purposes
- Modify and experiment with the source code
- Share and redistribute the software

Under the following terms:
- **NonCommercial** — You may not use this project for commercial purposes,
  including selling the software or incorporating it into commercial products
  or services.
- **Attribution** — You must give appropriate credit when redistributing. ✓ Must remain open source

See [LICENSE](LICENSE) file for full details.

## Version
Current version: 1.0.0
