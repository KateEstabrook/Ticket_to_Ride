"""
Start Menu View for Ticket to Ride
Add this class to your main game file, before the GameView class
"""

import arcade
from arcade import SpriteList
import constants as c
import player
import globals

class StartMenuView(arcade.View):
    """Start menu where players choose their color"""

    def __init__(self):
        super().__init__()
        # Create a sprite for the background
        # self.background_sprite = arcade.Sprite("images/menu_screen.png")
        self.bg_tex = arcade.load_texture("images/menu_screen.png")

        self.selected_color = None

        # Track which stage we're in
        self.showing_colors = False

        # Available player colors with their card images
        self.player_colors = [
            ("Red", "red.png"),
            ("Blue", "blue.png"),
            ("Green", "green.png"),
            ("Yellow", "yellow.png")
        ]

        # Load card textures
        self.card_textures = {}
        for color_name, filename in self.player_colors:
            self.card_textures[color_name] = arcade.load_texture(f"images/{filename}")

        self.color_buttons = []
        self.start_button_bounds = None
        self.choose_color_button_bounds = None

    def sw(self) -> int:
        """Window width (falls back to constants if needed)."""
        return getattr(self.window, "width", c.SCREEN_WIDTH)

    def sh(self) -> int:
        """Window height (falls back to constants if needed)."""
        return getattr(self.window, "height", c.WINDOW_HEIGHT)

    def _cover_scale_rect(self, tex_w, tex_h, view_w, view_h):
        """Scale a texture to *cover* the view (preserve aspect), return LBWH rect."""
        scale = max(view_w / tex_w, view_h / tex_h)
        draw_w = tex_w * scale
        draw_h = tex_h * scale
        left = (view_w - draw_w) / 2
        bottom = (view_h - draw_h) / 2
        return arcade.LBWH(left, bottom, draw_w, draw_h)

    def _centered_rect(self, cx, cy, w, h):
        """LBWH rect centered at (cx, cy)."""
        return arcade.LBWH(cx - w / 2, cy - h / 2, w, h)

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Render the start menu"""
        self.clear()

        width, height = self.sw(), self.sh()

        # Draw background scaled to cover the screen
        bg_rect = self._cover_scale_rect(self.bg_tex.width, self.bg_tex.height, width, height)
        arcade.draw_texture_rect(self.bg_tex, bg_rect)

        if not self.showing_colors:
            # show only "Choose Your Color" button
            self.draw_choose_color_button()
        else:
            # show color selection and start button

            # Draw color selection buttons
            self.draw_color_buttons()

            # Show selected color
            if self.selected_color:
                arcade.draw_text(
                    f"Selected: {self.selected_color}",
                    c.SCREEN_WIDTH // 2 - 192,
                    c.WINDOW_HEIGHT * 0.18,
                    arcade.color.YELLOW,
                    font_size=20,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )

                # Draw start button
                self.draw_start_button()

    def draw_choose_color_button(self):
        """Draw the initial 'Choose Your Color' button"""
        width, height = self.sw(), self.sh()

        btn_w = max(260, min(420, int(width * 0.23)))
        btn_h = max(64, min(96, int(height * 0.09)))
        cx, cy = width * 0.50, height * 0.15

        tex = arcade.make_soft_square_texture(2, (154, 30, 31), outer_alpha=255)
        rect = self._centered_rect(cx, cy, btn_w, btn_h)
        arcade.draw_texture_rect(tex, rect)
        arcade.draw_rect_outline(rect, arcade.color.WHITE, border_width=4)
        arcade.draw_text(
            "CHOOSE YOUR COLOR",
            cx, cy, arcade.color.WHITE,
            font_size=int(height * 0.025),
            anchor_x="center", anchor_y="center", bold=True
        )

        self.choose_color_button_bounds = (
            rect.left, rect.left + rect.width,
            rect.bottom, rect.bottom + rect.height
        )

    def draw_color_buttons(self):
        """Draw the initial 'Choose Your Color' button"""
        width, height = self.sw(), self.sh()

        card_w = max(100, min(160, int(height * 0.12)))
        card_h = int(card_w * 4 / 3)  # keep card aspect ratio
        spacing = max(16, int(card_w * 0.18))

        total_w = card_w * len(self.player_colors) + spacing * (len(self.player_colors) - 1)
        start_x = (width - total_w) / 2 + card_w / 2
        y = height * 0.35

        self.color_buttons = []
        for i, (name, _) in enumerate(self.player_colors):
            x = start_x + i * (card_w + spacing)
            tex = self.card_textures[name]
            rect = self._centered_rect(x, y, card_w, card_h)

            arcade.draw_texture_rect(tex, rect)

            selected = (self.selected_color == name)
            arcade.draw_rect_outline(
                rect,
                arcade.color.YELLOW if selected else arcade.color.WHITE,
                border_width=5 if selected else 2
            )

            label_color = arcade.color.BLACK if name in ("White", "Yellow") else arcade.color.WHITE
            arcade.draw_text(
                name, x, y, label_color,
                font_size=int(height * 0.022),
                anchor_x="center", anchor_y="center", bold=True
            )

            self.color_buttons.append({
                "color": name,
                "bounds": (rect.left, rect.left + rect.width,
                           rect.bottom, rect.bottom + rect.height)
            })

    def draw_start_button(self):
        """Draw the start button"""
        width, height = self.sw(), self.sh()

        btn_w = max(180, min(260, int(width * 0.16)))
        btn_h = max(54, min(86, int(height * 0.08)))
        cx, cy = width * 0.50, height * 0.08

        tex = arcade.make_soft_square_texture(2, (34, 139, 34), outer_alpha=255)
        rect = self._centered_rect(cx, cy, btn_w, btn_h)
        arcade.draw_texture_rect(tex, rect)
        arcade.draw_rect_outline(rect, arcade.color.WHITE, border_width=3)
        arcade.draw_text(
            "START GAME", cx, cy, arcade.color.WHITE,
            font_size=int(height * 0.03),
            anchor_x="center", anchor_y="center", bold=True
        )

        self.start_button_bounds = (
            rect.left, rect.left + rect.width,
            rect.bottom, rect.bottom + rect.height
        )

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse clicks"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Stage 1: Check if "Choose Your Color" button was clicked
            if not self.showing_colors and self.choose_color_button_bounds:
                left, right, bottom, top = self.choose_color_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.showing_colors = True
                    return

            # Stage 2: Check color button clicks
            if self.showing_colors:
                for btn in self.color_buttons:
                    left, right, bottom, top = btn['bounds']
                    if left <= x <= right and bottom <= y <= top:
                        self.selected_color = btn['color']
                        return

                # Check start button click
                if self.selected_color and self.start_button_bounds:
                    left, right, bottom, top = self.start_button_bounds
                    if left <= x <= right and bottom <= y <= top:
                        # Import GameView here to avoid circular import
                        from board import GameView

                        # Create and show game view with selected color
                        player_obj = player.Player(self.selected_color)
                        globals.player_obj = player_obj
                        game_view = GameView(player_obj)
                        game_view.reset()
                        self.window.show_view(game_view)

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle key presses"""
        if symbol == arcade.key.ESCAPE:
            # If showing colors, go back to main screen
            if self.showing_colors:
                self.showing_colors = False
                self.selected_color = None
            else:
                # Otherwise close the window
                self.window.close()
