"""UI/widget creation for TrueFocus Timer."""

import tkinter as tk


class UIBuilder:
    """Builds and manages UI widgets."""

    def __init__(self, root, version, developer_name, theme_manager, clock_app):
        self.root = root
        self.version = version
        self.developer_name = developer_name
        self.theme_manager = theme_manager
        self.clock_app = clock_app

    def get_t(self, key):
        """Get a color value from the current theme."""
        return self.theme_manager.get_color(key)

    def create_all_widgets(self):
        """Create all UI widgets."""
        self.create_title()
        self.create_settings()
        self.create_clocks()
        self.create_controls()
        self.create_footer()

    def create_title(self):
        """Create title widget."""
        self.title_widget = tk.Label(
            self.root,
            text="TrueFocus Timer",
            font=('Arial', 24, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )
        self.title_widget.pack(pady=15)

    def create_settings(self):
        """Create settings frame with time controls."""
        self.settings = tk.Frame(
            self.root,
            bg=self.get_t("settings_bg"),
            relief=tk.RAISED,
            bd=2
        )
        self.settings.pack(pady=10, padx=20, fill=tk.X)

        # Time label
        self.settings_time_label = tk.Label(
            self.settings,
            text="Time:",
            font=('Arial', 11),
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.settings_time_label.pack(side=tk.LEFT, padx=10)

        # 1 hour button
        self.time_btn_1hr = tk.Button(
            self.settings,
            text="1 hour",
            width=8,
            command=lambda: self.clock_app.set_time(3600),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.time_btn_1hr.pack(side=tk.LEFT, padx=3)

        # 2 hour button
        self.time_btn_2hr = tk.Button(
            self.settings,
            text="2 hour",
            width=8,
            command=lambda: self.clock_app.set_time(7200),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.time_btn_2hr.pack(side=tk.LEFT, padx=3)

        # Custom time label
        self.custom_label = tk.Label(
            self.settings,
            text="Custom (min):",
            font=('Arial', 11),
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.custom_label.pack(side=tk.LEFT, padx=(15, 5))

        # Custom time entry
        self.custom_entry = tk.Entry(
            self.settings,
            width=8,
            font=('Arial', 11),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.custom_entry.pack(side=tk.LEFT, padx=3)

        # Custom time button
        self.custom_btn = tk.Button(
            self.settings,
            text="Set",
            width=6,
            command=self.clock_app.set_custom,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.custom_btn.pack(side=tk.LEFT, padx=3)

        # Theme toggle button (right side)
        self.theme_toggle_btn = tk.Button(
            self.settings,
            text=self.theme_manager.get_theme_icon(),
            font=('Arial', 11),
            width=4,
            height=1,
            command=self.clock_app.toggle_theme,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.theme_toggle_btn.pack(side=tk.RIGHT, padx=10)

    def create_clocks(self):
        """Create player clock frames."""
        self.clocks = tk.Frame(
            self.root,
            bg=self.get_t("main_bg")
        )
        self.clocks.pack(pady=25, expand=True, fill=tk.BOTH)

        # Player 1 (Productivity)
        self.p1_frame = tk.Frame(
            self.clocks,
            bg=self.get_t("frame_bg"),
            relief=tk.RAISED,
            bd=4
        )
        self.p1_frame.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.BOTH)

        self.p1_name = tk.Entry(
            self.p1_frame,
            font=('Arial', 16, 'bold'),
            justify='center',
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark"),
            relief=tk.FLAT
        )
        self.p1_name.insert(0, "Productivity")
        self.p1_name.pack(pady=15)

        self.p1_time = tk.Label(
            self.p1_frame,
            text="00:10:00",
            font=('Arial', 56, 'bold'),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p1_time.pack(pady=40)

        self.p1_btn = tk.Button(
            self.p1_frame,
            text="CLICK",
            font=('Arial', 16, 'bold'),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            height=3,
            width=15,
            command=lambda: self.clock_app.button_click(1)
        )
        self.p1_btn.pack(pady=25)

        # Player 2 (Slack)
        self.p2_frame = tk.Frame(
            self.clocks,
            bg=self.get_t("frame_bg"),
            relief=tk.RAISED,
            bd=4
        )
        self.p2_frame.pack(side=tk.RIGHT, padx=15, expand=True, fill=tk.BOTH)

        self.p2_name = tk.Entry(
            self.p2_frame,
            font=('Arial', 16, 'bold'),
            justify='center',
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark"),
            relief=tk.FLAT
        )
        self.p2_name.insert(0, "Slack")
        self.p2_name.pack(pady=15)

        self.p2_time = tk.Label(
            self.p2_frame,
            text="00:00:00",
            font=('Arial', 56, 'bold'),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p2_time.pack(pady=40)

        self.p2_btn = tk.Button(
            self.p2_frame,
            text="CLICK",
            font=('Arial', 16, 'bold'),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            height=3,
            width=15,
            command=lambda: self.clock_app.button_click(2)
        )
        self.p2_btn.pack(pady=25)

    def create_controls(self):
        """Create control buttons."""
        self.controls = tk.Frame(
            self.root,
            bg=self.get_t("main_bg")
        )
        self.controls.pack(pady=15)

        self.pause_btn = tk.Button(
            self.controls,
            text="STOP",
            font=('Arial', 13, 'bold'),
            command=self.clock_app.toggle_pause,
            width=12,
            height=2,
            bg=self.get_t("button_stop"),
            fg=self.get_t("text_light")
        )
        self.pause_btn.pack(side=tk.LEFT, padx=8)

        self.reset_btn = tk.Button(
            self.controls,
            text="RESET",
            font=('Arial', 13, 'bold'),
            command=self.clock_app.reset,
            width=12,
            height=2,
            bg=self.get_t("button_reset"),
            fg=self.get_t("text_light")
        )
        self.reset_btn.pack(side=tk.LEFT, padx=8)

    def create_footer(self):
        """Create footer with company and version info."""
        self.footer = tk.Frame(
            self.root,
            bg=self.get_t("main_bg")
        )
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.company_label = tk.Label(
            self.footer,
            text=f"Powered by {self.developer_name}",
            font=('Arial', 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_muted")
        )
        self.company_label.pack(side=tk.LEFT, anchor=tk.W)

        self.version_label = tk.Label(
            self.footer,
            text=f"v{self.version}",
            font=('Arial', 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_muted")
        )
        self.version_label.pack(side=tk.RIGHT, anchor=tk.E)

    def apply_theme(self):
        """Apply the current theme to all widgets."""
        # Main window
        self.root.configure(bg=self.get_t("main_bg"))

        # Title
        self.title_widget.config(
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )

        # Settings frame
        self.settings.config(bg=self.get_t("settings_bg"))
        self.settings_time_label.config(
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.time_btn_1hr.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.time_btn_2hr.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.custom_label.config(
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.custom_entry.config(
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.custom_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.theme_toggle_btn.config(
            text=self.theme_manager.get_theme_icon(),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )

        # Clocks frame
        self.clocks.config(bg=self.get_t("main_bg"))

        # Player 1
        self.p1_frame.config(bg=self.get_t("frame_bg"))
        self.p1_name.config(
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p1_time.config(
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p1_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive")
        )

        # Player 2
        self.p2_frame.config(bg=self.get_t("frame_bg"))
        self.p2_name.config(
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p2_time.config(
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p2_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive")
        )

        # Controls
        self.controls.config(bg=self.get_t("main_bg"))
        self.pause_btn.config(
            bg=self.get_t("button_stop"),
            fg=self.get_t("text_light")
        )
        self.reset_btn.config(
            bg=self.get_t("button_reset"),
            fg=self.get_t("text_light")
        )

        # Footer
        self.footer.config(bg=self.get_t("main_bg"))
        self.company_label.config(
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_muted")
        )
        self.version_label.config(
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_muted")
        )

    def update_player_times(self, time1_str, time2_str):
        """Update displayed times for both players."""
        self.p1_time.config(text=time1_str)
        self.p2_time.config(text=time2_str)

    def update_button_states(self, active_player):
        """Update button states based on active player."""
        if active_player == 1:
            self.p1_btn.config(
                text="ACTIVE",
                bg=self.get_t("button_active")
            )
            self.p2_btn.config(
                text="CLICK",
                bg=self.get_t("button_inactive")
            )
        elif active_player == 2:
            self.p2_btn.config(
                text="ACTIVE",
                bg=self.get_t("button_active")
            )
            self.p1_btn.config(
                text="CLICK",
                bg=self.get_t("button_inactive")
            )
        else:
            self.p1_btn.config(
                text="CLICK",
                bg=self.get_t("button_inactive")
            )
            self.p2_btn.config(
                text="CLICK",
                bg=self.get_t("button_inactive")
            )

    def set_frame_warning(self, frame, warning_type):
        """Set frame background color based on warning type."""
        if warning_type == "critical":
            bg_color = self.get_t("warning_critical")
            text_color = self.get_t("text_light")
        elif warning_type == "medium":
            bg_color = self.get_t("warning_medium")
            text_color = self.get_t("text_light")
        else:
            bg_color = self.get_t("frame_bg")
            text_color = self.get_t("text_dark")

        frame.config(bg=bg_color)
        if frame == self.p1_frame:
            self.p1_time.config(bg=bg_color, fg=text_color)
        else:
            self.p2_time.config(bg=bg_color, fg=text_color)

    def set_pause_button_state(self, is_running):
        """Update pause button appearance based on running state."""
        if is_running:
            self.pause_btn.config(
                text="STOP",
                bg=self.get_t("button_stop")
            )
        else:
            self.pause_btn.config(
                text="RESUME",
                bg=self.get_t("warning_medium")
            )

    def show_game_over_popup(self, winner_name):
        """Show game over popup window."""
        win = tk.Toplevel(self.root)
        win.title("Game Over")
        win.geometry("350x180")
        win.configure(bg=self.get_t("main_bg"))

        def on_close():
            self.clock_app.stop_alarm()
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

        tk.Label(
            win,
            text="Focus Achieved!",
            font=('Arial', 24, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        ).pack(pady=40)

        tk.Button(
            win,
            text="Close",
            command=on_close,
            font=('Arial', 14),
            width=10,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        ).pack()
