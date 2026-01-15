import tkinter as tk
import time
import winsound  # Windows built-in sound library
import os
import sys
import threading
import json

__version__ = "1.2.0"
__developer_name__ = "AYJ Systems"
class ChessClock:
    def __init__(self, root):
        self.root = root
        self.root.title("TrueFocus Timer")
        self.root.geometry("900x700")

        # Set window icon
        try:
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                icon_path = os.path.join(sys._MEIPASS, "assets", "media", "app_icon.ico")
            else:
                # Running as script
                icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "media", "app_icon.ico")

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon loading error: {e}")

        # Time variables (in seconds)
        self.player1_time = 600  # Productivity - counts down (10 minutes default)
        self.player2_time = 0    # Slack - counts up
        self.active_player = None
        self.running = False
        self.last_update = None

        # Alarm control
        self.alarm_playing = False
        self.alarm_thread = None

        # Theme management
        self.themes = {
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
        self.current_theme = "light"
        self.load_config()

        self.root.configure(bg=self.themes[self.current_theme]["main_bg"])
        self.create_widgets()

    def get_config_path(self):
        """Get the config file path"""
        config_dir = os.path.join(os.path.expanduser("~"), ".productivity_clock")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, "config.json")

    def load_config(self):
        """Load theme preference from config file"""
        try:
            config_path = self.get_config_path()
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    theme = config.get("theme", "dark")
                    if theme in self.themes:
                        self.current_theme = theme
        except Exception as e:
            print(f"Error loading config: {e}")
            self.current_theme = "dark"

    def save_config(self):
        """Save theme preference to config file"""
        try:
            config_path = self.get_config_path()
            config = {"theme": self.current_theme}
            with open(config_path, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_t(self, key):
        """Get a color value from the current theme"""
        return self.themes[self.current_theme].get(key, "#000000")

    def get_theme_icon(self):
        """Get the theme toggle button icon"""
        return "☀️" if self.current_theme == "dark" else "🌙"

    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.save_config()
        self.apply_theme()

    def apply_theme(self):
        """Apply the current theme to all widgets"""
        # Main window
        self.root.configure(bg=self.get_t("main_bg"))

        # Title
        self.title_widget.config(bg=self.get_t("main_bg"), fg=self.get_t("text_light"))

        # Settings frame
        self.settings.config(bg=self.get_t("settings_bg"))
        self.settings_time_label.config(bg=self.get_t("settings_bg"), fg=self.get_t("text_light"))
        self.time_btn_1hr.config(bg=self.get_t("button_inactive"), fg=self.get_t("text_light"))
        self.time_btn_2hr.config(bg=self.get_t("button_inactive"), fg=self.get_t("text_light"))
        self.custom_label.config(bg=self.get_t("settings_bg"), fg=self.get_t("text_light"))
        self.custom_entry.config(bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))
        self.custom_btn.config(bg=self.get_t("button_inactive"), fg=self.get_t("text_light"))
        self.theme_toggle_btn.config(text=self.get_theme_icon(),
                                    bg=self.get_t("button_inactive"),
                                    fg=self.get_t("text_light"))

        # Clocks frame
        self.clocks.config(bg=self.get_t("main_bg"))

        # Player 1
        self.p1_frame.config(bg=self.get_t("frame_bg"))
        self.p1_name.config(bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))
        self.p1_time.config(bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))
        self.p1_btn.config(bg=self.get_t("button_inactive"), fg=self.get_t("text_light"),
                          activebackground=self.get_t("button_inactive"))

        # Player 2
        self.p2_frame.config(bg=self.get_t("frame_bg"))
        self.p2_name.config(bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))
        self.p2_time.config(bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))
        self.p2_btn.config(bg=self.get_t("button_inactive"), fg=self.get_t("text_light"),
                          activebackground=self.get_t("button_inactive"))

        # Controls
        self.controls.config(bg=self.get_t("main_bg"))
        self.pause_btn.config(bg=self.get_t("button_stop"), fg=self.get_t("text_light"))
        self.reset_btn.config(bg=self.get_t("button_reset"), fg=self.get_t("text_light"))

        # Footer frame and labels
        self.footer.config(bg=self.get_t("main_bg"))
        self.company_label.config(bg=self.get_t("main_bg"), fg=self.get_t("text_muted"))
        self.version_label.config(bg=self.get_t("main_bg"), fg=self.get_t("text_muted"))

        # Refresh time display to apply warning colors in current theme
        self.display_times()

    def create_widgets(self):
        # Title
        self.title_widget = tk.Label(self.root, text="TrueFocus Timer", font=('Arial', 24, 'bold'),
                        bg=self.get_t("main_bg"), fg=self.get_t("text_light"))
        self.title_widget.pack(pady=15)

        # Settings
        self.settings = tk.Frame(self.root, bg=self.get_t("settings_bg"), relief=tk.RAISED, bd=2)
        self.settings.pack(pady=10, padx=20, fill=tk.X)

        self.settings_time_label = tk.Label(self.settings, text="Time:", font=('Arial', 11),
                bg=self.get_t("settings_bg"), fg=self.get_t("text_light"))
        self.settings_time_label.pack(side=tk.LEFT, padx=10)

        self.time_btn_1hr = tk.Button(self.settings, text="1 hour", width=8,
                 command=lambda: self.set_time(3600),
                 bg=self.get_t("button_inactive"), fg=self.get_t("text_light"))
        self.time_btn_1hr.pack(side=tk.LEFT, padx=3)

        self.time_btn_2hr = tk.Button(self.settings, text="2 hour", width=8,
                 command=lambda: self.set_time(7200),
                 bg=self.get_t("button_inactive"), fg=self.get_t("text_light"))
        self.time_btn_2hr.pack(side=tk.LEFT, padx=3)

        self.custom_label = tk.Label(self.settings, text="Custom (min):", font=('Arial', 11),
                bg=self.get_t("settings_bg"), fg=self.get_t("text_light"))
        self.custom_label.pack(side=tk.LEFT, padx=(15, 5))

        self.custom_entry = tk.Entry(self.settings, width=8, font=('Arial', 11),
                                     bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))
        self.custom_entry.pack(side=tk.LEFT, padx=3)

        self.custom_btn = tk.Button(self.settings, text="Set", width=6,
                 command=self.set_custom,
                 bg=self.get_t("button_inactive"), fg=self.get_t("text_light"))
        self.custom_btn.pack(side=tk.LEFT, padx=3)

        # Theme toggle button (right side of settings)
        self.theme_toggle_btn = tk.Button(self.settings, text=self.get_theme_icon(),
                                         font=('Arial', 11), width=4, height=1,
                                         command=self.toggle_theme,
                                         bg=self.get_t("button_inactive"),
                                         fg=self.get_t("text_light"))
        self.theme_toggle_btn.pack(side=tk.RIGHT, padx=10)

        # Clocks
        self.clocks = tk.Frame(self.root, bg=self.get_t("main_bg"))
        self.clocks.pack(pady=25, expand=True, fill=tk.BOTH)

        # Player 1
        self.p1_frame = tk.Frame(self.clocks, bg=self.get_t("frame_bg"), relief=tk.RAISED, bd=4)
        self.p1_frame.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.BOTH)

        self.p1_name = tk.Entry(self.p1_frame, font=('Arial', 16, 'bold'),
                               justify='center', bg=self.get_t("frame_bg"),
                               fg=self.get_t("text_dark"), relief=tk.FLAT)
        self.p1_name.insert(0, "Productivity")
        self.p1_name.pack(pady=15)

        self.p1_time = tk.Label(self.p1_frame, text="00:10:00",
                               font=('Arial', 56, 'bold'), bg=self.get_t("frame_bg"),
                               fg=self.get_t("text_dark"))
        self.p1_time.pack(pady=40)

        self.p1_btn = tk.Button(self.p1_frame, text="CLICK",
                               font=('Arial', 16, 'bold'),
                               bg=self.get_t("button_inactive"), fg=self.get_t("text_light"),
                               activebackground=self.get_t("button_inactive"),
                               height=3, width=15)
        self.p1_btn.config(command=lambda: self.button_click(1))
        self.p1_btn.pack(pady=25)

        # Player 2
        self.p2_frame = tk.Frame(self.clocks, bg=self.get_t("frame_bg"), relief=tk.RAISED, bd=4)
        self.p2_frame.pack(side=tk.RIGHT, padx=15, expand=True, fill=tk.BOTH)

        self.p2_name = tk.Entry(self.p2_frame, font=('Arial', 16, 'bold'),
                               justify='center', bg=self.get_t("frame_bg"),
                               fg=self.get_t("text_dark"), relief=tk.FLAT)
        self.p2_name.insert(0, "Slack")
        self.p2_name.pack(pady=15)

        self.p2_time = tk.Label(self.p2_frame, text="00:00:00",
                               font=('Arial', 56, 'bold'), bg=self.get_t("frame_bg"),
                               fg=self.get_t("text_dark"))
        self.p2_time.pack(pady=40)

        self.p2_btn = tk.Button(self.p2_frame, text="CLICK",
                               font=('Arial', 16, 'bold'),
                               bg=self.get_t("button_inactive"), fg=self.get_t("text_light"),
                               activebackground=self.get_t("button_inactive"),
                               height=3, width=15)
        self.p2_btn.config(command=lambda: self.button_click(2))
        self.p2_btn.pack(pady=25)

        # Controls
        self.controls = tk.Frame(self.root, bg=self.get_t("main_bg"))
        self.controls.pack(pady=15)

        self.pause_btn = tk.Button(self.controls, text="STOP", font=('Arial', 13, 'bold'),
                 command=self.toggle_pause, width=12, height=2,
                 bg=self.get_t("button_stop"), fg=self.get_t("text_light"))
        self.pause_btn.pack(side=tk.LEFT, padx=8)

        self.reset_btn = tk.Button(self.controls, text="RESET", font=('Arial', 13, 'bold'),
                 command=self.reset, width=12, height=2,
                 bg=self.get_t("button_reset"), fg=self.get_t("text_light"))
        self.reset_btn.pack(side=tk.LEFT, padx=8)

        # Bottom footer frame for company and version
        self.footer = tk.Frame(self.root, bg=self.get_t("main_bg"))
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Company name at bottom left
        self.company_label = tk.Label(self.footer, text=f"Powered by {__developer_name__}",
                                font=('Arial', 9), bg=self.get_t("main_bg"),
                                fg=self.get_t("text_muted"))
        self.company_label.pack(side=tk.LEFT, anchor=tk.W)

        # Version number at bottom right
        self.version_label = tk.Label(self.footer, text=f"v{__version__}",
                                font=('Arial', 9), bg=self.get_t("main_bg"),
                                fg=self.get_t("text_muted"))
        self.version_label.pack(side=tk.RIGHT, anchor=tk.E)
    
    def button_click(self, player):
        # Start or switch to the clicked player's clock
        if self.active_player == player and self.running:
            # Already running this clock, do nothing
            return
        
        # Switch to or start this player's clock
        self.active_player = player
        self.running = True
        self.last_update = time.time()
        self.update_buttons()
        
        if not hasattr(self, '_tick_running'):
            self._tick_running = False
        
        if not self._tick_running:
            self._tick_running = True
            self.tick()
    
    def update_buttons(self):
        if self.active_player == 1:
            self.p1_btn.config(text="ACTIVE", bg=self.get_t("button_active"))
            self.p2_btn.config(text="CLICK", bg=self.get_t("button_inactive"))
        elif self.active_player == 2:
            self.p2_btn.config(text="ACTIVE", bg=self.get_t("button_active"))
            self.p1_btn.config(text="CLICK", bg=self.get_t("button_inactive"))
        else:
            self.p1_btn.config(text="CLICK", bg=self.get_t("button_inactive"))
            self.p2_btn.config(text="CLICK", bg=self.get_t("button_inactive"))
    
    def tick(self):
        if not self.running or self.active_player is None:
            self._tick_running = False
            return
        
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now
        
        if self.active_player == 1:
            # Productivity - count down
            self.player1_time -= elapsed
            if self.player1_time <= 0:
                self.player1_time = 0
                self.end_game(2)  # Slack wins
                self._tick_running = False
                return
        else:
            # Slack - count up
            self.player2_time += elapsed
        
        self.display_times()
        self.root.after(100, self.tick)
    
    def display_times(self):
        # Format and display times with hours
        total_seconds1 = int(abs(self.player1_time))
        h1 = total_seconds1 // 3600
        m1 = (total_seconds1 % 3600) // 60
        s1 = total_seconds1 % 60
        self.p1_time.config(text=f"{h1:02d}:{m1:02d}:{s1:02d}")

        total_seconds2 = int(abs(self.player2_time))
        h2 = total_seconds2 // 3600
        m2 = (total_seconds2 % 3600) // 60
        s2 = total_seconds2 % 60
        self.p2_time.config(text=f"{h2:02d}:{m2:02d}:{s2:02d}")

        # Color warnings for Productivity (countdown)
        if self.player1_time < 60:
            self.p1_frame.config(bg=self.get_t("warning_critical"))
            self.p1_time.config(bg=self.get_t("warning_critical"), fg=self.get_t("text_light"))
        elif self.player1_time < 180:
            self.p1_frame.config(bg=self.get_t("warning_medium"))
            self.p1_time.config(bg=self.get_t("warning_medium"), fg=self.get_t("text_light"))
        else:
            self.p1_frame.config(bg=self.get_t("frame_bg"))
            self.p1_time.config(bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))

        # Color warnings for Slack (countup) - changes color as time increases
        if self.player2_time > 1800:  # Over 30 min
            self.p2_frame.config(bg=self.get_t("warning_critical"))
            self.p2_time.config(bg=self.get_t("warning_critical"), fg=self.get_t("text_light"))
        elif self.player2_time > 600:  # Over 10 min
            self.p2_frame.config(bg=self.get_t("warning_medium"))
            self.p2_time.config(bg=self.get_t("warning_medium"), fg=self.get_t("text_light"))
        else:
            self.p2_frame.config(bg=self.get_t("frame_bg"))
            self.p2_time.config(bg=self.get_t("frame_bg"), fg=self.get_t("text_dark"))
    
    def set_time(self, seconds):
        if not self.running:
            self.player1_time = seconds
            self.player2_time = 0  # Slack always starts at 0
            self.display_times()
    
    def set_custom(self):
        try:
            minutes = float(self.custom_entry.get())
            seconds = int(minutes * 60)
            if seconds > 0:
                self.set_time(seconds)
        except ValueError:
            pass
    
    def toggle_pause(self):
        if self.active_player is None:
            return

        self.running = not self.running

        if self.running:
            self.pause_btn.config(text="STOP", bg=self.get_t("button_stop"))
            self.last_update = time.time()
            if not hasattr(self, '_tick_running'):
                self._tick_running = False
            if not self._tick_running:
                self._tick_running = True
                self.tick()
        else:
            self.pause_btn.config(text="RESUME", bg=self.get_t("warning_medium"))
            self._tick_running = False
    
    def reset(self):
        # Stop alarm when resetting
        self.stop_alarm()

        self.running = False
        self.active_player = None
        self.player1_time = 600
        self.player2_time = 0  # Slack resets to 0
        self.pause_btn.config(text="STOP", bg=self.get_t("button_stop"))
        self.update_buttons()
        self.display_times()
    
    def play_alarm_loop(self, alarm_path):
        """Play alarm sound in a loop until stopped"""
        # Get the duration of the sound file (approximate based on file size)
        # For a more responsive stop, we'll use ASYNC and replay it
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
    
    def stop_alarm(self):
        """Stop the looping alarm"""
        self.alarm_playing = False
        # Stop any currently playing sound
        winsound.PlaySound(None, winsound.SND_PURGE)
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join(timeout=1.0)
    
    def end_game(self, winner):
        self.running = False
        self.p1_btn.config(text="GAME OVER", bg=self.get_t("text_muted"))
        self.p2_btn.config(text="GAME OVER", bg=self.get_t("text_muted"))
        
        # Get alarm path
        alarm_path = None
        try:
            # Get the correct directory for both script and .exe
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                script_dir = sys._MEIPASS
            else:
                # Running as script
                script_dir = os.path.dirname(os.path.abspath(__file__))
            
            alarm_path = os.path.join(script_dir, "assets", "media", "alarm.wav")
            
            print(f"Looking for alarm at: {alarm_path}")
            print(f"File exists: {os.path.exists(alarm_path)}")
            
            if os.path.exists(alarm_path):
                file_size = os.path.getsize(alarm_path)
                print(f"File size: {file_size} bytes")
                
                if file_size > 0:
                    # Start looping alarm in a separate thread
                    self.alarm_playing = True
                    self.alarm_thread = threading.Thread(target=self.play_alarm_loop, args=(alarm_path,), daemon=True)
                    self.alarm_thread.start()
                    print("Alarm started in loop")
                else:
                    print("WAV file is empty")
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:
                print("Alarm file not found")
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception as e:
            print(f"Sound error: {e}")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        
        # Show game over popup
        winner_name = self.p1_name.get() if winner == 2 else self.p2_name.get()

        win = tk.Toplevel(self.root)
        win.title("Game Over")
        win.geometry("350x180")
        win.configure(bg=self.get_t("main_bg"))

        # Stop alarm when window is closed
        def on_close():
            self.stop_alarm()
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        tk.Label(win, text=f"Focus Achieved!",
                font=('Arial', 24, 'bold'),
                bg=self.get_t("main_bg"), fg=self.get_t("text_light")).pack(pady=40)
        tk.Button(win, text="Close", command=on_close,
                 font=('Arial', 14), width=10,
                 bg=self.get_t("button_inactive"), fg=self.get_t("text_light")).pack()

def main():
    root = tk.Tk()
    app = ChessClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()