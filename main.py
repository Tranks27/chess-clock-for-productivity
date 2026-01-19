"""Entry point for TrueFocus Timer application."""

import tkinter as tk

from src.themes import ThemeManager
from src.config import load_config, save_config
from src.audio import AlarmPlayer, get_script_dir
from src.ui import UIBuilder
from src.timer import TimerState
from src.stats import StatsTracker  # NEW IMPORT
import os

__version__ = "1.2.0"
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
        self.stats_tracker = StatsTracker()  # NEW: Initialize stats tracker

        # Load theme preference
        theme = load_config(self.theme_manager.themes)
        self.theme_manager.current_theme = theme

        self.root.configure(bg=self.theme_manager.get_color("main_bg"))

        # Create UI
        self.ui = UIBuilder(self.root, __version__, __developer_name__,
                           self.theme_manager, self)
        self.ui.create_all_widgets()

    def _set_window_icon(self):
        """Set window icon from assets."""
        try:
            script_dir = get_script_dir()
            icon_path = os.path.join(script_dir, "assets", "media", "app_icon.ico")

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon loading error: {e}")

    def button_click(self, player):
        """Handle player button click."""
        previous_player = self.timer_state.active_player
        if self.timer_state.start_active_player(player):
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

    def set_time(self, seconds):
        """Set player 1 time."""
        if self.timer_state.set_player1_time(seconds):
            self._display_times()

    def set_custom(self):
        """Set custom time from entry field."""
        try:
            minutes = float(self.ui.custom_entry.get())
            seconds = int(minutes * 60)
            if seconds > 0:
                self.set_time(seconds)
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
        self.ui.update_button_states(None)
        self.ui.set_pause_button_state(False)
        self._display_times()

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.theme_manager.toggle_theme()
        save_config(self.theme_manager.current_theme)
        self.ui.apply_theme()
        self._display_times()

    def stop_alarm(self):
        """Stop the alarm."""
        self.alarm_player.stop_alarm()

    def show_stats(self):
        """Show stats visualization."""
        self.ui.show_stats_window()

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
