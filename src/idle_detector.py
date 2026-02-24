"""Idle detection and automatic Slack timer switch."""

import threading
import time
from pynput import mouse
from src.debug_log import get_debug_logger
from src.config import (
    IDLE_TIMEOUT_SECONDS,
    IDLE_PROMPT_TIMEOUT_SECONDS,
    IDLE_CHECK_INTERVAL_SECONDS,
)


class IdleDetector:
    """Detects when user is idle and prompts to switch to Slack timer."""

    def __init__(self, idle_timeout=IDLE_TIMEOUT_SECONDS, prompt_timeout=IDLE_PROMPT_TIMEOUT_SECONDS):
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
        self.listener = None
        self.idle_callback = None  # Called when idle detected
        self.reset_callback = None  # Called when activity detected
        self.is_enabled_callback = None  # Called to decide if idle checks should run

        self._lock = threading.Lock()
        self._idle_detected = False
        self._idle_dialog_shown = False
        self.logger = get_debug_logger("truefocus.idle")

    def set_callbacks(self, idle_callback=None, reset_callback=None, is_enabled_callback=None):
        """Set callbacks for idle detection and reset events."""
        self.idle_callback = idle_callback
        self.reset_callback = reset_callback
        self.is_enabled_callback = is_enabled_callback

    def start(self):
        """Start monitoring for idle activity."""
        if self.is_running:
            return

        self.is_running = True
        self._idle_detected = False
        self._idle_dialog_shown = False

        # Start mouse listener
        self.listener = mouse.Listener(on_move=self._on_mouse_move)
        self.listener.start()
        self.logger.info(
            "idle-detector-started idle_timeout=%s prompt_timeout=%s",
            self.idle_timeout,
            self.prompt_timeout,
        )

        # Start idle detection thread
        threading.Thread(target=self._detect_idle, daemon=True).start()

    def stop(self):
        """Stop monitoring for idle activity."""
        self.is_running = False
        if self.listener is not None:
            try:
                self.listener.stop()
            except Exception:
                pass
            self.listener = None
        self.logger.info("idle-detector-stopped")

    def _on_mouse_move(self, x, y):
        """Called when mouse moves."""
        if not self.is_running:
            return

        should_call_reset = False
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
                    should_call_reset = True

        # Callbacks run outside lock to avoid lock contention/deadlock risk.
        if should_call_reset and self.reset_callback:
            try:
                self.logger.info("idle-reset-callback-triggered")
                self.reset_callback()
            except Exception:
                self.logger.exception("idle-reset-callback-error")
                pass

    def _detect_idle(self):
        """Monitor for idle periods."""
        while self.is_running:
            time.sleep(IDLE_CHECK_INTERVAL_SECONDS)
            should_trigger_idle = False

            with self._lock:
                if self.is_running:
                    if self.is_enabled_callback and not self.is_enabled_callback():
                        # Idle detection should only run during active productivity tracking.
                        self.last_movement_time = time.time()
                        self._idle_detected = False
                        self._idle_dialog_shown = False
                        continue

                    elapsed = time.time() - self.last_movement_time

                    # Idle detected - show dialog once
                    if elapsed >= self.idle_timeout and not self._idle_dialog_shown:
                        self._idle_detected = True
                        self._idle_dialog_shown = True
                        should_trigger_idle = True
                        self.logger.info("idle-detected elapsed=%.2fs", elapsed)
            if should_trigger_idle and self.idle_callback:
                try:
                    self.idle_callback(self.prompt_timeout)
                except Exception:
                    self.logger.exception("idle-callback-error")
                    pass

    def reset(self):
        """Manually reset idle timer."""
        with self._lock:
            self.last_movement_time = time.time()
            self._idle_detected = False
            self._idle_dialog_shown = False
