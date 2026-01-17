"""Audio and alarm handling for TrueFocus Timer."""

import os
import sys
import threading
import time
import winsound


def get_script_dir():
    """Get the correct directory for both script and .exe."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys._MEIPASS
    else:
        # Running as script - go up one level from src/ to project root
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AlarmPlayer:
    """Handles alarm sound playback."""

    def __init__(self):
        self.alarm_playing = False
        self.alarm_thread = None

    def play_alarm_loop(self, alarm_path):
        """Play alarm sound in a loop until stopped."""
        while self.alarm_playing:
            try:
                # Play sound asynchronously
                winsound.PlaySound(alarm_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

                # Wait for sound to finish, but check alarm_playing frequently
                # Average alarm is 3-5 seconds, check every 0.1 seconds
                for _ in range(50):  # Check for 5 seconds max
                    if not self.alarm_playing:
                        break
                    time.sleep(0.1)

            except Exception as e:
                print(f"Error playing alarm: {e}")
                break

    def start_alarm(self, alarm_path):
        """Start looping alarm in a separate thread."""
        self.alarm_playing = True
        self.alarm_thread = threading.Thread(
            target=self.play_alarm_loop,
            args=(alarm_path,),
            daemon=True
        )
        self.alarm_thread.start()

    def stop_alarm(self):
        """Stop the looping alarm."""
        self.alarm_playing = False
        # Stop any currently playing sound
        winsound.PlaySound(None, winsound.SND_PURGE)
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join(timeout=1.0)

    def get_alarm_path(self):
        """Get the path to the alarm sound file."""
        script_dir = get_script_dir()
        return os.path.join(script_dir, "assets", "media", "alarm.wav")

    def play_error_sound(self):
        """Play a system error sound as fallback."""
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
