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

        self.stats_btn = tk.Button(
            self.controls,
            text="STATS",
            font=('Arial', 13, 'bold'),
            command=self.clock_app.show_stats,
            width=12,
            height=2,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.stats_btn.pack(side=tk.LEFT, padx=8)

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
        self.stats_btn.config(
            bg=self.get_t("button_inactive"),
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

    def show_stats_window(self):
        """Show stats visualization window."""
        win = tk.Toplevel(self.root)
        win.title("Today's Stats")
        win.geometry("900x620")
        win.configure(bg=self.get_t("main_bg"))

        sessions = self.clock_app.stats_tracker.get_sessions_with_metrics()
        today_sessions = self._get_today_sessions(sessions)

        header = tk.Frame(win, bg=self.get_t("main_bg"))
        header.pack(fill=tk.X, padx=20, pady=(16, 8))

        title = tk.Label(
            header,
            text="Today",
            font=('Arial', 20, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )
        title.pack(side=tk.LEFT)

        tk.Button(
            header,
            text="Close",
            command=win.destroy,
            font=('Arial', 11),
            width=8,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        ).pack(side=tk.RIGHT)

        headline_row = tk.Frame(win, bg=self.get_t("main_bg"))
        headline_row.pack(fill=tk.X, padx=20, pady=(0, 10))
        self._render_headline_metrics(headline_row, today_sessions)

        insight_row = tk.Frame(win, bg=self.get_t("main_bg"))
        insight_row.pack(fill=tk.X, padx=20, pady=(0, 10))
        self._render_insights(insight_row, today_sessions)

        table_container = tk.Frame(win, bg=self.get_t("main_bg"))
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))
        self._render_session_table(table_container, today_sessions)

    def _get_today_sessions(self, sessions):
        """Filter sessions to today by local date."""
        from datetime import datetime

        today = datetime.now().date()
        today_sessions = []
        for session in sessions:
            start = session.get("start_time")
            if not start:
                continue
            try:
                start_dt = datetime.fromisoformat(start)
            except ValueError:
                continue
            if start_dt.date() == today:
                today_sessions.append(session)
        return today_sessions

    def _render_headline_metrics(self, parent, sessions):
        """Render the top-row headline metrics for today."""
        planned = sum(s.get("initial_productivity_time", 0) for s in sessions)
        actual = sum(s.get("actual_focus_time", 0) for s in sessions)
        slack = sum(s.get("total_slack_time", 0) for s in sessions)
        slack_ratio_total = (slack / (actual + slack)) if (actual + slack) else 0
        efficiency = self._calculate_efficiency(slack_ratio_total)

        cards = [
            ("Planned Focus", self._format_seconds(planned)),
            ("Actual Focus", self._format_seconds(actual)),
            ("Slack (Interruptions)", self._format_seconds(slack)),
            ("Focus Efficiency", f"{efficiency * 100:.0f}%")
        ]

        for label, value in cards:
            card = tk.Frame(
                parent,
                bg=self.get_t("frame_bg"),
                relief=tk.RAISED,
                bd=2
            )
            card.pack(side=tk.LEFT, padx=6, ipadx=12, ipady=8)

            tk.Label(
                card,
                text=label,
                font=('Arial', 9),
                bg=self.get_t("frame_bg"),
                fg=self.get_t("text_muted")
            ).pack()

            tk.Label(
                card,
                text=value,
                font=('Arial', 15, 'bold'),
                bg=self.get_t("frame_bg"),
                fg=self.get_t("text_light")
            ).pack()

    def _render_insights(self, parent, sessions):
        """Render behavioral insights for today."""
        total_slack = sum(s.get("total_slack_time", 0) for s in sessions)
        avg_slack = (total_slack / len(sessions)) if sessions else 0

        most_disrupted = None
        max_ratio = -1
        for session in sessions:
            ratio = session.get("slack_ratio", 0)
            if ratio > max_ratio:
                max_ratio = ratio
                most_disrupted = session

        longest_interrupt = None
        longest_duration = None
        for session in sessions:
            for seg in session.get("slack_segments", []):
                duration = seg.get("duration_seconds")
                if duration is None:
                    continue
                if longest_duration is None or duration > longest_duration:
                    longest_duration = duration
                    longest_interrupt = duration

        items = [
            ("Sessions", str(len(sessions))),
            ("Avg Slack / Session", self._format_seconds(avg_slack)),
            ("Most Disrupted", self._format_most_disrupted(most_disrupted, max_ratio)),
        ]

        if longest_interrupt is not None:
            items.insert(0, ("Longest Interruption", self._format_seconds(longest_interrupt)))

        for label, value in items:
            card = tk.Frame(
                parent,
                bg=self.get_t("settings_bg"),
                relief=tk.RAISED,
                bd=1
            )
            card.pack(side=tk.LEFT, padx=6, ipadx=10, ipady=6)

            tk.Label(
                card,
                text=label,
                font=('Arial', 9),
                bg=self.get_t("settings_bg"),
                fg=self.get_t("text_muted")
            ).pack()

            tk.Label(
                card,
                text=value,
                font=('Arial', 12, 'bold'),
                bg=self.get_t("settings_bg"),
                fg=self.get_t("text_light")
            ).pack()

    def _render_session_table(self, parent, sessions):
        """Render today's session table."""
        container = tk.Frame(parent, bg=self.get_t("frame_bg"), bd=2, relief=tk.RAISED)
        container.pack(fill=tk.BOTH, expand=True)

        header = tk.Frame(container, bg=self.get_t("frame_bg"))
        header.pack(fill=tk.X, padx=12, pady=(10, 6))

        tk.Label(
            header,
            text="Sessions Today",
            font=('Arial', 12, 'bold'),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        ).pack(side=tk.LEFT)

        table = tk.Frame(container, bg=self.get_t("frame_bg"))
        table.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        columns = ["Start", "Planned", "Slack", "Slack %", "Actual", "Efficiency", "Outcome"]
        widths = [10, 12, 10, 9, 12, 11, 12]

        for idx, col in enumerate(columns):
            tk.Label(
                table,
                text=col,
                font=('Arial', 9, 'bold'),
                bg=self.get_t("frame_bg"),
                fg=self.get_t("text_muted"),
                width=widths[idx],
                anchor=tk.W
            ).grid(row=0, column=idx, sticky="w", pady=(0, 6))

        if not sessions:
            tk.Label(
                table,
                text="No sessions yet today.",
                font=('Arial', 10),
                bg=self.get_t("frame_bg"),
                fg=self.get_t("text_dark")
            ).grid(row=1, column=0, columnspan=len(columns), sticky="w")
            return

        from datetime import datetime
        for row_idx, session in enumerate(sessions, start=1):
            start_time = session.get("start_time")
            try:
                start_dt = datetime.fromisoformat(start_time) if start_time else None
                start_label = start_dt.strftime("%H:%M") if start_dt else "--:--"
            except ValueError:
                start_label = "--:--"

            planned = self._format_seconds(session.get("initial_productivity_time", 0))
            slack = self._format_seconds(session.get("total_slack_time", 0))
            actual = self._format_seconds(session.get("actual_focus_time", 0))
            slack_ratio = session.get("slack_ratio", 0)
            efficiency = self._calculate_efficiency(slack_ratio)
            efficiency_label = f"{efficiency * 100:.0f}%"
            slack_label = f"{slack_ratio * 100:.0f}%"
            raw_outcome = session.get("outcome", "unknown")
            outcome = raw_outcome.replace("_", " ").title()

            values = [start_label, planned, slack, slack_label, actual, efficiency_label, outcome]

            for col_idx, value in enumerate(values):
                tk.Label(
                    table,
                    text=value,
                    font=('Arial', 10),
                    bg=self.get_t("frame_bg"),
                    fg=self.get_t("warning_medium") if raw_outcome == "reset_early" else self.get_t("text_dark"),
                    width=widths[col_idx],
                    anchor=tk.W
                ).grid(row=row_idx, column=col_idx, sticky="w")

    def _format_signed_seconds(self, total_seconds):
        """Format seconds with a sign for overrun values."""
        sign = "-" if total_seconds < 0 else "+"
        return f"{sign}{self._format_seconds(abs(total_seconds))}"

    def _format_most_disrupted(self, session, ratio):
        """Format the most disrupted session label."""
        if not session:
            return "--"
        from datetime import datetime

        start_time = session.get("start_time")
        try:
            start_dt = datetime.fromisoformat(start_time) if start_time else None
            start_label = start_dt.strftime("%H:%M") if start_dt else "--:--"
        except ValueError:
            start_label = "--:--"
        return f"{start_label} ({ratio * 100:.0f}%)"

    def _calculate_efficiency(self, slack_ratio):
        """Compute focus efficiency from slack ratio."""
        return max(0, 1 - slack_ratio)

    def _format_seconds(self, total_seconds):
        """Format seconds to H:MM:SS."""
        total_seconds = int(abs(total_seconds))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:d}:{minutes:02d}:{seconds:02d}"
