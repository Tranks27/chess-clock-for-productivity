"""Timer logic and state management for TrueFocus Timer."""

import time
from src.config import DEFAULT_RESET_TIME


class TimerState:
    """Manages timer state and time values."""

    def __init__(self, initial_player1_time=DEFAULT_RESET_TIME):
        # Time variables (in seconds)
        self.player1_time = initial_player1_time  # Productivity - counts down
        self.player2_time = 0  # Slack - counts up
        self.active_player = None
        self.running = False
        self.last_update = None
        self._tick_running = False

    def reset(self, initial_player1_time=DEFAULT_RESET_TIME):
        """Reset timer to initial state."""
        self.player1_time = initial_player1_time
        self.player2_time = 0
        self.active_player = None
        self.running = False
        self.last_update = None
        self._tick_running = False

    def start_active_player(self, player):
        """Start or switch to the active player."""
        if self.active_player == player and self.running:
            return False  # Already running this clock

        self.active_player = player
        self.running = True
        self.last_update = time.time()
        return True

    def toggle_pause(self):
        """Toggle pause state."""
        if self.active_player is None:
            return False

        self.running = not self.running
        if self.running:
            self.last_update = time.time()
        return self.running

    def update_time(self):
        """Update timer values based on elapsed time."""
        if not self.running or self.active_player is None:
            return None

        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now

        if self.active_player == 1:
            # Productivity - count down
            self.player1_time -= elapsed
            if self.player1_time <= 0:
                self.player1_time = 0
                return 2  # Slack wins

        else:
            # Slack - count up
            self.player2_time += elapsed

        return None

    def set_player1_time(self, seconds):
        """Set player 1 time (only when not running)."""
        if not self.running:
            self.player1_time = seconds
            self.player2_time = 0
            return True
        return False

    def format_time(self, total_seconds):
        """Format seconds to HH:MM:SS string."""
        total_seconds = int(abs(total_seconds))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_warning_level(self):
        """Get warning level for player 1 (productivity countdown).

        Returns:
            str or None: warning level - None (normal), 'medium', 'critical'
        """
        if self.player1_time < 60:
            return "critical"
        elif self.player1_time < 180:
            return "medium"
        return None
