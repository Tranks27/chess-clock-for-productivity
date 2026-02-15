"""Idle detection and automatic Slack timer switch."""

import threading
import time
from datetime import datetime
from pynput import mouse


class IdleDetector:
    """Detects when user is idle and prompts to switch to Slack timer."""

    def __init__(self, idle_timeout=300, prompt_timeout=180):
        """
        Initialize idle detector.

        Args:
            idle_timeout: Seconds of no mouse movement before prompting (default 5 min)
            prompt_timeout: Seconds user has to respond before auto-switching (default 3 min)
        """
        self.idle_timeout = idle_timeout  # 5 minutes
        self.prompt_timeout = prompt_timeout  # 3 minutes

        self.last_mouse_position = None
        self.last_movement_time = time.time()
        self.is_running = False
        self.detector_thread = None
        self.idle_callback = None  # Called when idle detected
        self.reset_callback = None  # Called when activity detected

        self._lock = threading.Lock()
        self._idle_detected = False
        self._idle_dialog_shown = False

    def set_callbacks(self, idle_callback=None, reset_callback=None):
        """Set callbacks for idle detection and reset events."""
        self.idle_callback = idle_callback
        self.reset_callback = reset_callback

    def start(self):
        """Start monitoring for idle activity."""
        if self.is_running:
            return

        self.is_running = True
        self._idle_detected = False
        self._idle_dialog_shown = False

        # Start mouse listener
        listener = mouse.Listener(on_move=self._on_mouse_move)
        listener.start()

        # Start idle detection thread
        self.detector_thread = threading.Thread(target=self._detect_idle, daemon=True)
        self.detector_thread.start()

    def stop(self):
        """Stop monitoring for idle activity."""
        self.is_running = False

    def _on_mouse_move(self, x, y):
        """Called when mouse moves."""
        if not self.is_running:
            return

        with self._lock:
            current_pos = (x, y)

            # Check if position actually changed
            if self.last_mouse_position != current_pos:
                self.last_mouse_position = current_pos
                self.last_movement_time = time.time()

                # Reset idle state if was idle
                if self._idle_detected:
                    self._idle_detected = False
                    self._idle_dialog_shown = False
                    if self.reset_callback:
                        self.reset_callback()

    def _detect_idle(self):
        """Monitor for idle periods."""
        while self.is_running:
            time.sleep(1)

            with self._lock:
                if self.is_running:
                    elapsed = time.time() - self.last_movement_time

                    # Idle detected - show dialog once
                    if elapsed >= self.idle_timeout and not self._idle_dialog_shown:
                        self._idle_detected = True
                        self._idle_dialog_shown = True

                        if self.idle_callback:
                            self.idle_callback(self.prompt_timeout)

    def reset(self):
        """Manually reset idle timer."""
        with self._lock:
            self.last_movement_time = time.time()
            self._idle_detected = False
            self._idle_dialog_shown = False
