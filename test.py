import arcade

BOARD_WIDTH = 1150
BOARD_HEIGHT = 720

CITY_POINTS = {
    "Calgary": (587, 212),
    "Vancouver": (100, 600),
    "Seattle": (140, 560),
    "Portland": (160, 480),
    "Los Angeles": (900, 80),
}

CITY_MARKER_RADIUS = 8


class FullscreenGame(arcade.Window):
    def __init__(self):
        # Create windowed mode first (must be windowed at init on macOS)
        screen_width, screen_height = arcade.get_display_size()
        super().__init__(screen_width, screen_height, "Ticket to Ride", resizable=False)

        # Track window size and board scale/offset
        self.win_width, self.win_height = self.get_size()
        self.board_scale = 1
        self.offset_x = 0
        self.offset_y = 0

        arcade.set_background_color(arcade.color.ALMOND)

    def on_show(self):
        """
        Called when the window is shown. This is the safe place to switch to fullscreen on macOS.
        """
        self.set_fullscreen(True)
        self.win_width, self.win_height = self.get_size()
        self._update_scale_and_offset()

    def _update_scale_and_offset(self):
        scale_x = self.win_width / BOARD_WIDTH
        scale_y = self.win_height / BOARD_HEIGHT
        self.board_scale = min(scale_x, scale_y)
        self.offset_x = (self.win_width - BOARD_WIDTH * self.board_scale) / 2
        self.offset_y = (self.win_height - BOARD_HEIGHT * self.board_scale) / 2

    def board_to_screen(self, bx, by):
        sx = self.offset_x + bx * self.board_scale
        sy = self.offset_y + by * self.board_scale
        return sx, sy

    def on_draw(self):
        arcade.start_render()
        left = self.offset_x
        bottom = self.offset_y
        right = left + BOARD_WIDTH * self.board_scale
        top = bottom + BOARD_HEIGHT * self.board_scale

        arcade.draw_lrtb_rectangle_filled(left, right, top, bottom, arcade.color.LIGHT_GRAY)
        arcade.draw_lrtb_rectangle_outline(left, right, top, bottom, arcade.color.GRAY, 4)

        for name, (bx, by) in CITY_POINTS.items():
            sx, sy = self.board_to_screen(bx, by)
            r = CITY_MARKER_RADIUS * self.board_scale
            arcade.draw_circle_filled(sx, sy, r, arcade.color.RED)
            arcade.draw_text(name, sx + 10, sy + 10, arcade.color.BLACK, font_size=max(10, int(12 * self.board_scale)))

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()


def main():
    window = FullscreenGame()
    arcade.run()


if __name__ == "__main__":
    main()
