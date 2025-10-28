import arcade
import constants as c

class StartMenuView(arcade.View):
    """Start menu where players choose their color (resolution-independent)."""

    def __init__(self):
        super().__init__()

        # Load once; draw scaled each frame
        self.bg_tex = arcade.load_texture("images/menu_screen.png")

        self.selected_color = None
        self.showing_colors = False

        self.player_colors = [
            ("RED", "red.png"),
            ("BLUE", "blue.png"),
            ("GREEN", "green.png"),
            ("YELLOW", "yellow.png")
        ]
        self.card_textures = {
            name: arcade.load_texture(f"images/{fn}")
            for name, fn in self.player_colors
        }

        # Click bounds are recomputed every on_draw based on current size
        self.color_buttons = []
        self.start_button_bounds = None
        self.choose_color_button_bounds = None

    # Layout helpers (use window size, not constants)

    def sw(self) -> int:
        return getattr(self.window, "width", c.SCREEN_WIDTH)

    def sh(self) -> int:
        return getattr(self.window, "height", c.WINDOW_HEIGHT)

    def _cover_scale_rect(self, tex_w, tex_h, view_w, view_h):
        """
        Compute LBWH rect to draw a texture scaled to 'cover' the screen
        while preserving aspect ratio (like CSS background-size: cover).
        """
        scale = max(view_w / tex_w, view_h / tex_h)
        draw_w = tex_w * scale
        draw_h = tex_h * scale
        left = (view_w - draw_w) / 2
        bottom = (view_h - draw_h) / 2
        return arcade.LBWH(left, bottom, draw_w, draw_h)

    def _centered_rect(self, cx, cy, w, h):
        """Return LBWH rect centered at (cx,cy)."""
        return arcade.LBWH(cx - w / 2, cy - h / 2, w, h)

    # Standard View methods

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        W, H = self.sw(), self.sh()

        # Background scaled to cover the screen
        bg_rect = self._cover_scale_rect(self.bg_tex.width, self.bg_tex.height, W, H)
        arcade.draw_texture_rect(self.bg_tex, bg_rect)

        # UI
        if not self.showing_colors:
            self.draw_choose_color_button()
        else:
            self.draw_color_buttons()
            if self.selected_color:
                arcade.draw_text(
                    f"Selected: {self.selected_color}",
                    W * 0.5, H * 0.18,
                    arcade.color.YELLOW, font_size=int(H * 0.028),
                    anchor_x="center", anchor_y="center", bold=True
                )
                self.draw_start_button()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Choose-your-color button
        if not self.showing_colors and self.choose_color_button_bounds:
            l, r, b, t = self.choose_color_button_bounds
            if l <= x <= r and b <= y <= t:
                self.showing_colors = True
                return

        # Color buttons + Start
        if self.showing_colors:
            for btn in self.color_buttons:
                l, r, b, t = btn['bounds']
                if l <= x <= r and b <= y <= t:
                    self.selected_color = btn['color']
                    return

            if self.selected_color and self.start_button_bounds:
                l, r, b, t = self.start_button_bounds
                if l <= x <= r and b <= y <= t:
                    from board import GameView
                    game_view = GameView(player_color=self.selected_color)
                    game_view.reset()
                    self.window.show_view(game_view)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.close()

    # Drawing primitives that rebuild bounds per frame

    def draw_choose_color_button(self):
        W, H = self.sw(), self.sh()

        # Size scales with screen; clamp to sensible range
        btn_w = max(260, min(420, int(W * 0.23)))
        btn_h = max(64,  min(96,  int(H * 0.09)))
        cx, cy = W * 0.50, H * 0.15

        tex = arcade.make_soft_square_texture(2, (154, 30, 31), outer_alpha=255)
        rect = self._centered_rect(cx, cy, btn_w, btn_h)
        arcade.draw_texture_rect(tex, rect)
        arcade.draw_rect_outline(rect, arcade.color.WHITE, border_width=4)
        arcade.draw_text(
            "CHOOSE YOUR COLOR", cx, cy,
            arcade.color.WHITE, font_size=int(H * 0.035),
            anchor_x="center", anchor_y="center", bold=True
        )
        self.choose_color_button_bounds = (rect.left, rect.left + rect.width,
                                           rect.bottom, rect.bottom + rect.height)

    def draw_color_buttons(self):
        W, H = self.sw(), self.sh()

        # Card size and row layout scale with height (keeps aspect consistent)
        card_w = max(100, min(160, int(H * 0.12)))
        card_h = int(card_w * 4/3)   # keep card aspect
        spacing = max(16, int(card_w * 0.18))

        total_w = card_w * len(self.player_colors) + spacing * (len(self.player_colors) - 1)
        start_x = (W - total_w) / 2 + card_w / 2
        y = H * 0.35

        self.color_buttons = []
        for i, (name, _) in enumerate(self.player_colors):
            x = start_x + i * (card_w + spacing)
            tex = self.card_textures[name]
            rect = self._centered_rect(x, y, card_w, card_h)
            arcade.draw_texture_rect(tex, rect)

            selected = (self.selected_color == name)
            arcade.draw_rect_outline(rect,
                                     arcade.color.YELLOW if selected else arcade.color.WHITE,
                                     border_width=5 if selected else 2)

            # Label
            label_color = arcade.color.BLACK if name in ("WHITE", "YELLOW") else arcade.color.WHITE
            arcade.draw_text(name, x, y, label_color,
                             font_size=int(H * 0.022),
                             anchor_x="center", anchor_y="center", bold=True)

            self.color_buttons.append({
                "color": name,
                "bounds": (rect.left, rect.left + rect.width,
                           rect.bottom, rect.bottom + rect.height)
            })

    def draw_start_button(self):
        W, H = self.sw(), self.sh()

        btn_w = max(180, min(260, int(W * 0.16)))
        btn_h = max(54,  min(86,  int(H * 0.08)))
        cx, cy = W * 0.50, H * 0.08

        tex = arcade.make_soft_square_texture(2, (34, 139, 34), outer_alpha=255)
        rect = self._centered_rect(cx, cy, btn_w, btn_h)
        arcade.draw_texture_rect(tex, rect)
        arcade.draw_rect_outline(rect, arcade.color.WHITE, border_width=3)
        arcade.draw_text(
            "START GAME", cx, cy, arcade.color.WHITE,
            font_size=int(H * 0.03),
            anchor_x="center", anchor_y="center", bold=True
        )
        self.start_button_bounds = (rect.left, rect.left + rect.width,
                                    rect.bottom, rect.bottom + rect.height)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        # Bounds are recomputed on each on_draw; nothing else needed.
