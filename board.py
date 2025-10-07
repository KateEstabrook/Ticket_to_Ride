"""
Ticket to Ride Board
With dictionaries for cities including paths
"""

import arcade
import platform

PLAYER_SCALING = 0.05

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
WINDOW_TITLE = "Ticket to Ride"
if platform.system() == "Darwin":  # macOS
    WINDOW_WIDTH = SCREEN_WIDTH
    WINDOW_HEIGHT = SCREEN_HEIGHT - 115

else:
    WINDOW_WIDTH = SCREEN_WIDTH - 400
    WINDOW_HEIGHT = SCREEN_HEIGHT - 180

BOARD_WIDTH = 1150
BOARD_HEIGHT = 720
BOARD_LEFT = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_BOTTOM = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2

CITY_SCALE = 0.0111
CITY_SCALE_YELLOW = 0.016


CITIES = {
    "Calgary": {"CITY_IMG_X": 587, "CITY_IMG_Y": 212},
    "Vancouver": {"CITY_IMG_X": 266, "CITY_IMG_Y": 255},
    "Seattle": {"CITY_IMG_X": 261, "CITY_IMG_Y": 390},
    "Portland": {"CITY_IMG_X": 207, "CITY_IMG_Y": 512},
    "San Francisco": {"CITY_IMG_X": 173, "CITY_IMG_Y": 995},
    "Los Angeles": {"CITY_IMG_X": 362, "CITY_IMG_Y": 1250},
    "Helena": {"CITY_IMG_X": 832, "CITY_IMG_Y": 535},
    "Salt Lake City": {"CITY_IMG_X": 655, "CITY_IMG_Y": 838},
    "Las Vegas": {"CITY_IMG_X": 520, "CITY_IMG_Y": 1108},
    "Phoenix": {"CITY_IMG_X": 656, "CITY_IMG_Y": 1268},
    "Winnipeg": {"CITY_IMG_X": 1134, "CITY_IMG_Y": 238},
    "Denver": {"CITY_IMG_X": 974, "CITY_IMG_Y": 915},
    "Santa Fe": {"CITY_IMG_X": 956, "CITY_IMG_Y": 1134},
    "El Paso": {"CITY_IMG_X": 944, "CITY_IMG_Y": 1355},
    "Duluth": {"CITY_IMG_X": 1410, "CITY_IMG_Y": 520},
    "Omaha": {"CITY_IMG_X": 1334, "CITY_IMG_Y": 747},
    "Kansas City": {"CITY_IMG_X": 1385, "CITY_IMG_Y": 870},
    "Oklahoma City": {"CITY_IMG_X": 1338, "CITY_IMG_Y": 1082},
    "Dallas": {"CITY_IMG_X": 1385, "CITY_IMG_Y": 1297},
    "Houston": {"CITY_IMG_X": 1486, "CITY_IMG_Y": 1395},
    "Sault St. Marie": {"CITY_IMG_X": 1720, "CITY_IMG_Y": 364},
    "Chicago": {"CITY_IMG_X": 1708, "CITY_IMG_Y": 674},
    "Saint Louis": {"CITY_IMG_X": 1600, "CITY_IMG_Y": 874},
    "Little Rock": {"CITY_IMG_X": 1558, "CITY_IMG_Y": 1092},
    "New Orleans": {"CITY_IMG_X": 1715, "CITY_IMG_Y": 1365},
    "Toronto": {"CITY_IMG_X": 1986, "CITY_IMG_Y": 411},
    "Pittsburgh": {"CITY_IMG_X": 2029, "CITY_IMG_Y": 635},
    "Nashville": {"CITY_IMG_X": 1828, "CITY_IMG_Y": 970},
    "Atlanta": {"CITY_IMG_X": 1950, "CITY_IMG_Y": 1052},
    "Charleston": {"CITY_IMG_X": 2180, "CITY_IMG_Y": 1071},
    "Miami": {"CITY_IMG_X": 2259, "CITY_IMG_Y": 1459},
    "Raleigh": {"CITY_IMG_X": 2112, "CITY_IMG_Y": 912},
    "Washington": {"CITY_IMG_X": 2255, "CITY_IMG_Y": 747},
    "New York": {"CITY_IMG_X": 2233, "CITY_IMG_Y": 526},
    "Boston": {"CITY_IMG_X": 2363, "CITY_IMG_Y": 346},
    "Montreal": {"CITY_IMG_X": 2189, "CITY_IMG_Y": 200}
}

