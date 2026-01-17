<img width="889" height="724" alt="image" src="https://github.com/user-attachments/assets/3ce78fe4-7bd9-4e51-ac1c-e02ef1494ee8" />


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
pyinstaller --onefile --windowed --name TrueFocusTimer --add-data "assets/media;assets/media" --icon=assets/media/app_icon.ico main.py
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
