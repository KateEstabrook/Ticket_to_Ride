"""
Ticket to Ride Board
With dictionaries for cities including paths
"""

import arcade

PLAYER_SCALING = 0.05

WINDOW_WIDTH = 1150
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Ticket to Ride"

# First city position (kansas city) on the original background image
CITY_IMG_X = 583
CITY_IMG_Y = 368
TOP_LEFT_INPUT = True
CITY_SCALE = 0.01       # optional scale for the city sprite

CITY_SCALE = 0.0111
CITY_SCALE_YELLOW = 0.016

CITIES = {
    "Calgary" : {
        "CITY_IMG_X" : 587, "CITY_IMG_Y" : 212
    },
    "Vancouver" : {
        "CITY_IMG_X" : 266, "CITY_IMG_Y" : 255
    },
    "Seattle": {
        "CITY_IMG_X" : 250, "CITY_IMG_Y" : 400
    },
    "Portland": {

    },
    "San Francisco": {

    },
    "Los Angeles": {

    },
    "Helena": {

    },
    "Salt Lake City": {

    },
    "Las Vegas": {

    },
    "Phoenix": {

    },
    "Winnipeg": {

    },
    "Denver": {

    },
    "Santa Fe": {

    },
    "El Paso": {

    },
    "Duluth": {

    },
    "Omaha": {

    },
    "Kansas City": {

    },
    "Oklahoma City": {

    },
    "Dallas": {

    },
    "Houston": {

    },
    "Sault St. Marie": {

    },
    "Chicago": {

    },
    "Saint Louis": {

    },
    "Little Rock": {

    },
    "New Orleans": {

    },
    "Toronto": {

    },
    "Pittsburgh": {

    },
    "Nashville": {

    },
    "Atlanta": {

    },
    "Charleston": {

    },
    "Miami": {

    },
    "Raleigh": {

    },
    "Washington": {

    },
    "New York": {

    },
    "Boston": {

    },
    "Montreal": {

    }
          }

ROUTES = {
    "Vancouver": {
        "Seattle": 1,
        "Calgary": 3
    },
    "Seattle": {
        "Portland": 1,
        "Calgary": 4,
        "Vancouver": 1,
        "Helena": 6
    },
    "Portland": {
        "San Francisco": 5,
        "Seattle": 1,
        "Salt Lake City": 6
    },
    "San Francisco": {
        "Portland": 5,
        "Salt Lake City": 5,
        "Los Angeles": 3
    },
    "Los Angeles": {
        "San Francisco": 3,
        "Las Vegas": 2,
        "Phoenix": 3,
        "El Paso": 6
    },
    "Calgary": {
        "Vancouver": 3,
        "Seattle": 4,
        "Helena": 4
    },
    "Helena": {
        "Calgary": 4,
        "Seattle": 6,
        "Salt Lake City": 3,
        "Winnipeg": 4,
        "Duluth": 6,
        "Omaha": 5,
        "Denver": 4
    },
    "Salt Lake City": {
        "Portland": 6,
        "San Francisco": 5,
        "Las Vegas": 3,
        "Denver": 3,
        "Helena": 3
    },
    "Las Vegas": {
        "Salt Lake City": 3,
        "Los Angeles": 2
    },
    "Phoenix": {
        "Los Angeles": 3,
        "Denver": 5,
        "Santa Fe": 3,
        "El Paso": 3
    },
    "Winnipeg": {
        "Calgary": 6,
        "Helena": 4,
        "Duluth": 4,
        "Sault St. Marie": 6
    },
    "Denver": {
        "Helena": 4,
        "Salt Lake City": 3,
        "Phoenix": 5,
        "Omaha": 4,
        "Oklahoma City": 4,
        "Santa Fe": 2,
        "Kansas City": 4
    },
    "Santa Fe": {
        "Denver": 2,
        "Phoenix": 3,
        "El Paso": 2,
        "Oklahoma City": 3
    },
    "El Paso": {
        "Santa Fe": 2,
        "Phoenix": 3,
        "Los Angeles": 6,
        "Oklahoma City": 5,
        "Dallas": 4,
        "Houston": 6
    },
    "Duluth": {
        "Winnipeg": 4,
        "Helena": 6,
        "Omaha": 2,
        "Chicago": 3,
        "Toronto": 6,
        "Sault St. Marie": 3
    },
    "Omaha": {
        "Duluth": 2,
        "Helena": 5,
        "Chicago": 4,
        "Kansas City": 1,
        "Denver": 4
    },
    "Kansas City": {
        "Omaha": 1,
        "Denver": 4,
        "Saint Louis": 2,
        "Oklahoma City": 2
    },
    "Oklahoma City": {
        "Kansas City": 2,
        "Denver": 4,
        "El Paso": 5,
        "Dallas": 2,
        "Little Rock": 2,
        "Santa Fe": 3
    },
    "Dallas": {
        "El Paso": 4,
        "Houston": 1,
        "Oklahoma City": 2,
        "Little Rock":2
    },
    "Houston": {

    },
    "Sault St. Marie": {

    },
    "Chicago": {

    },
    "Saint Louis": {

    },
    "Little Rock": {

    },
    "New Orleans": {

    },
    "Toronto": {

    },
    "Pittsburgh": {

    },
    "Nashville": {

    },
    "Atlanta": {

    },
    "Charleston": {

    },
    "Miami": {

    },
    "Raleigh": {

    },
    "Washington": {

    },
    "New York": {

    },
    "Boston": {

    },
    "Montreal": {

    }
}


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

        # One list for all city sprites (create it ONCE)
        self.city_list = arcade.SpriteList()

        # Load textures once
        base_tex = arcade.load_texture("images/city.png")
        hover_tex = arcade.load_texture("images/button_yellow.png")

        # Build sprites from CITIES
        for city in CITIES:
            # Skip cities with no coordinates yet
            if "CITY_IMG_X" not in CITIES[city].keys() or "CITY_IMG_Y" not in CITIES[city].keys():
                continue

            # Create one sprite per city
            self.city = arcade.Sprite()  # keep your place_city logic (uses self.city)
            self.city.append_texture(base_tex)
            self.city.append_texture(hover_tex)
            self.city.set_texture(0)
            self.city.scale = CITY_SCALE

            # Position it using your helper
            self.place_city(
                CITIES[city]["CITY_IMG_X"], CITIES[city]["CITY_IMG_Y"],
                top_left=True, scale=None  # scale already set above
            )

            # Add to the shared list
            self.city_list.append(self.city)

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