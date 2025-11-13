"""
Win Screen for Ticket to Ride
"""

import arcade
import constants as c

class WinScreenView(arcade.View):
    """Win screen showing final results"""

    def __init__(self, longest_route_length=0):
        super().__init__()

        # Store the longest route length
        self.longest_route_length = longest_route_length
        self.bg_tex = arcade.load_texture("images/menu_screen.png")

        # Initialize players as None, will be set from main
        self.players = None


    def sw(self) -> int:
        """Window width (falls back to constants if needed)."""
        return getattr(self.window, "width", c.SCREEN_WIDTH)

    def sh(self) -> int:
        """Window height (falls back to constants if needed)."""
        return getattr(self.window, "height", c.SCREEN_HEIGHT)

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

    def on_draw(self):
        """Render the win screen"""
        self.clear()

        width, height = self.sw(), self.sh()

        # Draw background image
        bg_rect = self._cover_scale_rect(self.bg_tex.width, self.bg_tex.height, width, height)
        arcade.draw_texture_rect(self.bg_tex, bg_rect)

        # Main results container
        self.draw_results_container(width, height)

        # Instructions at bottom
        self.draw_instructions(width, height)

    def draw_results_container(self, width, height):
        """Draw the main results container with styled rectangle"""
        # Main container background
        container_w = max(500, min(850, int(width * 0.8)))
        container_h = max(400, min(650, int(height * 0.7)))
        cx, cy = width // 2, height // 2

        # Create styled container
        tex = arcade.make_soft_square_texture(2, (0, 0, 0, 0), outer_alpha=0)
        rect = self._centered_rect(cx, cy, container_w, container_h)
        arcade.draw_texture_rect(tex, rect)

        # Title section with its own styled rectangle
        self.draw_title_section(width, height, container_w, container_h, cx, cy)

        # Player results section
        self.draw_player_results(width, height, container_w, container_h, cx, cy)

    def draw_title_section(self, width, height, container_w, container_h, container_cx, container_cy):
        """Draw the title section with styled background"""
        title_w = container_w * 0.9
        title_h = max(80, min(120, int(container_h * 0.2)))
        title_cx, title_cy = container_cx, container_cy + container_h * 0.45

        # Title background
        title_tex = arcade.make_soft_square_texture(2, (154, 30, 31), outer_alpha=255)
        title_rect = self._centered_rect(title_cx, title_cy, title_w, title_h)
        arcade.draw_texture_rect(title_tex, title_rect)
        arcade.draw_rect_outline(title_rect, arcade.color.WHITE, border_width=3)

        # Title text
        arcade.draw_text("JOURNEY COMPLETE!",
                        title_cx, title_cy + 10,
                        arcade.color.GOLD, 42,
                        anchor_x="center", anchor_y="center")

    def draw_player_results(self, width, height, container_w, container_h, container_cx, container_cy):
        """Draw player results with styled entries"""
        # Sort players by points
        sorted_players = sorted(self.players, key=lambda x: x["points"], reverse=True)

        # Player entry dimensions
        entry_w = container_w * 0.85
        entry_h = max(60, min(80, int(container_h * 0.12)))
        start_y = container_cy + container_h * 0.25

        for i, player in enumerate(sorted_players):
            entry_y = start_y - (i * (entry_h + 25))

            # Player entry background
            if i == 0:  # 1st place
                entry_color = (251, 238, 204)
                border_color = arcade.color.GOLD
                border_width = 6
            else:
                entry_color = (251, 238, 204)
                border_color = arcade.color.DARK_BROWN
                border_width = 3  #

            entry_tex = arcade.make_soft_square_texture(2, entry_color, outer_alpha=255)
            entry_rect = self._centered_rect(container_cx, entry_y, entry_w, entry_h)
            arcade.draw_texture_rect(entry_tex, entry_rect)
            arcade.draw_rect_outline(entry_rect, border_color, border_width=border_width)

            # Player rank and name
            rank_text = f"{i + 1}. {player['name']}"
            arcade.draw_text(rank_text,
                             entry_rect.left + 20, entry_y,
                             player["color"], 24,
                             anchor_y="center", bold=True)

            # Points
            points_text = f"{player['points']} pts"
            arcade.draw_text(points_text,
                             entry_rect.right - 20, entry_y,
                             arcade.color.BLACK, 24,
                             anchor_x="right", anchor_y="center",
                             bold=True)

            # Longest path indicator
            if player["longest_path"]:
                # Position rectangle to the right of the player entry
                badge_x = entry_rect.right + 150
                badge_y = entry_y
                badge_w = 250
                badge_h = 35

                # Draw the badge
                badge_tex = arcade.make_soft_square_texture(2, arcade.color.FOREST_GREEN, outer_alpha=255)
                badge_rect = self._centered_rect(badge_x, badge_y, badge_w, badge_h)
                arcade.draw_texture_rect(badge_tex, badge_rect)
                arcade.draw_rect_outline(badge_rect, arcade.color.WHITE, border_width=2)

                # Draw text inside the badge
                arcade.draw_text("Longest Continuous Route!",
                                 badge_x, badge_y,
                                 arcade.color.WHITE, 14,
                                 anchor_x="center", anchor_y="center",
                                 bold=True)

    def draw_instructions(self, width, height):
        """Draw instructions at bottom with styled rectangle"""
        instructions_w = max(300, min(400, int(width * 0.3)))
        instructions_h = max(40, min(60, int(height * 0.06)))
        cx, cy = width // 2, height * 0.22

        # Instructions background
        instructions_tex = arcade.make_soft_square_texture(2, (251, 238, 204), outer_alpha=255)
        instructions_rect = self._centered_rect(cx, cy, instructions_w, instructions_h)
        arcade.draw_texture_rect(instructions_tex, instructions_rect)
        arcade.draw_rect_outline(instructions_rect, arcade.color.BLACK, border_width=3)

        arcade.draw_text("Press ESC to close",
                        cx, cy,
                        arcade.color.BLACK, 16,
                        anchor_x="center", anchor_y="center")

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle key presses"""
        if symbol == arcade.key.ESCAPE:
            self.window.close()


def main():
    """Main function to run the win screen independently"""
    window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, "Ticket to Ride - Results")

    # Test data
    players = [
        {"name": "You", "color": (171, 38, 2), "points": 127, "longest_path": False},
        {"name": "Yellow", "color": (241, 193, 19), "points": 115, "longest_path": True},
        {"name": "Blue", "color": (10, 85, 161), "points": 98, "longest_path": False},
        {"name": "Green", "color": (115, 143, 43), "points": 85, "longest_path": False}
    ]

    # Create win screen with longest route length
    win_view = WinScreenView(longest_route_length=45)
    # Set players after creating the view
    win_view.players = players
    window.show_view(win_view)
    arcade.run()


if __name__ == "__main__":
    main()
