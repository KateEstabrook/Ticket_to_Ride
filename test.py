"""
Ticket to Ride test

Simple program to show basic sprite usage.
"""

import arcade

PLAYER_SCALING = 0.05

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Ticket to Ride"

# First city position (kansas city) on the original background image
CITY_IMG_X = 583
CITY_IMG_Y = 368
TOP_LEFT_INPUT = True
CITY_SCALE = 0.01       # optional scale for the city sprite


class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        """Initializer"""

        # Call the parent class initializer
        super().__init__()

        # Background image will be stored in this variable
        self.background = arcade.load_texture("images/board.png")

        city_texture = "images/city.png"
        self.city = arcade.Sprite(city_texture)
        self.city_list = arcade.SpriteList()
        self.city_list.append(self.city)
        self.place_city(CITY_IMG_X, CITY_IMG_Y, top_left=TOP_LEFT_INPUT, scale=CITY_SCALE)

        # Preload the yellow version and add it as an extra texture (index 1)
        self.city.append_texture(arcade.load_texture("images/button_yellow.png"))
        self.city.set_texture(0)  # ensure we start with the default texture (index 0)

        # Variables that will hold sprite lists
        self.player_sprite = arcade.Sprite(
            "images/cursor.png",
            scale=PLAYER_SCALING,
        )
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        # Set the background color
        self.background_color = arcade.color.AMAZON

    def reset(self):
        """Restart the game."""
        # Set up the player
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

    def img_to_screen(self, ix: float, iy: float, *, top_left: bool = False) -> tuple[float, float]:
        """
        Convert a coordinate on the background image (in image pixels) to the window/screen coordinate.
        Works because you draw the background stretched to WINDOW_*.
        """
        # Flip Y if coordinates were measured from the image's top edge
        if top_left:
            iy = self.background.height - iy

        sx = WINDOW_WIDTH / self.background.width
        sy = WINDOW_HEIGHT / self.background.height
        return ix * sx, iy * sy

    def place_city(self, ix: float, iy: float, *, top_left: bool = False, scale: float | None = None) -> None:
        """
        Position the city sprite using image-pixel coordinates.
        """
        x, y = self.img_to_screen(ix, iy, top_left=top_left)
        self.city.center_x = x
        self.city.center_y = y
        if scale is not None:
            self.city.scale = scale

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        # Draw all the sprites.
        self.city_list.draw()
        self.player_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Generate a list of all cities that collided with the cursor
            city_hit = arcade.check_for_collision_with_list(self.player_sprite, self.city_list)

            # Any city we’re touching -> show yellow (texture index 1)
            for city in city_hit:
                city.set_texture(1)
                city.scale = 0.016

            # Any city we’re NOT touching -> revert to default (texture index 0)
            for city in self.city_list:
                if city not in city_hit:
                    city.set_texture(0)
                    city.scale = 0.01


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            self.reset()
        elif symbol == arcade.key.ESCAPE:
            self.window.close()


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and set up the GameView
    game = GameView()
    game.reset()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()