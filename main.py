"""Entry point for TrueFocus Timer application."""

import tkinter as tk
from tkinter import messagebox
import threading
import time
import ctypes

from src.themes import ThemeManager
from src.config import load_config, save_config
from src.audio import AlarmPlayer, get_script_dir
from src.ui import UIBuilder
from src.timer import TimerState
from src.stats import StatsTracker
from src.idle_detector import IdleDetector
from src.mini_window import MiniWindowManager
import os

__version__ = "1.3.0"
__developer_name__ = "AYJ Systems"


class ChessClock:
    """Main application controller."""

    def __init__(self, root):
        self.root = root
        self.root.title("TrueFocus Timer")
        self.root.geometry("900x700")

        # Set window icon
        self._set_window_icon()

        # Initialize managers
        self.theme_manager = ThemeManager()
        self.timer_state = TimerState()
        self.alarm_player = AlarmPlayer()
        self.stats_tracker = StatsTracker()
        self.idle_detector = IdleDetector(idle_timeout=300, prompt_timeout=180)

        # Load theme preference
        theme = load_config(self.theme_manager.themes)
        self.theme_manager.current_theme = theme

        self.root.configure(bg=self.theme_manager.get_color("main_bg"))
        self._apply_window_chrome_theme()

        # Create UI
        self.ui = UIBuilder(self.root, __version__, __developer_name__,
                           self.theme_manager, self)
        self.ui.create_all_widgets()

        # Setup idle detector callbacks
        self.idle_detector.set_callbacks(
            idle_callback=self._on_idle_detected,
            reset_callback=self._on_activity_detected
        )
        self.idle_detector.start()

        # Handle window close to stop idle detector
        self.root.protocol("WM_DELETE_WINDOW", self._on_window_close)

        self._idle_prompt_active = False
        self._idle_auto_switch_thread = None
        self._auto_switched_to_slack = False
        self.mini_window_manager = MiniWindowManager(
            root=self.root,
            theme_manager=self.theme_manager,
            timer_state=self.timer_state,
            switch_player_callback=self._switch_clock_from_mini
        )

        # Show a sticky mini timer while the main window is minimized.
        self.root.bind("<Unmap>", self.mini_window_manager.on_root_unmap)
        self.root.bind("<Map>", self.mini_window_manager.on_root_map)
        self.root.bind("<Map>", lambda _e: self.root.after(10, self._apply_window_chrome_theme), add="+")
        self.root.after(10, self._apply_window_chrome_theme)

    def _set_window_icon(self, window=None):
        """Set window icon from assets."""
        if window is None:
            window = self.root
        try:
            for icon_path in self._get_preferred_icon_paths():
                if os.path.exists(icon_path):
                    window.iconbitmap(icon_path)
                    break
        except Exception as e:
            print(f"Icon loading error: {e}")

    def _get_preferred_icon_paths(self):
        """Return icon candidates in priority order."""
        script_dir = get_script_dir()
        media_dir = os.path.join(script_dir, "assets", "media")
        return [
            os.path.join(media_dir, "app_icon_circle.ico"),
        ]

    def button_click(self, player):
        """Handle player button click."""
        previous_player = self.timer_state.active_player
        if self.timer_state.start_active_player(player):
            self.ui.set_pause_button_state(True)
            self.ui.set_time_selection_enabled(False)
            self.ui.update_button_states(self.timer_state.active_player)

            # NEW: Start tracking session when first player clicks
            if self.stats_tracker.current_session is None:
                self.stats_tracker.start_session(self.timer_state.player1_time)

            if player == 2 and self.stats_tracker.current_session is not None:
                self.stats_tracker.current_session["slack_events_count"] += 1
                if previous_player != 2:
                    self.stats_tracker.start_slack_segment()
            elif player == 1 and previous_player == 2:
                self.stats_tracker.end_slack_segment()

            if not self.timer_state._tick_running:
                self.timer_state._tick_running = True
                self.tick()

    def _switch_clock_from_mini(self, player):
        """Switch active clock from the mini window buttons."""
        self.button_click(player)

    def tick(self):
        """Update timer and display."""
        winner = self.timer_state.update_time()

        if winner is not None:
            self.end_game()
            self.timer_state._tick_running = False
            return

        if not self.timer_state.running or self.timer_state.active_player is None:
            self.timer_state._tick_running = False
            return

        # Display times
        self._display_times()

        self.root.after(100, self.tick)

    def _display_times(self):
        """Display formatted times and update warning colors."""
        time1_str = self.timer_state.format_time(self.timer_state.player1_time)
        time2_str = self.timer_state.format_time(self.timer_state.player2_time)

        self.ui.update_player_times(time1_str, time2_str)

        # Update warning colors for player 1 only
        p1_warning = self.timer_state.get_warning_level()
        self.ui.set_frame_warning(self.ui.p1_frame, p1_warning)
        self.mini_window_manager.update()

    def set_time(self, seconds):
        """Set player 1 time."""
        if self.timer_state.set_player1_time(seconds):
            self._display_times()

    def adjust_hours(self, delta):
        """Increment or decrement hours."""
        try:
            current = int(self.ui.custom_hours_entry.get())
            new_value = max(0, current + delta)
            self.ui.custom_hours_entry.delete(0, tk.END)
            self.ui.custom_hours_entry.insert(0, str(new_value))
        except ValueError:
            pass

    def adjust_minutes(self, delta):
        """Increment or decrement minutes."""
        try:
            current = int(self.ui.custom_mins_entry.get())
            new_value = (current + delta) % 60
            self.ui.custom_mins_entry.delete(0, tk.END)
            self.ui.custom_mins_entry.insert(0, f"{new_value:02d}")
        except ValueError:
            pass

    def set_custom(self):
        """Set custom time from entry fields (hours and minutes)."""
        try:
            hours = float(self.ui.custom_hours_entry.get())
            minutes = float(self.ui.custom_mins_entry.get())
            total_seconds = int((hours * 3600) + (minutes * 60))
            if total_seconds > 0:
                self.set_time(total_seconds)
        except ValueError:
            pass

    def toggle_pause(self):
        """Toggle pause/resume."""
        is_running = self.timer_state.toggle_pause()

        if is_running is not False:
            self.ui.set_pause_button_state(is_running)
            if not self.timer_state._tick_running:
                self.timer_state._tick_running = True
                self.tick()

    def reset(self):
        """Reset timer to initial state."""
        self.alarm_player.stop_alarm()

        # NEW: Track reset session before resetting
        if self.stats_tracker.current_session is not None:
            self.stats_tracker.reset_session(self.timer_state.player2_time)

        self.timer_state.reset()
        self.ui.set_time_selection_enabled(True)
        self.ui.update_button_states(None)
        self.ui.set_pause_button_state(True)
        self._display_times()

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.theme_manager.toggle_theme()
        save_config(self.theme_manager.current_theme)
        self._apply_window_chrome_theme()
        self.ui.apply_theme()
        self.mini_window_manager.apply_theme()
        self._display_times()

    def _apply_window_chrome_theme(self):
        """Apply dark/light mode and caption colors to native Windows title bar."""
        try:
            self.root.update_idletasks()
            hwnd = self.root.winfo_id()
            # Tk can return a child handle on some systems; use the top-level parent when available.
            top_hwnd = ctypes.windll.user32.GetParent(hwnd)
            if top_hwnd:
                hwnd = top_hwnd

            is_dark = 1 if self.theme_manager.current_theme == "dark" else 0
            value = ctypes.c_int(is_dark)
            # Windows 10/11 immersive dark caption attribute ids.
            for attr in (20, 19):  # DWMWA_USE_IMMERSIVE_DARK_MODE
                try:
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        ctypes.c_void_p(hwnd),
                        ctypes.c_uint(attr),
                        ctypes.byref(value),
                        ctypes.sizeof(value)
                    )
                except Exception:
                    continue

            # Force caption/text colors so the title bar is not bright white.
            def _hex_to_colorref(hex_color):
                hex_color = hex_color.lstrip("#")
                if len(hex_color) != 6:
                    return None
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return (b << 16) | (g << 8) | r

            def _mix_hex(hex_a, hex_b, ratio=0.5):
                """Mix two #RRGGBB colors; ratio favors second color."""
                a = hex_a.lstrip("#")
                b = hex_b.lstrip("#")
                if len(a) != 6 or len(b) != 6:
                    return hex_a
                ratio = max(0.0, min(1.0, ratio))
                ar, ag, ab = int(a[0:2], 16), int(a[2:4], 16), int(a[4:6], 16)
                br, bg, bb = int(b[0:2], 16), int(b[2:4], 16), int(b[4:6], 16)
                rr = int(ar * (1.0 - ratio) + br * ratio)
                rg = int(ag * (1.0 - ratio) + bg * ratio)
                rb = int(ab * (1.0 - ratio) + bb * ratio)
                return f"#{rr:02x}{rg:02x}{rb:02x}"

            base_bg = self.theme_manager.get_color("main_bg")
            accent_bg = self.theme_manager.get_color("settings_bg")
            # Slight contrast from app body, still within theme palette.
            caption_hex = _mix_hex(base_bg, accent_bg, 0.35)
            border_hex = _mix_hex(base_bg, accent_bg, 0.55)

            caption = _hex_to_colorref(caption_hex)
            border = _hex_to_colorref(border_hex)
            text = _hex_to_colorref(self.theme_manager.get_color("text_dark" if is_dark else "text_light"))

            if caption is not None:
                cap_val = ctypes.c_uint(caption)
                try:
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        ctypes.c_void_p(hwnd),
                        ctypes.c_uint(35),  # DWMWA_CAPTION_COLOR
                        ctypes.byref(cap_val),
                        ctypes.sizeof(cap_val)
                    )
                except Exception:
                    pass

            if border is not None:
                border_val = ctypes.c_uint(border)
                for attr in (34,):  # DWMWA_BORDER_COLOR
                    try:
                        ctypes.windll.dwmapi.DwmSetWindowAttribute(
                            ctypes.c_void_p(hwnd),
                            ctypes.c_uint(attr),
                            ctypes.byref(border_val),
                            ctypes.sizeof(border_val)
                        )
                    except Exception:
                        continue

            if text is not None:
                text_val = ctypes.c_uint(text)
                try:
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        ctypes.c_void_p(hwnd),
                        ctypes.c_uint(36),  # DWMWA_TEXT_COLOR
                        ctypes.byref(text_val),
                        ctypes.sizeof(text_val)
                    )
                except Exception:
                    pass
        except Exception:
            pass

    def stop_alarm(self):
        """Stop the alarm."""
        self.alarm_player.stop_alarm()

    def show_stats(self):
        """Show stats visualization."""
        self.ui.show_stats_window()

    def _on_idle_detected(self, timeout_seconds):
        """Handle idle detection - prompt user to switch to Slack."""
        if self._idle_prompt_active or self.timer_state.active_player == 2:
            return  # Already on Slack or dialog already shown

        self._idle_prompt_active = True
        self._auto_switched_to_slack = False
        idle_dialog = None

        def show_idle_prompt():
            """Show the idle detection dialog in the main thread."""
            nonlocal idle_dialog

            idle_dialog = tk.Toplevel(self.root)
            idle_dialog.title("Idle Detected")
            idle_dialog.geometry("350x170")
            idle_dialog.transient(self.root)
            idle_dialog.grab_set()

            # Center the dialog
            idle_dialog.update_idletasks()
            x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (idle_dialog.winfo_width() // 2)
            y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (idle_dialog.winfo_height() // 2)
            idle_dialog.geometry(f"+{x}+{y}")

            # Message label
            message = tk.Label(
                idle_dialog,
                text=f"No mouse movement for 5 minutes.\n\nSwitch to Slack timer?\n\n(Auto-switching in {timeout_seconds} seconds if no response)",
                wraplength=320,
                justify=tk.CENTER
            )
            message.pack(pady=15)

            # Buttons frame
            button_frame = tk.Frame(idle_dialog)
            button_frame.pack(pady=10)

            def on_yes():
                """User clicked Yes."""
                nonlocal idle_dialog
                self._idle_prompt_active = False
                if idle_dialog:
                    try:
                        idle_dialog.destroy()
                    except:
                        pass
                self.button_click(2)  # Switch to Slack timer

            def on_no():
                """User clicked No - wait for auto-switch timeout."""
                nonlocal idle_dialog
                if idle_dialog:
                    try:
                        idle_dialog.destroy()
                    except:
                        pass

            yes_btn = tk.Button(button_frame, text="Yes", command=on_yes, width=8)
            yes_btn.pack(side=tk.LEFT, padx=5)

            no_btn = tk.Button(button_frame, text="No", command=on_no, width=8)
            no_btn.pack(side=tk.LEFT, padx=5)

        # Show dialog in main thread
        self.root.after(0, show_idle_prompt)

        # Start auto-switch timer in background thread
        def auto_switch_after_timeout():
            """Auto-switch to Slack after timeout if user didn't respond."""
            for _ in range(timeout_seconds):
                if not self._idle_prompt_active:
                    return  # User already responded
                time.sleep(1)

            # Auto-switch to Slack - close dialog and switch
            if self._idle_prompt_active:
                self._idle_prompt_active = False
                self._auto_switched_to_slack = True

                # Close the idle dialog if it exists
                def close_and_switch():
                    nonlocal idle_dialog
                    if idle_dialog:
                        try:
                            idle_dialog.destroy()
                        except:
                            pass

                    # Switch to Slack timer
                    self.button_click(2)

                    # Show confirmation popup
                    messagebox.showinfo(
                        "Auto-Switched to Slack",

                        "AFK detected!!!ðŸ‘€\nSwitched to Slack and started tracking.\n\n" \
                        "Jump back to the Main timer when youâ€™re ready."
                    )
                self.root.after(0, close_and_switch)

        self._idle_auto_switch_thread = threading.Thread(
            target=auto_switch_after_timeout,
            daemon=True
        )
        self._idle_auto_switch_thread.start()

    def _on_activity_detected(self):
        """Handle activity detection - user moved mouse after being idle."""
        if self._idle_prompt_active:
            self._idle_prompt_active = False

    def _on_window_close(self):
        """Handle window close event."""
        self.idle_detector.stop()
        self.mini_window_manager.destroy()
        self.root.destroy()

    def end_game(self):
        """Handle game end."""
        self.timer_state.running = False
        
        # NEW: Track completed session
        if self.stats_tracker.current_session is not None:
            self.stats_tracker.end_session(self.timer_state.player2_time, outcome="completed")
        
        self.ui.p1_btn.config(
            text="GAME OVER",
            bg=self.theme_manager.get_color("text_muted")
        )
        self.ui.p2_btn.config(
            text="GAME OVER",
            bg=self.theme_manager.get_color("text_muted")
        )

        # Start alarm
        alarm_path = self.alarm_player.get_alarm_path()

        try:
            print(f"Looking for alarm at: {alarm_path}")
            print(f"File exists: {os.path.exists(alarm_path)}")

            if os.path.exists(alarm_path):
                file_size = os.path.getsize(alarm_path)
                print(f"File size: {file_size} bytes")

                if file_size > 0:
                    self.alarm_player.start_alarm(alarm_path)
                    print("Alarm started in loop")
                else:
                    print("WAV file is empty")
                    self.alarm_player.play_error_sound()
            else:
                print("Alarm file not found")
                self.alarm_player.play_error_sound()
        except Exception as e:
            print(f"Sound error: {e}")
            self.alarm_player.play_error_sound()

        # Show game over popup
        self.ui.show_game_over_popup("")


def main():
    """Start the application."""
    root = tk.Tk()
    ChessClock(root)
    root.mainloop()


if __name__ == "__main__":
    main()

