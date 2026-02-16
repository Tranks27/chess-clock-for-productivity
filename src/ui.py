"""UI/widget creation for TrueFocus Timer."""

import io
import os
import tkinter as tk

from src.audio import get_script_dir

try:
    import cairosvg
except ImportError:
    cairosvg = None

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class UIBuilder:
    """Builds and manages UI widgets."""

    def __init__(self, root, version, developer_name, theme_manager, clock_app):
        self.root = root
        self.version = version
        self.developer_name = developer_name
        self.theme_manager = theme_manager
        self.clock_app = clock_app
        self.stats_btn_icon = None
        self.theme_light_icon = None
        self.theme_dark_icon = None
        self.font_family = "Bahnschrift"

    def get_t(self, key):
        """Get a color value from the current theme."""
        return self.theme_manager.get_color(key)

    def _load_svg_icon(self, filename, size=18):
        """Load an SVG icon from assets/media as a Tk image."""
        media_dir = os.path.join(get_script_dir(), "assets", "media")
        icon_path = os.path.join(media_dir, filename)
        if not os.path.exists(icon_path):
            return None

        if cairosvg is None or Image is None or ImageTk is None:
            print(f"SVG icon requires cairosvg + Pillow: {filename}")
            return None

        try:
            png_bytes = cairosvg.svg2png(
                url=icon_path,
                output_width=size,
                output_height=size,
            )
            image = Image.open(io.BytesIO(png_bytes))
            return ImageTk.PhotoImage(image)
        except Exception as err:
            print(f"SVG icon render error ({filename}): {err}")
            return None

        return None

    def _load_stats_icon(self, size=18):
        """Load stats icon image."""
        return self._load_svg_icon("stats_icon.svg", size=size)

    def _get_theme_button_icon(self):
        """Return the icon matching the current theme."""
        if self.theme_manager.current_theme == "dark":
            return self.theme_light_icon
        return self.theme_dark_icon

    def create_all_widgets(self):
        """Create all UI widgets."""
        self.create_title()
        self.create_settings()
        self.create_clocks()
        self.create_controls()
        self.create_footer()

    def create_title(self):
        """Create title widget."""
        self.title_row = tk.Frame(
            self.root,
            bg=self.get_t("main_bg")
        )
        self.title_row.pack(fill=tk.X, padx=24, pady=(12, 6))

        self.title_widget = tk.Label(
            self.title_row,
            text="TrueFocus Timer",
            font=(self.font_family, 30, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("title_text")
        )
        self.title_widget.pack(side=tk.LEFT)

        self.title_subtitle = tk.Label(
            self.title_row,
            text="WORK x SLACK",
            font=(self.font_family, 10, "bold"),
            bg=self.get_t("main_bg"),
            fg=self.get_t("button_inactive")
        )
        self.title_subtitle.pack(side=tk.RIGHT, pady=(12, 0))

    def create_settings(self):
        """Create settings frame with time controls."""
        self.settings = tk.Frame(
            self.root,
            bg=self.get_t("settings_bg"),
            relief=tk.RIDGE,
            bd=2
        )
        self.settings.pack(pady=10, padx=24, fill=tk.X)

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
            text="Custom:",
            font=('Arial', 11),
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.custom_label.pack(side=tk.LEFT, padx=(15, 5))

        # Hours minus button
        self.hours_minus_btn = tk.Button(
            self.settings,
            text="-",
            width=2,
            font=('Arial', 9),
            command=lambda: self.clock_app.adjust_hours(-1),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.hours_minus_btn.pack(side=tk.LEFT, padx=1)

        # Custom hours entry
        self.custom_hours_entry = tk.Entry(
            self.settings,
            width=3,
            font=('Arial', 11),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark"),
            justify='center'
        )
        self.custom_hours_entry.insert(0, "1")
        self.custom_hours_entry.pack(side=tk.LEFT, padx=2)

        # Hours plus button
        self.hours_plus_btn = tk.Button(
            self.settings,
            text="+",
            width=2,
            font=('Arial', 9),
            command=lambda: self.clock_app.adjust_hours(1),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.hours_plus_btn.pack(side=tk.LEFT, padx=1)

        # Hours label
        self.hours_label = tk.Label(
            self.settings,
            text="h",
            font=('Arial', 11),
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.hours_label.pack(side=tk.LEFT, padx=5)

        # Minutes minus button
        self.mins_minus_btn = tk.Button(
            self.settings,
            text="-",
            width=2,
            font=('Arial', 9),
            command=lambda: self.clock_app.adjust_minutes(-1),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.mins_minus_btn.pack(side=tk.LEFT, padx=1)

        # Custom minutes entry
        self.custom_mins_entry = tk.Entry(
            self.settings,
            width=3,
            font=('Arial', 11),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark"),
            justify='center'
        )
        self.custom_mins_entry.insert(0, "00")
        self.custom_mins_entry.pack(side=tk.LEFT, padx=2)

        # Minutes plus button
        self.mins_plus_btn = tk.Button(
            self.settings,
            text="+",
            width=2,
            font=('Arial', 9),
            command=lambda: self.clock_app.adjust_minutes(1),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        )
        self.mins_plus_btn.pack(side=tk.LEFT, padx=1)

        # Minutes label
        self.mins_label = tk.Label(
            self.settings,
            text="m",
            font=('Arial', 11),
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.mins_label.pack(side=tk.LEFT, padx=5)

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
        self.theme_light_icon = self._load_svg_icon("light.svg", size=30)
        self.theme_dark_icon = self._load_svg_icon("dark.svg", size=30)
        theme_icon = self._get_theme_button_icon()
        self.theme_toggle_btn = tk.Button(
            self.settings,
            text="" if theme_icon is not None else self.theme_manager.get_theme_icon(),
            image=theme_icon,
            compound=tk.CENTER,
            font=('Arial', 11),
            command=self.clock_app.toggle_theme,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=2,
            highlightthickness=1,
            padx=2,
            pady=0
        )
        self.theme_toggle_btn.pack(side=tk.RIGHT, padx=10)

        # Stats button (top-right, next to theme toggle)
        self.stats_btn_icon = self._load_stats_icon(size=30)
        self.stats_btn = tk.Button(
            self.settings,
            text="📊",
            font=('Arial', 15, 'bold'),
            command=self.clock_app.show_stats,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=2,
            highlightthickness=1,
            padx=2,
            pady=0
        )
        self.stats_btn.config(text="STATS")
        self.stats_btn.pack(side=tk.RIGHT, padx=4)
        if self.stats_btn_icon is not None:
            self.stats_btn.config(
                text="",
                image=self.stats_btn_icon,
                compound=tk.CENTER
            )
        else:
            self.stats_btn.config(text="STATS")

        modern_buttons = [
            self.time_btn_1hr,
            self.time_btn_2hr,
            self.hours_minus_btn,
            self.hours_plus_btn,
            self.mins_minus_btn,
            self.mins_plus_btn,
            self.custom_btn,
        ]
        for btn in modern_buttons:
            btn.config(
                relief=tk.RAISED,
                bd=1,
                activebackground=self.get_t("button_inactive"),
                activeforeground=self.get_t("text_light"),
                padx=8
            )

        # Widgets that control initial timer duration.
        self.time_selection_widgets = [
            self.time_btn_1hr,
            self.time_btn_2hr,
            self.hours_minus_btn,
            self.custom_hours_entry,
            self.hours_plus_btn,
            self.mins_minus_btn,
            self.custom_mins_entry,
            self.mins_plus_btn,
            self.custom_btn,
        ]

    def create_clocks(self):
        """Create player clock frames."""
        self.clocks = tk.Frame(
            self.root,
            bg=self.get_t("main_bg")
        )
        self.clocks.pack(pady=18, padx=24, expand=True, fill=tk.BOTH)

        # Player 1 (Productivity)
        self.p1_frame = tk.Frame(
            self.clocks,
            bg=self.get_t("frame_bg"),
            relief=tk.RIDGE,
            bd=3
        )
        self.p1_frame.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.BOTH)

        self.p1_name = tk.Entry(
            self.p1_frame,
            font=(self.font_family, 15, 'bold'),
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
            font=(self.font_family, 52, 'bold'),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p1_time.pack(pady=40)

        self.p1_btn = tk.Button(
            self.p1_frame,
            text="CLICK",
            font=(self.font_family, 15, 'bold'),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_active"),
            activeforeground=self.get_t("text_light"),
            height=3,
            width=15,
            relief=tk.RAISED,
            bd=2,
            command=lambda: self.clock_app.button_click(1)
        )
        self.p1_btn.pack(pady=25)

        # Player 2 (Slack)
        self.p2_frame = tk.Frame(
            self.clocks,
            bg=self.get_t("frame_bg"),
            relief=tk.RIDGE,
            bd=3
        )
        self.p2_frame.pack(side=tk.RIGHT, padx=15, expand=True, fill=tk.BOTH)

        self.p2_name = tk.Entry(
            self.p2_frame,
            font=(self.font_family, 15, 'bold'),
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
            font=(self.font_family, 52, 'bold'),
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.p2_time.pack(pady=40)

        self.p2_btn = tk.Button(
            self.p2_frame,
            text="CLICK",
            font=(self.font_family, 15, 'bold'),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_active"),
            activeforeground=self.get_t("text_light"),
            height=3,
            width=15,
            relief=tk.RAISED,
            bd=2,
            command=lambda: self.clock_app.button_click(2)
        )
        self.p2_btn.pack(pady=25)

    def create_controls(self):
        """Create control buttons."""
        self.controls = tk.Frame(
            self.root,
            bg=self.get_t("main_bg")
        )
        self.controls.pack(pady=(10, 14))

        self.pause_btn = tk.Button(
            self.controls,
            text="STOP",
            font=(self.font_family, 13, 'bold'),
            command=self.clock_app.toggle_pause,
            width=12,
            height=2,
            bg=self.get_t("button_stop"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_stop"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=2
        )
        self.pause_btn.pack(side=tk.LEFT, padx=8)

        self.reset_btn = tk.Button(
            self.controls,
            text="RESET",
            font=(self.font_family, 13, 'bold'),
            command=self.clock_app.reset,
            width=12,
            height=2,
            bg=self.get_t("button_reset"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_reset"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=2
        )
        self.reset_btn.pack(side=tk.LEFT, padx=8)

    def create_footer(self):
        """Create footer with company and version info."""
        self.footer = tk.Frame(
            self.root,
            bg=self.get_t("main_bg")
        )
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=24, pady=10)

        self.company_label = tk.Label(
            self.footer,
            text=f"Powered by {self.developer_name}",
            font=(self.font_family, 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_muted")
        )
        self.company_label.pack(side=tk.LEFT, anchor=tk.W)

        self.version_label = tk.Label(
            self.footer,
            text=f"v{self.version}",
            font=(self.font_family, 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_muted")
        )
        self.version_label.pack(side=tk.RIGHT, anchor=tk.E)

    def apply_theme(self):
        """Apply the current theme to all widgets."""
        # Main window
        self.root.configure(bg=self.get_t("main_bg"))

        # Title
        self.title_row.config(bg=self.get_t("main_bg"))
        self.title_widget.config(
            bg=self.get_t("main_bg"),
            fg=self.get_t("title_text")
        )
        self.title_subtitle.config(
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_muted")
        )

        # Settings frame
        self.settings.config(bg=self.get_t("settings_bg"))
        self.settings_time_label.config(
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.time_btn_1hr.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=1
        )
        self.time_btn_2hr.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=1
        )
        self.custom_label.config(
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.hours_minus_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=1
        )
        self.custom_hours_entry.config(
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.hours_plus_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=1
        )
        self.hours_label.config(
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.mins_minus_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=1
        )
        self.custom_mins_entry.config(
            bg=self.get_t("frame_bg"),
            fg=self.get_t("text_dark")
        )
        self.mins_plus_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=1
        )
        self.mins_label.config(
            bg=self.get_t("settings_bg"),
            fg=self.get_t("text_light")
        )
        self.custom_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=1
        )
        self.theme_toggle_btn.config(
            text="",
            image=self._get_theme_button_icon(),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=2,
            highlightthickness=1
        )
        if self._get_theme_button_icon() is None:
            self.theme_toggle_btn.config(text=self.theme_manager.get_theme_icon())

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
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light")
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
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light")
        )

        # Controls
        self.controls.config(bg=self.get_t("main_bg"))
        self.pause_btn.config(
            bg=self.get_t("button_stop"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_stop"),
            activeforeground=self.get_t("text_light")
        )
        self.reset_btn.config(
            bg=self.get_t("button_reset"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_reset"),
            activeforeground=self.get_t("text_light")
        )
        self.stats_btn.config(
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light"),
            activebackground=self.get_t("button_inactive"),
            activeforeground=self.get_t("text_light"),
            relief=tk.RAISED,
            bd=2,
            highlightthickness=1
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

    def set_time_selection_enabled(self, enabled):
        """Enable/disable time selection controls."""
        state = tk.NORMAL if enabled else tk.DISABLED
        for widget in getattr(self, "time_selection_widgets", []):
            widget.config(state=state)

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
        from datetime import datetime, timedelta
        import calendar

        win = tk.Toplevel(self.root)
        win.title("Stats Dashboard")
        win.geometry("1200x750")
        win.configure(bg=self.get_t("main_bg"))

        sessions = self.clock_app.stats_tracker.get_sessions_with_metrics()
        today = datetime.now().date()

        # State: track selected date and current month
        state = {
            "selected_date": today,
            "current_month": today.month,
            "current_year": today.year,
            "header_label": None,
            "table_container": None,
            "headline_row": None,
            "insight_row": None,
            "month_label": None,
            "cal_grid_frame": None
        }

        def update_display(selected_date):
            """Update left side when a date is selected."""
            state["selected_date"] = selected_date

            # Update header
            date_str = selected_date.strftime("%A, %B %d, %Y")
            if state["header_label"]:
                state["header_label"].config(text=date_str)

            # Get sessions for selected date
            selected_sessions = self._get_sessions_by_date(sessions, selected_date)

            # Update headline metrics
            if state["headline_row"]:
                for widget in state["headline_row"].winfo_children():
                    widget.destroy()
                self._render_headline_metrics(state["headline_row"], selected_sessions)

            # Update insights
            if state["insight_row"]:
                for widget in state["insight_row"].winfo_children():
                    widget.destroy()
                self._render_insights(state["insight_row"], selected_sessions)

            # Update session table
            if state["table_container"]:
                for widget in state["table_container"].winfo_children():
                    widget.destroy()
                self._render_session_table(state["table_container"], selected_sessions)

            # Redraw calendar grid to show selected date in orange
            if state.get("cal_grid_frame"):
                if selected_date.month == state["current_month"] and selected_date.year == state["current_year"]:
                    for widget in state["cal_grid_frame"].winfo_children():
                        widget.destroy()
                    self._render_calendar_grid(state["cal_grid_frame"], sessions, state, update_display)

        def change_month(delta):
            """Navigate to previous/next month."""
            import calendar
            state["current_month"] += delta
            if state["current_month"] > 12:
                state["current_month"] = 1
                state["current_year"] += 1
            elif state["current_month"] < 1:
                state["current_month"] = 12
                state["current_year"] -= 1

            # Update month label
            if state.get("month_label"):
                state["month_label"].config(text=f"{calendar.month_name[state['current_month']]} {state['current_year']}")

            # Redraw only the calendar grid (not buttons)
            if state.get("cal_grid_frame"):
                for widget in state["cal_grid_frame"].winfo_children():
                    widget.destroy()
            self._render_calendar_grid(state["cal_grid_frame"], sessions, state, update_display)

        header = tk.Frame(win, bg=self.get_t("main_bg"))
        header.pack(fill=tk.X, padx=20, pady=(16, 8))

        state["header_label"] = tk.Label(
            header,
            text=today.strftime("%A, %B %d, %Y"),
            font=('Arial', 20, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )
        state["header_label"].pack(side=tk.LEFT)

        tk.Button(
            header,
            text="Close",
            command=win.destroy,
            font=('Arial', 11),
            width=8,
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        ).pack(side=tk.RIGHT)

        state["headline_row"] = tk.Frame(win, bg=self.get_t("main_bg"))
        state["headline_row"].pack(fill=tk.X, padx=20, pady=(0, 10))
        self._render_headline_metrics(state["headline_row"], self._get_today_sessions(sessions))

        state["insight_row"] = tk.Frame(win, bg=self.get_t("main_bg"))
        state["insight_row"].pack(fill=tk.X, padx=20, pady=(0, 10))
        self._render_insights(state["insight_row"], self._get_today_sessions(sessions))

        # Main content with two columns
        content_frame = tk.Frame(win, bg=self.get_t("main_bg"))
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

        # Left column: sessions for selected date
        left_frame = tk.Frame(content_frame, bg=self.get_t("main_bg"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        state["table_container"] = tk.Frame(left_frame, bg=self.get_t("main_bg"))
        state["table_container"].pack(fill=tk.BOTH, expand=True)
        self._render_session_table(state["table_container"], self._get_today_sessions(sessions))

        # Right column: calendar
        right_frame = tk.Frame(content_frame, bg=self.get_t("main_bg"))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        # Calendar header with navigation buttons
        cal_header_frame = tk.Frame(right_frame, bg=self.get_t("main_bg"))
        cal_header_frame.pack(fill=tk.X, pady=(0, 10))

        cal_header = tk.Label(
            cal_header_frame,
            text="Activity Calendar",
            font=('Arial', 12, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )
        cal_header.pack(pady=(0, 10))

        # Navigation frame
        nav_frame = tk.Frame(right_frame, bg=self.get_t("main_bg"))
        nav_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Button(
            nav_frame,
            text="< Prev",
            width=8,
            font=('Arial', 9),
            command=lambda: change_month(-1),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        ).pack(side=tk.LEFT, padx=5)

        state["month_label"] = tk.Label(
            nav_frame,
            text=f"{calendar.month_name[state['current_month']]} {state['current_year']}",
            font=('Arial', 11, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )
        state["month_label"].pack(side=tk.LEFT, expand=True)

        tk.Button(
            nav_frame,
            text="Next >",
            width=8,
            font=('Arial', 9),
            command=lambda: change_month(1),
            bg=self.get_t("button_inactive"),
            fg=self.get_t("text_light")
        ).pack(side=tk.RIGHT, padx=5)

        # Calendar grid frame (will be cleared on month change)
        state["cal_grid_frame"] = tk.Frame(right_frame, bg=self.get_t("main_bg"))
        state["cal_grid_frame"].pack(fill=tk.BOTH, expand=True)

        # Initial render
        import calendar
        self._render_calendar_grid(state["cal_grid_frame"], sessions, state, update_display)

    def _get_today_sessions(self, sessions):
        """Filter sessions to today by local date."""
        from datetime import datetime

        today = datetime.now().date()
        return self._get_sessions_by_date(sessions, today)

    def _get_sessions_by_date(self, sessions, target_date):
        """Filter sessions to a specific date."""
        from datetime import datetime

        filtered_sessions = []
        for session in sessions:
            start = session.get("start_time")
            if not start:
                continue
            try:
                start_dt = datetime.fromisoformat(start)
            except ValueError:
                continue
            if start_dt.date() == target_date:
                filtered_sessions.append(session)
        return filtered_sessions

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
                font=('Arial', 15, 'bold'),
                bg=self.get_t("settings_bg"),
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

    def _render_calendar_grid(self, grid_frame, sessions, state, on_day_select=None):
        """Render just the calendar grid (for month changes)."""
        import calendar
        from datetime import datetime

        # Build day -> session count mapping
        day_sessions = {}
        for session in sessions:
            start_time = session.get("start_time")
            if not start_time:
                continue
            try:
                start_dt = datetime.fromisoformat(start_time)
                day = start_dt.date()
                day_sessions[day] = day_sessions.get(day, 0) + 1
            except ValueError:
                continue

        # Weekday headers
        for col, day_name in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            tk.Label(
                grid_frame,
                text=day_name,
                font=('Arial', 9, 'bold'),
                bg=self.get_t("settings_bg"),
                fg=self.get_t("text_light"),
                width=6,
                height=2
            ).grid(row=0, column=col, padx=2, pady=2, sticky='nsew')

        # Calendar days
        cal_obj = calendar.monthcalendar(state['current_year'], state['current_month'])
        today = datetime.now().date()

        for week_num, week in enumerate(cal_obj):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell for days outside the month
                    tk.Label(
                        grid_frame,
                        text="",
                        bg=self.get_t("main_bg")
                    ).grid(row=week_num + 1, column=day_num, padx=2, pady=2)
                else:
                    day_date = datetime(state['current_year'], state['current_month'], day).date()
                    sessions_count = day_sessions.get(day_date, 0)

                    # Determine color based on activity
                    if day_date == today:
                        bg_color = self.get_t("button_active")
                        text_color = self.get_t("text_light")
                    elif day_date == state.get("selected_date"):
                        bg_color = self.get_t("warning_medium")
                        text_color = self.get_t("text_light")
                    elif sessions_count > 0:
                        bg_color = self.get_t("frame_bg")
                        text_color = self.get_t("text_dark")
                    else:
                        bg_color = self.get_t("frame_bg")
                        text_color = self.get_t("text_dark")

                    # Create day cell as button
                    day_text = f"{day}"
                    if sessions_count > 0:
                        day_text += f"\n({sessions_count})"

                    def make_click_handler(d):
                        def click_handler():
                            if on_day_select:
                                selected = datetime(state['current_year'], state['current_month'], d).date()
                                on_day_select(selected)
                        return click_handler

                    tk.Button(
                        grid_frame,
                        text=day_text,
                        font=('Arial', 8),
                        bg=bg_color,
                        fg=text_color,
                        width=6,
                        height=4,
                        relief=tk.RAISED,
                        bd=1,
                        command=make_click_handler(day) if on_day_select else None
                    ).grid(row=week_num + 1, column=day_num, padx=2, pady=2, sticky='nsew')

        # Legend removed.
        return
        tk.Label(
            legend_frame,
            text="●",
            font=('Arial', 12),
            bg=self.get_t("main_bg"),
            fg=self.get_t("button_active")
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            legend_frame,
            text="Today",
            font=('Arial', 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            legend_frame,
            text="●",
            font=('Arial', 12),
            bg=self.get_t("main_bg"),
            fg=self.get_t("warning_medium")
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            legend_frame,
            text="Selected",
            font=('Arial', 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        ).pack(side=tk.LEFT)

    def _render_calendar(self, parent, sessions, state=None, on_day_select=None, on_month_change=None):
        """Render activity calendar showing days with sessions."""
        import calendar
        from datetime import datetime, timedelta

        if state is None:
            state = {"current_month": datetime.now().month, "current_year": datetime.now().year}

        # Calendar header
        cal_header = tk.Label(
            parent,
            text="Activity Calendar",
            font=('Arial', 12, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )
        cal_header.pack(pady=(0, 10))

        # Build day -> session count mapping
        day_sessions = {}
        for session in sessions:
            start_time = session.get("start_time")
            if not start_time:
                continue
            try:
                start_dt = datetime.fromisoformat(start_time)
                day = start_dt.date()
                day_sessions[day] = day_sessions.get(day, 0) + 1
            except ValueError:
                continue

        # Create navigation frame
        nav_frame = tk.Frame(parent, bg=self.get_t("main_bg"))
        nav_frame.pack(fill=tk.X, pady=(0, 10))

        if on_month_change:
            tk.Button(
                nav_frame,
                text="< Prev",
                width=8,
                font=('Arial', 9),
                command=lambda: on_month_change(-1),
                bg=self.get_t("button_inactive"),
                fg=self.get_t("text_light")
            ).pack(side=tk.LEFT, padx=5)

        month_label = tk.Label(
            nav_frame,
            text=f"{calendar.month_name[state['current_month']]} {state['current_year']}",
            font=('Arial', 11, 'bold'),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        )
        month_label.pack(side=tk.LEFT, expand=True)

        if on_month_change:
            tk.Button(
                nav_frame,
                text="Next >",
                width=8,
                font=('Arial', 9),
                command=lambda: on_month_change(1),
                bg=self.get_t("button_inactive"),
                fg=self.get_t("text_light")
            ).pack(side=tk.RIGHT, padx=5)

        # Create calendar grid
        cal_frame = tk.Frame(parent, bg=self.get_t("main_bg"))
        cal_frame.pack()

        # Weekday headers
        for col, day_name in enumerate(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            tk.Label(
                cal_frame,
                text=day_name,
                font=('Arial', 9, 'bold'),
                bg=self.get_t("settings_bg"),
                fg=self.get_t("text_light"),
                width=6,
                height=2
            ).grid(row=0, column=col, padx=2, pady=2, sticky='nsew')

        # Calendar days
        cal_obj = calendar.monthcalendar(state['current_year'], state['current_month'])
        today = datetime.now().date()

        for week_num, week in enumerate(cal_obj):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell for days outside the month
                    tk.Label(
                        cal_frame,
                        text="",
                        bg=self.get_t("main_bg")
                    ).grid(row=week_num + 1, column=day_num, padx=2, pady=2)
                else:
                    day_date = datetime(state['current_year'], state['current_month'], day).date()
                    sessions_count = day_sessions.get(day_date, 0)

                    # Determine color based on activity
                    if day_date == today:
                        bg_color = self.get_t("button_active")
                        text_color = self.get_t("text_light")
                    elif day_date == state.get("selected_date"):
                        bg_color = self.get_t("warning_medium")
                        text_color = self.get_t("text_light")
                    elif sessions_count > 0:
                        bg_color = self.get_t("frame_bg")
                        text_color = self.get_t("text_dark")
                    else:
                        bg_color = self.get_t("frame_bg")
                        text_color = self.get_t("text_dark")

                    # Create day cell as button
                    day_text = f"{day}"
                    if sessions_count > 0:
                        day_text += f"\n({sessions_count})"

                    def make_click_handler(d):
                        def click_handler():
                            if on_day_select:
                                selected = datetime(state['current_year'], state['current_month'], d).date()
                                on_day_select(selected)
                        return click_handler

                    tk.Button(
                        cal_frame,
                        text=day_text,
                        font=('Arial', 8),
                        bg=bg_color,
                        fg=text_color,
                        width=6,
                        height=4,
                        relief=tk.RAISED,
                        bd=1,
                        command=make_click_handler(day) if on_day_select else None
                    ).grid(row=week_num + 1, column=day_num, padx=2, pady=2, sticky='nsew')

        # Legend removed.
        return
        legend_frame = tk.Frame(parent, bg=self.get_t("main_bg"))
        legend_frame.pack(pady=(15, 0))

        tk.Label(
            legend_frame,
            text="●",
            font=('Arial', 12),
            bg=self.get_t("main_bg"),
            fg=self.get_t("button_active")
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            legend_frame,
            text="Today",
            font=('Arial', 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            legend_frame,
            text="●",
            font=('Arial', 12),
            bg=self.get_t("main_bg"),
            fg=self.get_t("warning_medium")
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            legend_frame,
            text="Selected",
            font=('Arial', 9),
            bg=self.get_t("main_bg"),
            fg=self.get_t("text_light")
        ).pack(side=tk.LEFT)
