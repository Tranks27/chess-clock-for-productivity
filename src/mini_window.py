"""Mini floating timer window for TrueFocus Timer."""

import ctypes
import os
import tkinter as tk

from src.audio import get_script_dir

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageTk
except ImportError:
    Image = None
    ImageDraw = None
    ImageEnhance = None
    ImageFilter = None
    ImageTk = None


class MiniWindowManager:
    """Manage the circular mini timer window shown while app is minimized."""

    def __init__(self, root, theme_manager, timer_state, switch_player_callback=None):
        self.root = root
        self.theme_manager = theme_manager
        self.timer_state = timer_state
        self.switch_player_callback = switch_player_callback

        self.mini_window = None
        self.mini_status_text_id = None
        self.mini_time_text_id = None
        self.mini_slack_text_id = None
        self.mini_status_shadow_id = None
        self.mini_time_shadow_id = None
        self.mini_slack_shadow_id = None
        self.mini_background_icon = None
        self.mini_background_icon_source = None
        self.mini_background_icon_mtime = None
        self.mini_circle_canvas = None
        self.mini_shape_size = 210
        self.mini_icon_zoom = 1.45
        self.mini_transparent_key = "#FF00FF"
        self.mini_drag_offset_x = 0
        self.mini_drag_offset_y = 0
        self.mini_custom_position = None
        self.mini_focus_btn_bg_id = None
        self.mini_focus_btn_text_id = None
        self.mini_slack_btn_bg_id = None
        self.mini_slack_btn_text_id = None

    def on_root_unmap(self, event):
        """Handle root minimize/hide."""
        if event.widget is not self.root:
            return
        self.root.after(100, self.sync_with_root_state)

    def on_root_map(self, event):
        """Handle root restore/show."""
        if event.widget is not self.root:
            return
        self.root.after(100, self.sync_with_root_state)

    def sync_with_root_state(self):
        """Show mini timer when minimized, hide when restored."""
        if str(self.root.state()) == "iconic":
            self.show()
        else:
            self.hide()

    def show(self):
        """Show mini timer window."""
        if self.mini_window is None or not self.mini_window.winfo_exists():
            self._create_window()
        self._position_window()
        self.update()
        self.mini_window.deiconify()
        self.mini_window.lift()

    def hide(self):
        """Hide mini timer window."""
        if self.mini_window is not None and self.mini_window.winfo_exists():
            self.mini_window.withdraw()

    def restore_main(self):
        """Restore main app window and hide mini timer."""
        self.hide()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def destroy(self):
        """Destroy mini timer resources."""
        if self.mini_window is not None and self.mini_window.winfo_exists():
            self.mini_window.destroy()

    def apply_theme(self):
        """Apply theme to mini timer visuals."""
        if self.mini_window is None or not self.mini_window.winfo_exists():
            return

        bg = self.theme_manager.get_color("main_bg")
        self.mini_window.configure(bg=self.mini_transparent_key)
        if self.mini_circle_canvas is not None:
            self.mini_circle_canvas.config(bg=self.mini_transparent_key)
            self._render_background(bg)
            self.mini_circle_canvas.itemconfig(self.mini_status_shadow_id, fill="#101010")
            self.mini_circle_canvas.itemconfig(self.mini_time_shadow_id, fill="#101010")
            self.mini_circle_canvas.itemconfig(self.mini_slack_shadow_id, fill="#101010")
            self.mini_circle_canvas.itemconfig(self.mini_time_text_id, fill="#FFF4DB")
            self.mini_circle_canvas.itemconfig(self.mini_slack_text_id, fill="#FF6B7A")
            if self.mini_focus_btn_text_id is not None:
                self.mini_circle_canvas.itemconfig(self.mini_focus_btn_text_id, fill="#FFF4DB")
            if self.mini_slack_btn_text_id is not None:
                self.mini_circle_canvas.itemconfig(self.mini_slack_btn_text_id, fill="#FFF4DB")

    def update(self):
        """Refresh displayed status and times."""
        if self.mini_window is None or not self.mini_window.winfo_exists():
            return

        p1 = self.timer_state.format_time(self.timer_state.player1_time)
        p2 = self.timer_state.format_time(self.timer_state.player2_time)

        if self.timer_state.active_player is None:
            status = "READY"
            status_color = "#DCE6F7"
        elif self.timer_state.running and self.timer_state.active_player == 1:
            status = "FOCUS"
            status_color = "#6EE7FF"
        elif self.timer_state.running and self.timer_state.active_player == 2:
            status = "SLACK"
            status_color = "#FF9A62"
        else:
            status = "PAUSED"
            status_color = "#B8C2D6"

        if self.mini_circle_canvas is not None:
            self.mini_circle_canvas.itemconfig(self.mini_status_text_id, text=status, fill=status_color)
            self.mini_circle_canvas.itemconfig(self.mini_status_shadow_id, text=status)
            self.mini_circle_canvas.itemconfig(self.mini_time_text_id, text=p1)
            self.mini_circle_canvas.itemconfig(self.mini_time_shadow_id, text=p1)
            self.mini_circle_canvas.itemconfig(self.mini_slack_text_id, text=p2)
            self.mini_circle_canvas.itemconfig(self.mini_slack_shadow_id, text=p2)
            self._update_switch_button_styles()

    def _create_window(self):
        """Create mini timer window and its canvas elements."""
        self.mini_window = tk.Toplevel(self.root)
        self.mini_window.title(" ")
        self._set_window_icon(self.mini_window)
        self.mini_window.geometry(f"{self.mini_shape_size}x{self.mini_shape_size}")
        self.mini_window.resizable(False, False)
        self.mini_window.overrideredirect(True)
        self.mini_window.attributes("-topmost", True)
        self.mini_window.configure(bg=self.mini_transparent_key)
        try:
            self.mini_window.attributes("-transparentcolor", self.mini_transparent_key)
        except tk.TclError:
            pass

        self.mini_circle_canvas = tk.Canvas(
            self.mini_window,
            width=self.mini_shape_size,
            height=self.mini_shape_size,
            highlightthickness=0,
            bd=0,
            bg=self.mini_transparent_key,
        )
        self.mini_circle_canvas.pack(fill=tk.BOTH, expand=True)

        center_x = self.mini_shape_size // 2
        status_y = int(self.mini_shape_size * 0.22)
        main_y = int(self.mini_shape_size * 0.50)
        slack_y = int(self.mini_shape_size * 0.69)
        buttons_y = int(self.mini_shape_size * 0.84)
        button_width = int(self.mini_shape_size * 0.20)
        button_height = int(self.mini_shape_size * 0.12)
        button_gap = int(self.mini_shape_size * 0.04)

        self.mini_status_shadow_id = self.mini_circle_canvas.create_text(
            center_x + 1, status_y + 1, text="READY",
            font=("Segoe UI", 13, "bold"), fill="#000000", tags="mini_overlay"
        )
        self.mini_status_text_id = self.mini_circle_canvas.create_text(
            center_x, status_y, text="READY",
            font=("Segoe UI", 13, "bold"), fill="#9DEAFF", tags="mini_overlay"
        )

        self.mini_time_shadow_id = self.mini_circle_canvas.create_text(
            center_x + 1, main_y + 1, text="00:00:00",
            font=("Consolas", 34, "bold"), fill="#000000", tags="mini_overlay"
        )
        self.mini_time_text_id = self.mini_circle_canvas.create_text(
            center_x, main_y, text="00:00:00",
            font=("Consolas", 34, "bold"), fill="#FFF4DB", tags="mini_overlay"
        )

        self.mini_slack_shadow_id = self.mini_circle_canvas.create_text(
            center_x + 1, slack_y + 1, text="00:00:00",
            font=("Consolas", 14, "bold"), fill="#000000", tags="mini_overlay"
        )
        self.mini_slack_text_id = self.mini_circle_canvas.create_text(
            center_x, slack_y, text="00:00:00",
            font=("Consolas", 14, "bold"), fill="#FF6B7A", tags="mini_overlay"
        )

        focus_left = center_x - button_gap // 2 - button_width
        focus_right = center_x - button_gap // 2
        slack_left = center_x + button_gap // 2
        slack_right = center_x + button_gap // 2 + button_width
        btn_top = buttons_y - button_height // 2
        btn_bottom = buttons_y + button_height // 2

        self.mini_focus_btn_bg_id = self.mini_circle_canvas.create_rectangle(
            focus_left, btn_top, focus_right, btn_bottom,
            outline="#0B1220", width=1, fill="#1D2A3A", tags=("mini_focus_btn", "mini_overlay")
        )
        self.mini_focus_btn_text_id = self.mini_circle_canvas.create_text(
            (focus_left + focus_right) // 2, buttons_y, text="FOCUS",
            font=("Segoe UI", 7, "bold"), fill="#FFF4DB", tags=("mini_focus_btn", "mini_overlay")
        )
        self.mini_slack_btn_bg_id = self.mini_circle_canvas.create_rectangle(
            slack_left, btn_top, slack_right, btn_bottom,
            outline="#0B1220", width=1, fill="#3A2323", tags=("mini_slack_btn", "mini_overlay")
        )
        self.mini_slack_btn_text_id = self.mini_circle_canvas.create_text(
            (slack_left + slack_right) // 2, buttons_y, text="SLACK",
            font=("Segoe UI", 7, "bold"), fill="#FFF4DB", tags=("mini_slack_btn", "mini_overlay")
        )

        self.mini_circle_canvas.tag_bind("mini_focus_btn", "<Button-1>", self._on_focus_button_click)
        self.mini_circle_canvas.tag_bind("mini_slack_btn", "<Button-1>", self._on_slack_button_click)

        self._bind_drag(self.mini_window)
        self._bind_drag(self.mini_circle_canvas)
        self.mini_circle_canvas.bind("<Double-Button-1>", lambda _event: self.restore_main())

        self._position_window()
        self.apply_theme()
        self.update()

    def _position_window(self):
        """Place mini timer near bottom-right (or saved custom position)."""
        if self.mini_window is None or not self.mini_window.winfo_exists():
            return
        self.mini_window.update_idletasks()
        width = self.mini_window.winfo_width()
        height = self.mini_window.winfo_height()
        left, top, right, bottom = self._get_work_area_bounds()

        if self.mini_custom_position is None:
            x = right - width - 8
            y = bottom - height - 8
        else:
            left, top, right, bottom = self._get_virtual_desktop_bounds()
            x, y = self.mini_custom_position
            x = max(left, min(x, right - width))
            y = max(top, min(y, bottom - height))
            self.mini_custom_position = (x, y)
        self.mini_window.geometry(f"+{x}+{y}")

    def _bind_drag(self, widget):
        """Bind drag handlers for moving mini window."""
        widget.bind("<ButtonPress-1>", self._on_drag_start, add="+")
        widget.bind("<B1-Motion>", self._on_drag_motion, add="+")

    def _on_drag_start(self, event):
        """Capture drag offset."""
        if self.mini_window is None or not self.mini_window.winfo_exists():
            return
        if self._event_over_switch_button(event):
            return
        self.mini_drag_offset_x = event.x_root - self.mini_window.winfo_x()
        self.mini_drag_offset_y = event.y_root - self.mini_window.winfo_y()

    def _on_drag_motion(self, event):
        """Move mini window during drag."""
        if self.mini_window is None or not self.mini_window.winfo_exists():
            return
        if self._event_over_switch_button(event):
            return
        left, top, right, bottom = self._get_virtual_desktop_bounds()
        width = self.mini_window.winfo_width()
        height = self.mini_window.winfo_height()
        x = event.x_root - self.mini_drag_offset_x
        y = event.y_root - self.mini_drag_offset_y
        x = max(left, min(x, right - width))
        y = max(top, min(y, bottom - height))
        self.mini_custom_position = (x, y)
        self.mini_window.geometry(f"+{x}+{y}")

    def _on_focus_button_click(self, _event):
        """Switch to focus clock from mini window."""
        if callable(self.switch_player_callback):
            self.switch_player_callback(1)
            self.update()
        return "break"

    def _on_slack_button_click(self, _event):
        """Switch to slack clock from mini window."""
        if callable(self.switch_player_callback):
            self.switch_player_callback(2)
            self.update()
        return "break"

    def _event_over_switch_button(self, event):
        """Return True when pointer is over a switch button item."""
        if self.mini_circle_canvas is None:
            return False
        hit_items = self.mini_circle_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item_id in hit_items:
            tags = self.mini_circle_canvas.gettags(item_id)
            if "mini_focus_btn" in tags or "mini_slack_btn" in tags:
                return True
        return False

    def _update_switch_button_styles(self):
        """Highlight mini switch button for active clock."""
        if (
            self.mini_focus_btn_bg_id is None
            or self.mini_slack_btn_bg_id is None
            or self.mini_circle_canvas is None
        ):
            return

        focus_fill = "#1D2A3A"
        slack_fill = "#3A2323"
        if self.timer_state.active_player == 1 and self.timer_state.running:
            focus_fill = "#227A99"
        elif self.timer_state.active_player == 2 and self.timer_state.running:
            slack_fill = "#A14F2A"

        self.mini_circle_canvas.itemconfig(self.mini_focus_btn_bg_id, fill=focus_fill)
        self.mini_circle_canvas.itemconfig(self.mini_slack_btn_bg_id, fill=slack_fill)

    def _get_virtual_desktop_bounds(self):
        """Get virtual desktop bounds across monitors."""
        try:
            sm_xvirtualscreen = 76
            sm_yvirtualscreen = 77
            sm_cxvirtualscreen = 78
            sm_cyvirtualscreen = 79
            left = ctypes.windll.user32.GetSystemMetrics(sm_xvirtualscreen)
            top = ctypes.windll.user32.GetSystemMetrics(sm_yvirtualscreen)
            width = ctypes.windll.user32.GetSystemMetrics(sm_cxvirtualscreen)
            height = ctypes.windll.user32.GetSystemMetrics(sm_cyvirtualscreen)
            return left, top, left + width, top + height
        except Exception:
            screen_w = self.mini_window.winfo_screenwidth()
            screen_h = self.mini_window.winfo_screenheight()
            return 0, 0, screen_w, screen_h

    def _get_work_area_bounds(self):
        """Get desktop work area excluding taskbar."""
        screen_w = self.mini_window.winfo_screenwidth()
        screen_h = self.mini_window.winfo_screenheight()

        try:
            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", ctypes.c_long),
                    ("top", ctypes.c_long),
                    ("right", ctypes.c_long),
                    ("bottom", ctypes.c_long),
                ]

            rect = RECT()
            spi_get_work_area = 0x0030
            if ctypes.windll.user32.SystemParametersInfoW(spi_get_work_area, 0, ctypes.byref(rect), 0):
                return rect.left, rect.top, rect.right, rect.bottom
        except Exception:
            pass

        return 0, 0, screen_w, screen_h

    def _render_background(self, fallback_color):
        """Render circular mini background image with readability adjustments."""
        if self.mini_circle_canvas is None or not self.mini_circle_canvas.winfo_exists():
            return

        self.mini_circle_canvas.delete("mini_bg")
        size = self.mini_shape_size - 4

        png_fallback = os.path.join(get_script_dir(), "assets", "media", "truefocus_timer.png")
        icon_candidates = self._get_preferred_icon_paths() + [png_fallback]

        selected_path = None
        selected_mtime = None
        for icon_path in icon_candidates:
            if os.path.exists(icon_path):
                selected_path = icon_path
                selected_mtime = os.path.getmtime(icon_path)
                break

        needs_reload = (
            self.mini_background_icon is None
            or selected_path != self.mini_background_icon_source
            or selected_mtime != self.mini_background_icon_mtime
        )

        if needs_reload:
            self.mini_background_icon = None
            self.mini_background_icon_source = selected_path
            self.mini_background_icon_mtime = selected_mtime
            if selected_path is not None:
                try:
                    if (
                        Image is not None
                        and ImageDraw is not None
                        and ImageTk is not None
                        and ImageEnhance is not None
                        and ImageFilter is not None
                    ):
                        resampling = Image.Resampling if hasattr(Image, "Resampling") else Image
                        src = Image.open(selected_path).convert("RGBA")
                        zoom_size = max(size, int(size * self.mini_icon_zoom))
                        src = src.resize((zoom_size, zoom_size), resampling.LANCZOS)
                        crop_left = (zoom_size - size) // 2
                        crop_top = (zoom_size - size) // 2
                        src = src.crop((crop_left, crop_top, crop_left + size, crop_top + size))
                        src = ImageEnhance.Color(src).enhance(0.75)
                        src = ImageEnhance.Brightness(src).enhance(0.55)
                        src = src.filter(ImageFilter.GaussianBlur(0.45))
                        src = Image.alpha_composite(src, Image.new("RGBA", (size, size), (0, 0, 0, 65)))
                        mask = Image.new("L", (size, size), 0)
                        ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
                        src.putalpha(mask)
                        self.mini_background_icon = ImageTk.PhotoImage(src)
                    else:
                        self.mini_background_icon = tk.PhotoImage(file=selected_path)
                except Exception:
                    self.mini_background_icon = None

        if self.mini_background_icon is not None:
            center = self.mini_shape_size // 2
            self.mini_circle_canvas.create_image(center, center, image=self.mini_background_icon, tags="mini_bg")
        else:
            self.mini_circle_canvas.create_oval(
                2, 2, self.mini_shape_size - 2, self.mini_shape_size - 2,
                outline="", fill=fallback_color, tags="mini_bg"
            )

        self.mini_circle_canvas.tag_lower("mini_bg")

    def _set_window_icon(self, window):
        """Set icon for mini toplevel."""
        for icon_path in self._get_preferred_icon_paths():
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
                break

    def _get_preferred_icon_paths(self):
        """Return icon candidates in priority order."""
        media_dir = os.path.join(get_script_dir(), "assets", "media")
        return [os.path.join(media_dir, "app_icon_circle.ico")]