ROUTES = {
    "Vancouver": {"Seattle": 1, "Calgary": 3},
    "Seattle": {"Portland": 1, "Calgary": 4, "Vancouver": 1, "Helena": 6},
    "Portland": {"San Francisco": 5, "Seattle": 1, "Salt Lake City": 6},
    "San Francisco": {"Portland": 5, "Salt Lake City": 5, "Los Angeles": 3},
    "Los Angeles": {"San Francisco": 3, "Las Vegas": 2, "Phoenix": 3, "El Paso": 6},
    "Calgary": {"Vancouver": 3, "Seattle": 4, "Helena": 4, "Winnipeg": 6},
    "Helena": {"Calgary": 4, "Seattle": 6, "Salt Lake City": 3, "Winnipeg": 4, "Duluth": 6, "Omaha": 5, "Denver": 4},
    "Salt Lake City": {"Portland": 6, "San Francisco": 5, "Las Vegas": 3, "Denver": 3, "Helena": 3},
    "Las Vegas": {"Salt Lake City": 3, "Los Angeles": 2},
    "Phoenix": {"Los Angeles": 3, "Denver": 5, "Santa Fe": 3, "El Paso": 3},
    "Winnipeg": {"Calgary": 6, "Helena": 4, "Duluth": 4, "Sault St. Marie": 6},
    "Denver": {"Helena": 4, "Salt Lake City": 3, "Phoenix": 5, "Omaha": 4, "Oklahoma City": 4, "Santa Fe": 2, "Kansas City": 4},
    "Santa Fe": {"Denver": 2, "Phoenix": 3, "El Paso": 2, "Oklahoma City": 3},
    "El Paso": {"Santa Fe": 2, "Phoenix": 3, "Los Angeles": 6, "Oklahoma City": 5, "Dallas": 4, "Houston": 6},
    "Duluth": {"Winnipeg": 4, "Helena": 6, "Omaha": 2, "Chicago": 3, "Toronto": 6, "Sault St. Marie": 3},
    "Omaha": {"Duluth": 2, "Helena": 5, "Chicago": 4, "Kansas City": 1, "Denver": 4},
    "Kansas City": {"Omaha": 1, "Denver": 4, "Saint Louis": 2, "Oklahoma City": 2},
    "Oklahoma City": {"Kansas City": 2, "Denver": 4, "El Paso": 5, "Dallas": 2, "Little Rock": 2, "Santa Fe": 3},
    "Dallas": {"El Paso": 4, "Houston": 1, "Oklahoma City": 2, "Little Rock": 2},
    "Houston": {"Dallas": 1, "El Paso": 6, "New Orleans": 2},
    "Sault St. Marie": {"Winnipeg": 6, "Duluth": 3, "Montreal": 5, "Toronto": 2},
    "Chicago": {"Toronto": 4, "Duluth": 3, "Omaha": 4, "Saint Louis": 2, "Pittsburgh": 3},
    "Saint Louis": {"Chicago": 2, "Pittsburgh": 5, "Nashville": 2, "Little Rock": 2, "Kansas City": 2},
    "Little Rock": {"Saint Louis": 2, "Nashville": 3, "New Orleans": 3, "Dallas": 2, "Oklahoma City": 2},
    "New Orleans": {"Little Rock": 3, "Houston": 2, "Atlanta": 4, "Miami": 6},
    "Toronto": {"Sault St. Marie": 2, "Montreal": 3, "Duluth": 6, "Chicago": 4, "Pittsburgh": 2},
    "Pittsburgh": {"Toronto": 2, "Chicago": 3, "New York": 2, "Saint Louis": 5, "Nashville": 4, "Washington": 2, "Raleigh": 2},
    "Nashville": {"Saint Louis": 2, "Pittsburgh": 4, "Little Rock": 3, "Atlanta": 1, "Raleigh": 3},
    "Atlanta": {"Nashville": 1, "Raleigh": 2, "Charleston": 2, "Miami": 5, "New Orleans": 4},
    "Charleston": {"Raleigh": 2, "Atlanta": 2, "Miami": 4},
    "Miami": {"Charleston": 4, "Atlanta": 5, "New Orleans": 6},
    "Raleigh": {"Charleston": 2, "Atlanta": 2, "Nashville": 3, "Washington": 2, "Pittsburgh": 2},
    "Washington": {"Raleigh": 2, "Pittsburgh": 2, "New York": 2},
    "New York": {"Washington": 2, "Pittsburgh": 2, "Montreal": 3, "Boston": 2},
    "Boston": {"New York": 2, "Montreal": 2},
    "Montreal": {"Boston": 2, "New York": 3, "Toronto": 3, "Sault St. Marie": 5}
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

        self.selected_cities = []  # list of selected city sprites (max. 2)

        # Variables that will hold sprite lists
        self.player_sprite = arcade.Sprite(
            "images/cursor.png",
            scale=PLAYER_SCALING,
        )
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)


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

        sx = BOARD_WIDTH / self.background.width
        sy = BOARD_HEIGHT / self.background.height
        return ix * sx + BOARD_LEFT, iy * sy + BOARD_BOTTOM

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
            arcade.LBWH(BOARD_LEFT, BOARD_BOTTOM,  BOARD_WIDTH, BOARD_HEIGHT),
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
            # fingertip = top-left corner of the cursor image
            tip_x = self.player_sprite.center_x - self.player_sprite.width / 3
            tip_y = self.player_sprite.center_y + self.player_sprite.height / 3

            # which cities are exactly under that point?
            hits = arcade.get_sprites_at_point((tip_x, tip_y), self.city_list)

            city = hits[0]

            # If this city is already selected -> deselect it
            if city in self.selected_cities:
                city.set_texture(0)
                city.scale = CITY_SCALE
                self.selected_cities.remove(city)
                return

            # Otherwise, select it; if already 2 selected, drop the newest first
            if len(self.selected_cities) == 2:
                newest = self.selected_cities.pop(1)
                newest.set_texture(0)
                newest.scale = CITY_SCALE

            # Mark this one as selected
            city.set_texture(1)
            city.scale = CITY_SCALE_YELLOW
            self.selected_cities.append(city)


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.R:
            self.reset()
        elif symbol == arcade.key.ESCAPE:
            self.window.close()


def main():
    """ Main function """
    if platform.system() == "Darwin":  # macOS
        window = arcade.Window(SCREEN_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=False)
        window.set_location(0, 0)
    else:
        window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True, resizable=False)

    game = GameView()
    game.reset()
    window.show_view(game)
    arcade.run()



if __name__ == "__main__":
    main()