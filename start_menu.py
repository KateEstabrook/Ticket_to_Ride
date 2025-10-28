"""
Start Menu View for Ticket to Ride
Add this class to your main game file, before the GameView class
"""

import arcade
from arcade import SpriteList
import globals
import constants as c
import player

class StartMenuView(arcade.View):
    """Start menu where players choose their color"""

    def __init__(self):
        super().__init__()
        # Create a sprite for the background
        self.background_sprite = arcade.Sprite("images/menu_screen.png")

        # Calculate scale to fit screen
        scale_x = c.SCREEN_WIDTH / self.background_sprite.width
        scale_y = c.WINDOW_HEIGHT / self.background_sprite.height

        # Use the smaller scale to fit entirely, or larger to fill screen
        self.background_sprite.scale = 0.415  # Fit inside
        # OR
        # self.background_sprite.scale = max(scale_x, scale_y)  # Fill screen

        # Center it
        self.background_sprite.center_x = c.SCREEN_WIDTH // 2 - 200
        self.background_sprite.center_y = c.WINDOW_HEIGHT // 2
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

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Render the start menu"""
        self.clear()

        # Draw background
        tmp = SpriteList()
        tmp.append(self.background_sprite)
        tmp.draw()

        if not self.showing_colors:
            # Stage 1: Show only "Choose Your Color" button
            self.draw_choose_color_button()
        else:
            # Stage 2: Show color selection and start button

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
        button_width = 350
        button_height = 80
        button_x = c.SCREEN_WIDTH // 2 - 192
        button_y = c.WINDOW_HEIGHT * 0.15

        # Draw button background
        button_texture = arcade.make_soft_square_texture(2, (154, 30, 31), outer_alpha=255)
        button_rect = arcade.LBWH(
            button_x - button_width // 2,
            button_y - button_height // 2,
            button_width,
            button_height
        )
        arcade.draw_texture_rect(button_texture, button_rect)

        # Draw button border
        arcade.draw_rect_outline(
            button_rect,
            arcade.color.WHITE,
            border_width=4
        )

        # Draw button text
        arcade.draw_text(
            "CHOOSE YOUR COLOR",
            button_x,
            button_y,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Store button bounds
        self.choose_color_button_bounds = (
            button_x - button_width // 2,   # left
            button_x + button_width // 2,   # right
            button_y - button_height // 2,  # bottom
            button_y + button_height // 2   # top
        )

    def draw_color_buttons(self):
        """Draw the color selection buttons"""
        button_width = 120
        button_height = 160
        spacing = 20

        # Calculate total width to center the buttons
        total_width = (button_width * len(self.player_colors) +
                      spacing * (len(self.player_colors) - 1))
        start_x = c.SCREEN_WIDTH // 2 - 450
        button_y = c.WINDOW_HEIGHT * 0.35

        self.color_buttons = []

        for i, (color_name, filename) in enumerate(self.player_colors):
            button_x = start_x + i * (button_width + spacing) + button_width // 2

            # Draw card image
            texture = self.card_textures[color_name]
            rect = arcade.LBWH(
                button_x - button_width // 2,
                button_y - button_height // 2,
                button_width,
                button_height
            )
            arcade.draw_texture_rect(texture, rect)

            # Draw border (yellow if selected)
            if self.selected_color == color_name:
                border_color = arcade.color.YELLOW
                border_width = 5
            else:
                border_color = arcade.color.WHITE
                border_width = 2

            arcade.draw_rect_outline(
                rect,
                border_color,
                border_width=border_width
            )

            # Draw color name
            text_color = arcade.color.WHITE
            if color_name in ["WHITE", "YELLOW"]:
                text_color = arcade.color.BLACK

            arcade.draw_text(
                color_name,
                button_x,
                button_y,
                text_color,
                font_size=16,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            # Store button bounds for click detection
            self.color_buttons.append({
                'color': color_name,
                'bounds': (
                    button_x - button_width // 2,   # left
                    button_x + button_width // 2,   # right
                    button_y - button_height // 2,  # bottom
                    button_y + button_height // 2   # top
                )
            })

    def draw_start_button(self):
        """Draw the start game button"""
        button_width = 200
        button_height = 60
        button_x = c.SCREEN_WIDTH // 2 - 192
        button_y = c.WINDOW_HEIGHT * 0.08

        # Draw button background
        button_texture = arcade.make_soft_square_texture(2, (34, 139, 34), outer_alpha=255)
        button_rect = arcade.LBWH(
            button_x - button_width // 2,
            button_y - button_height // 2,
            button_width,
            button_height
        )
        arcade.draw_texture_rect(button_texture, button_rect)

        # Draw button border
        arcade.draw_rect_outline(
            button_rect,
            arcade.color.WHITE,
            border_width=3
        )

        # Draw button text
        arcade.draw_text(
            "START GAME",
            button_x,
            button_y,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        # Store button bounds
        self.start_button_bounds = (
            button_x - button_width // 2,   # left
            button_x + button_width // 2,   # right
            button_y - button_height // 2,  # bottom
            button_y + button_height // 2   # top
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
                        game_view = GameView(player_obj=player.Player(self.selected_color))
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