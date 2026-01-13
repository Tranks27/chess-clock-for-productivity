<img width="896" height="726" alt="image" src="https://github.com/user-attachments/assets/4736cd41-5630-4cbb-9b68-250157029f3a" />

# Productivity Timer

A desktop timer to track productivity vs. slack time.

## Features
- Productivity clock (counts down)
- Slack clock (counts up)
- Customizable time presets (1 hour, 2 hours, or custom)
- Editable timer names (@todo)
- Alarm sound when timer finishes
- Color warnings for low time

## Installation

### Option 1: Download Executable (Windows)
Download the `.exe` file from the [Releases](https://github.com/yourusername/productivity-timer/releases) page.

### Option 2: Run from Source
1. Install Python 3.7+
2. $ python -m venv venv
2. $ pip install -r requirements.txt
3. Go into the environment- $ venv/Scripts/activate
4. $ python main.py


## Building Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name ProductivityClock --add-data "assets;assets" main.py
```

## Version
Current version: 1.0.0