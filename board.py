"""
Ticket to Ride Board
With dictionaries for cities including paths
"""

import arcade

PLAYER_SCALING = 0.05

# These are just a seed size for window creation; we switch to fullscreen after.
WINDOW_WIDTH = 1150
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Ticket to Ride"

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
    Fullscreen view with letterboxed board centered on screen.
    """

    def __init__(self):
        super().__init__()

        # Black bars around the board
        arcade.set_background_color(arcade.color.BLACK)

        # Load the board image (its intrinsic size defines the aspect ratio)
        self.background = arcade.load_texture("images/board.png")

        # Layout values computed from current window size
        self.fit_scale = 1.0
        self.board_left = 0.0
        self.board_bottom = 0.0

        # Compute layout BEFORE placing cities
        self._compute_layout()

        # Build city sprites
        self.city_list = arcade.SpriteList()
        base_tex = arcade.load_texture("images/city.png")
        hover_tex = arcade.load_texture("images/button_yellow.png")

        for name, d in CITIES.items():
            if "CITY_IMG_X" not in d or "CITY_IMG_Y" not in d:
                continue
            spr = arcade.Sprite()
            spr.append_texture(base_tex)
            spr.append_texture(hover_tex)
            spr.set_texture(0)
            spr.scale = CITY_SCALE

            # Keep original image coords on the sprite so we can re-place on resize
            spr._img_ix = d["CITY_IMG_X"]
            spr._img_iy = d["CITY_IMG_Y"]

            spr.center_x, spr.center_y = self.img_to_screen(spr._img_ix, spr._img_iy, top_left=True)
            self.city_list.append(spr)

        self.selected_cities = []

        # Cursor sprite
        self.player_sprite = arcade.Sprite("images/cursor.png", scale=PLAYER_SCALING)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Hide system mouse
        self.window.set_mouse_visible(False)

    def _compute_layout(self):
        """Compute scale and offsets so the board is centered with black borders."""
        w, h = self.window.get_size()
        img_w = self.background.width
        img_h = self.background.height

        # Fit scale that preserves the board aspect ratio (letterbox/pillarbox)
        self.fit_scale = min(w / img_w, h / img_h)

        render_w = img_w * self.fit_scale
        render_h = img_h * self.fit_scale
        self.board_left = (w - render_w) / 2
        self.board_bottom = (h - render_h) / 2

    def img_to_screen(self, ix: float, iy: float, *, top_left: bool = False) -> tuple[float, float]:
        """
        Map pixel coords on the board image -> screen coords using fit scale + offsets.
        """
        if top_left:
            iy = self.background.height - iy  # convert top-left Y to bottom-left Y
        x = self.board_left + ix * self.fit_scale
        y = self.board_bottom + iy * self.fit_scale
        return x, y

    def reset(self):
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

    def on_draw(self):
        self.clear()  # clears to black

        # Draw the board centered with preserved aspect ratio
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                self.board_left,
                self.board_bottom,
                self.background.width * self.fit_scale,
                self.background.height * self.fit_scale,
            ),
        )

        self.city_list.draw()
        self.player_list.draw()

    def on_resize(self, width: int, height: int):
        """
        Recompute layout and re-place city sprites when window size changes
        (including entering/exiting fullscreen on some platforms).
        """
        super().on_resize(width, height)
        self._compute_layout()
        for spr in self.city_list:
            spr.center_x, spr.center_y = self.img_to_screen(spr._img_ix, spr._img_iy, top_left=True)

    # ---- input ----
    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            tip_x = self.player_sprite.center_x - self.player_sprite.width / 3
            tip_y = self.player_sprite.center_y + self.player_sprite.height / 3

            hits = arcade.get_sprites_at_point((tip_x, tip_y), self.city_list)

            if not hits:
                return  # avoid index error if clicking empty space

            city = hits[0]

            if city in self.selected_cities:
                city.set_texture(0)
                city.scale = CITY_SCALE
                self.selected_cities.remove(city)
                return

            if len(self.selected_cities) == 2:
                newest = self.selected_cities.pop(1)
                newest.set_texture(0)
                newest.scale = CITY_SCALE

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
    # Create a window (seed size), then switch to fullscreen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.set_fullscreen(True)

    # Create and set up the GameView
    game = GameView()
    game.reset()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()
