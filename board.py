"""
Ticket to Ride Board
"""

import platform
import arcade
import constants as c
import random

class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self, player_color = None):
        """Initializer"""

        # Call the parent class initializer
        super().__init__()

        self.player_color = player_color

        # Background image will be stored in this variable
        self.background = arcade.load_texture("images/board_borders.png")

        self.leaderboard_lines = [
            arcade.Text("Player 0 - 312", 600, 830, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("Player 1 - 343", 600, 800, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("Player 2 - 232", 800, 830, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("Player 3 - 123", 800, 800, arcade.color.WHITE, 15, anchor_x="left"),
        ]

        text_x1, text_y1 = self.img_to_screen(2730, 1000, top_left=True)
        text_x2, text_y2 = self.img_to_screen(3030, 1000, top_left=True)
        text_x3, text_y3 = self.img_to_screen(3330, 1000, top_left=True)
        text_x4, text_y4 = self.img_to_screen(2730, 1220, top_left=True)
        text_x5, text_y5 = self.img_to_screen(3030, 1220, top_left=True)
        text_x6, text_y6 = self.img_to_screen(3330, 1220, top_left=True)
        text_x7, text_y7 = self.img_to_screen(2730, 1440, top_left=True)
        text_x8, text_y8 = self.img_to_screen(3030, 1440, top_left=True)
        text_x9, text_y9 = self.img_to_screen(3330, 1440, top_left=True)

        self.index_cards = [
            arcade.Text("2", text_x1, text_y1, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", text_x2, text_y2, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("3", text_x3, text_y3, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("1", text_x4, text_y4, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("1", text_x5, text_y5, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("2", text_x6, text_y6, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("3", text_x7, text_y7, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("2", text_x8, text_y8, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", text_x9, text_y9, arcade.color.WHITE, 13, anchor_x="left"),
        ]

        # Train pieces
        # One list for all train sprites (create it ONCE)
        self.train_list = arcade.SpriteList()
        blue_train = arcade.load_texture("images/train_piece_blue.png")
        green_train = arcade.load_texture("images/train_piece_green.png")
        red_train = arcade.load_texture("images/train_piece_red.png")
        yellow_train = arcade.load_texture("images/train_piece_yellow.png")

        # Create a mapping of city pairs to train sprites
        # Structure: {(city1, city2): [[sprites for route 1], [sprites for route 2]]}
        self.train_map = {}

        # Track which routes are taken
        # Structure: {(city1, city2): [False, False]} for double routes
        self.route_taken = {}

        # Build sprites from TRAINS
        for train, routes in c.TRAINS.items():
            self.train_map[train] = []
            self.route_taken[train] = [False] * len(routes)

            for route_data in routes:
                route_sprites = []
                positions = route_data["positions"]
                color = route_data["color"]

                for position in positions:
                    if isinstance(position, tuple) and len(position) == 3:
                        ix, iy, angle = position
                        train_sprite = arcade.Sprite()
                        train_sprite.append_texture(blue_train)
                        train_sprite.append_texture(green_train)
                        train_sprite.append_texture(red_train)
                        train_sprite.append_texture(yellow_train)
                        if self.player_color == 'BLUE':
                            train_sprite.set_texture(0)
                        elif self.player_color == 'GREEN':
                            train_sprite.set_texture(1)
                        elif self.player_color == 'RED':
                            train_sprite.set_texture(2)
                        elif self.player_color == 'YELLOW':
                            train_sprite.set_texture(3)
                        train_sprite.scale = c.TRAIN_SCALE
                        train_sprite.angle = angle
                        train_sprite.alpha = 0  # start fully transparent
                        # Store route information with the sprite
                        train_sprite.route_color = color
                        train_sprite.route_name = train
                        self.place_train_sprite(ix, iy, train_sprite, top_left=True)

                        self.train_list.append(train_sprite)
                        route_sprites.append(train_sprite)

                self.train_map[train].append(route_sprites)
        self.city_list = arcade.SpriteList()

        # Load textures
        base_tex = arcade.load_texture("images/city.png")
        hover_tex = arcade.load_texture("images/button_yellow.png")
        self.selected_color = None

        # Build sprites from CITIES
        for _, info in c.CITIES.items():
            # Skip cities with no coordinates yet
            if "CITY_IMG_X" not in info or "CITY_IMG_Y" not in info:
                continue

            # Create one sprite per city
            city = arcade.Sprite()
            city.append_texture(base_tex)
            city.append_texture(hover_tex)
            city.set_texture(0)
            city.scale = c.CITY_SCALE

            # Position it using your helper
            self.place_city(
                city, info["CITY_IMG_X"], info["CITY_IMG_Y"],
                top_left=True, scale=None
            )
            self.city_list.append(city)

        self.selected_cities = []

        # Variables that will hold sprite lists
        self.player_sprite = arcade.Sprite(
            "images/cursor.png",
            scale=c.PLAYER_SCALING,
        )

        self.card_textures = {
            name : arcade.load_texture(f"images/{filename}")
            for name, (_, _, filename) in c.PLAYER_CARDS.items()
        }

        self.card_list = arcade.SpriteList()

        for name, (sx, sy) in c.FACEUP_CARDS.items():
            card = arcade.Sprite()
            random_name = random.choice(list(self.card_textures))
            card.texture = self.card_textures[random_name]

            self.place_card(card, sx, sy, top_left=True, scale = 0.4)

            self.card_list.append(card)

        for name, (sx, sy, filename) in c.PLAYER_CARDS.items():
            card = arcade.Sprite()
            card.texture = self.card_textures[name]

            self.place_card(card, sx, sy, top_left=True, scale=0.4)

            self.card_list.append(card)

        self.card_banner = arcade.Sprite("images/card_banner.png", scale=0.4)
        cx, cy = self.img_to_screen(2850, 850, top_left=True)
        self.card_banner.center_x = cx
        self.card_banner.center_y = cy

        self.leaderboard_banner = arcade.Sprite("images/leaderboard_banner.png", scale=0.40)
        lx, ly = self.img_to_screen(1250, -30, top_left=True)
        self.leaderboard_banner.center_x = lx
        self.leaderboard_banner.center_y = ly

        self.deck = arcade.Sprite("images/deck.png", scale=0.40)
        sx, sy = self.img_to_screen(-100, 280, top_left=True)
        self.deck.center_x = sx
        self.deck.center_y = sy

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        self.showing_popup = False
        self.popup_city1 = None
        self.popup_city2 = None
        self.popup_route_length = 0
        self.color_buttons = []

    def reset(self):
        """Restart the game."""
        # Set up the player
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

    def img_to_screen(self, ix: float, iy: float, *, top_left: bool = False) -> tuple[float, float]:
        """
        Convert a coordinate on the background image (in image pixels)
        to the window/screen coordinate.
        Works because you draw the background stretched to WINDOW_*.
        """
        # Flip Y if coordinates were measured from the image's top edge
        if top_left:
            iy = self.background.height - iy

        sx = c.BOARD_WIDTH / self.background.width
        sy = c.BOARD_HEIGHT / self.background.height
        return ix * sx + c.BOARD_LEFT, iy * sy + c.BOARD_BOTTOM

    def place_city(self, city, ix: float, iy: float, *,
                   top_left: bool = False, scale: float | None = None) -> None:
        """
        Position the city sprite using image-pixel coordinates.
        """
        x, y = self.img_to_screen(ix, iy, top_left=top_left)
        city.center_x = x
        city.center_y = y
        if scale is not None:
            city.scale = scale

    def place_card(self, card, ix: float, iy: float, *,
                   top_left: bool = False, scale: float | None = None) -> None:
        """
        Position the city sprite using image-pixel coordinates.
        """
        x, y = self.img_to_screen(ix, iy, top_left=top_left)
        card.center_x = x
        card.center_y = y
        if scale is not None:
            card.scale = scale

    def place_train_sprite(self, ix: float, iy: float,
                           train_sprite: arcade.Sprite, *, top_left: bool = False) -> None:
        """
        Show train sprites for a route between connected cities
        """
        x, y = self.img_to_screen(ix, iy, top_left=top_left)
        train_sprite.center_x = x
        train_sprite.center_y = y

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(c.BOARD_LEFT, c.BOARD_BOTTOM,  c.BOARD_WIDTH, c.BOARD_HEIGHT),
        )

        # Draw all the sprites
        self.train_list.draw()
        self.city_list.draw()
        self.card_list.draw()
        for line in self.leaderboard_lines:
            line.draw()

        for line in self.index_cards:
            line.draw()

        if self.showing_popup:
            self.show_pop_up(self.popup_city1, self.popup_city2)

        tmp = arcade.SpriteList()
        tmp.append(self.card_banner)
        tmp.append(self.leaderboard_banner)
        tmp.append(self.deck)
        tmp.append(self.player_sprite)
        tmp.draw()

        for line in self.leaderboard_lines:
            line.draw()


    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        pass

    def sprite_to_name(self, spr: arcade.Sprite) -> str:
        """
        Helper to get the name of the city sprite in self.selected_cities
        """
        idx = self.city_list.index(spr)
        return list(c.CITIES.keys())[idx]


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.showing_popup:
            # Check if exit button was clicked
            if hasattr(self, 'exit_button_bounds'):
                left, right, bottom, top = self.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.showing_popup = False
                    self.deselect_all_cities()
                    self.selected_color = None
                    return

            # Check if save button was clicked
            if hasattr(self, 'save_button_bounds') and self.save_button_bounds:
                left, right, bottom, top = self.save_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    if (self.selected_color and self.valid_route_colors(
                            self.selected_color, self.popup_city1, self.popup_city2)):

                        self.showing_popup = False
                        self.claim_route(self.popup_city1, self.popup_city2)
                        self.deselect_all_cities()
                        self.selected_color = None
                    return


            # Check if color button was clicked
            selected_color = self.handle_color_selection(x, y)
            if selected_color:
                self.selected_color = selected_color
                return
            # If neither button was pressed keep going
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            # Generate a list of all cities that collided with the cursor
            # fingertip = top-left corner of the cursor image
            tip_x = self.player_sprite.center_x - self.player_sprite.width / 3
            tip_y = self.player_sprite.center_y + self.player_sprite.height / 3

            # which cities are exactly under that point?
            hits = arcade.get_sprites_at_point((tip_x, tip_y), self.city_list)

            if not hits:
                return

            city = hits[0]
            # If this city is already selected -> deselect it
            if city in self.selected_cities:
                city.set_texture(0)
                city.scale = c.CITY_SCALE
                self.selected_cities.remove(city)
                return

            if len(self.selected_cities) == 0:
                # If no city is already selected, select it
                city.set_texture(1)
                city.scale = c.CITY_SCALE_YELLOW
                self.selected_cities.append(city)
                return

            # Otherwise, select it; if already 2 selected, drop both
            if len(self.selected_cities) == 2:
                newest = self.selected_cities.pop(1)
                newest.set_texture(0)
                newest.scale = c.CITY_SCALE

                oldest = self.selected_cities.pop(0)
                oldest.set_texture(0)
                oldest.scale = c.CITY_SCALE

            first_city_name = self.sprite_to_name(self.selected_cities[0])
            second_city_name = self.sprite_to_name(city)

            if second_city_name in c.ROUTES.get(first_city_name, {}):
                # Check if there are any available routes
                city_pair = (first_city_name, second_city_name)
                reverse_pair = (second_city_name, first_city_name)

                # Determine which pair exists in TRAINS
                if city_pair in c.TRAINS:
                    pair = city_pair
                elif reverse_pair in c.TRAINS:
                    pair = reverse_pair
                else:
                    # Cities are connected but no train routes defined (shouldn't happen)
                    self.deselect_all_cities()
                    return

                # Check if any routes are available
                available_count = sum(1 for taken in self.route_taken[pair] if not taken)

                if available_count > 0:
                    # Mark this one as selected
                    city.set_texture(1)
                    city.scale = c.CITY_SCALE_YELLOW
                    self.selected_cities.append(city)

                    # Show pop-up with route information
                    self.showing_popup = True
                    self.popup_city1 = first_city_name
                    self.popup_city2 = second_city_name
                    self.popup_route_length = c.ROUTES[first_city_name][second_city_name]
                    self.selected_color = None
                    return

            # If we get here, either cities aren't connected or all routes are claimed
            self.deselect_all_cities()

    # Actions to make if specific buttons are pressed
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.reset()
        elif symbol == arcade.key.ESCAPE:
            self.window.close()

    def show_trains_between(self, city1, city2):
        """Show train sprites for a route between two connected cities."""
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)

        # Determine which pair exists
        if city_pair in self.train_map:
            pair = city_pair
        elif reverse_pair in self.train_map:
            pair = reverse_pair
        else:
            return

        # Find first available route (not taken)
        for i, taken in enumerate(self.route_taken[pair]):
            if not taken:
                # Mark this route as taken
                self.route_taken[pair][i] = True

                # Make all sprites for this route visible
                for train_sprite in self.train_map[pair][i]:
                    train_sprite.set_texture(0)
                    train_sprite.alpha = 255
                break

    def deselect_all_cities(self):
        """Deselect all currently selected cities"""
        for city in self.selected_cities:
            city.set_texture(0)
            city.scale = c.CITY_SCALE
        self.selected_cities.clear()

    def show_pop_up(self, city1, city2):
        """
        Show a white rectangle pop-up with color selection buttons using card images
        """
        # Calculate dimensions and positions
        popup_width = c.WINDOW_WIDTH * 0.4
        popup_height = c.WINDOW_HEIGHT * 0.4
        popup_x = c.WINDOW_WIDTH // 2
        popup_y = c.WINDOW_HEIGHT // 2

        # Draw white rectangle
        white_texture = arcade.make_soft_square_texture(2, (251, 238, 204), outer_alpha=255)
        arcade.draw_texture_rect(
            white_texture,
            arcade.LBWH(
                popup_x - popup_width // 2,
                popup_y - popup_height // 2,
                popup_width,
                popup_height
            )
        )

        # Define colors
        color_cards = [
            ("RED", "red.png"),
            ("BLUE", "blue.png"),
            ("GREEN", "green.png"),
            ("YELLOW", "yellow.png"),
            ("ORANGE", "orange.png"),
            ("PINK", "pink.png"),
            ("BLACK", "black.png"),
            ("WHITE", "white.png"),
            ("LOCOMOTIVE", "wild.png")
        ]

        # Card textures (images)
        card_textures = {}
        for color_name, filename in color_cards:
            card_textures[color_name] = arcade.load_texture(f"images/{filename}")

        # Button dimensions and layout
        button_width = popup_width * 0.18
        button_height = popup_height * 0.15
        horizontal_spacing = popup_width * 0.1
        vertical_spacing = popup_height * 0.03

        # Starting position for the grid
        start_x = popup_x - popup_width * 0.3
        start_y = popup_y - popup_height * -0.2

        # Store button positions for click detection
        self.color_buttons = []

        # Draw cards
        for row in range(3):
            row_x = start_x

            for col in range(3):
                index = row * 3 + col
                # Calculate button position
                button_x = row_x + col * (button_width + horizontal_spacing)
                button_y = start_y - row * (button_height + vertical_spacing)
                color_name, filename = color_cards[index]
                texture = card_textures[color_name]

                # Draw card image
                rect = arcade.LBWH(
                    button_x - button_width // 2,
                    button_y - button_height // 2,
                    button_width,
                    button_height
                )
                arcade.draw_texture_rect(texture, rect)

                # draw border
                if self.selected_color == color_name.lower():
                    border_color = arcade.color.YELLOW
                    border_width = 4
                else:
                    border_color = arcade.color.BLACK
                    border_width = 2

                arcade.draw_rect_outline(
                    rect,
                    border_color,
                    border_width=border_width
                )

                # Add text label
                text_color = arcade.color.WHITE
                # Black text for light-colored cards
                if color_name in ["WHITE", "YELLOW"]:
                    text_color = arcade.color.BLACK

                arcade.draw_text(
                    color_name,
                    button_x, button_y,
                    text_color,
                    font_size=10,
                    anchor_x="center",
                    anchor_y="center",
                    bold=True
                )

                # Store button info for click detection
                self.color_buttons.append({
                    'color': color_name.lower(),
                    'bounds': (
                        button_x - button_width // 2,  # left
                        button_x + button_width // 2,  # right
                        button_y - button_height // 2,  # bottom
                        button_y + button_height // 2  # top
                    )
                })

        # Add exit button in lower right corner
        exit_button_width = popup_width * 0.2
        exit_button_height = popup_height * 0.1
        exit_button_x = popup_x + popup_width * 0.48 - exit_button_width // 2
        exit_button_y = popup_y - popup_height * 0.45 + exit_button_height // 2

        exit_texture = arcade.make_soft_square_texture(2, c.EXIT_BUTTON, outer_alpha=255)
        exit_rect = arcade.LBWH(
            exit_button_x - exit_button_width // 2,
            exit_button_y - exit_button_height // 2,
            exit_button_width,
            exit_button_height
        )

        arcade.draw_texture_rect(exit_texture, exit_rect)
        arcade.draw_rect_outline(
            exit_rect,
            arcade.color.BLACK,
            border_width=2
        )

        arcade.draw_text(
            "EXIT",
            exit_button_x, exit_button_y,
            arcade.color.WHITE,
            font_size=12,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

        self.exit_button_bounds = (
            exit_button_x - exit_button_width // 2,  # left
            exit_button_x + exit_button_width // 2,  # right
            exit_button_y - exit_button_height // 2,  # bottom
            exit_button_y + exit_button_height // 2  # top
        )

        # Only show save button if a color has been selected
        if (self.selected_color and
                self.valid_route_colors(self.selected_color, city1, city2)):

            save_button_width = popup_width * 0.2
            save_button_height = popup_height * 0.1
            save_button_x = popup_x + popup_width * 0.25 - save_button_width // 2
            save_button_y = popup_y - popup_height * 0.45 + save_button_height // 2

            save_texture = arcade.make_soft_square_texture(2, c.SAVE_BUTTON, outer_alpha=255)
            save_rect = arcade.LBWH(
                save_button_x - save_button_width // 2,
                save_button_y - save_button_height // 2,
                save_button_width,
                save_button_height
            )

            arcade.draw_texture_rect(save_texture, save_rect)
            arcade.draw_rect_outline(
                save_rect,
                arcade.color.BLACK,
                border_width=2
            )

            arcade.draw_text(
                "SAVE",
                save_button_x, save_button_y,
                arcade.color.WHITE,
                font_size=12,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            self.save_button_bounds = (
                save_button_x - save_button_width // 2,  # left
                save_button_x + save_button_width // 2,  # right
                save_button_y - save_button_height // 2,  # bottom
                save_button_y + save_button_height // 2  # top
            )
        else:
            self.save_button_bounds = None

        # Add route information text
        route_length = self.popup_route_length
        text = f"You have selected {city1} to {city2} route (length: {route_length})"
        arcade.draw_text(
            text,
            popup_x, popup_y + popup_height * 0.45,
            arcade.color.BLACK,
            font_size=14,
            anchor_x="center",
            anchor_y="center",
            bold=True,
            align="center",
            width=popup_width * 0.8
        )

        # Add color selection prompt
        color_text = "Which color would you like to use?"
        arcade.draw_text(
            color_text,
            popup_x, popup_y + popup_height * 0.35,
            arcade.color.BLACK,
            font_size=12,
            anchor_x="center",
            anchor_y="center"
        )

        # Add selection status text
        if self.selected_color:
            status_text = f"Selected: {self.selected_color.upper()}"
            arcade.draw_text(
                status_text,
                popup_x, popup_y + popup_height * -0.3,
                arcade.color.BLACK,
                font_size=12,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )
        # invalid color
        if (self.selected_color and
                not self.valid_route_colors(self.selected_color, city1, city2)):
            error_text = f"Cannot use {self.selected_color.upper()} card on this route!"
            arcade.draw_text(
                error_text,
                popup_x - popup_width * 0.4,
                popup_y - popup_height * 0.4,
                arcade.color.RED,
                font_size=14,
                anchor_x="left",
                anchor_y="center",
                bold=True
            )


    def claim_route(self, city1, city2):
        """Claim the route after pop-up interaction"""
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)

        # Determine which pair exists
        if city_pair in self.train_map:
            pair = city_pair
        elif reverse_pair in self.train_map:
            pair = reverse_pair
        else:
            return

        # Find first available route and claim it
        for i, taken in enumerate(self.route_taken[pair]):
            if not taken:
                # Mark this route as taken
                self.route_taken[pair][i] = True

                # Make all sprites for this route visible
                for train_sprite in self.train_map[pair][i]:
                    train_sprite.set_texture(0)
                    train_sprite.alpha = 255
                break


    def is_point_in_button(self, x, y, button_bounds):
        """Check if a point is inside a button's bounds"""
        left, right, bottom, top = button_bounds
        return left <= x <= right and bottom <= y <= top

    def handle_color_selection(self, x, y):
        """Handle color button clicks"""
        if not hasattr(self, 'color_buttons'):
            return None

        for button in self.color_buttons:
            if self.is_point_in_button(x, y, button['bounds']):
                return button['color']
        return None

    # Color validation
    def valid_route_colors(self, selected_color, city1, city2):
        """Get available colors for the route"""
        for city_pair in [(city1, city2), (city2, city1)]:
            if city_pair in c.TRAINS:
                available_colors = {route_data["color"] for route_data in c.TRAINS[city_pair]}
                if selected_color == "locomotive":
                    return True
                return (selected_color in available_colors or
                        "colorless" in available_colors)
        return False


def main():
    """ Main function """
    if platform.system() == "Darwin":  # macOS
        window = arcade.Window(c.SCREEN_WIDTH, c.WINDOW_HEIGHT, c.WINDOW_TITLE, resizable=False)
        window.set_location(0, 0)
    else:
        window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.WINDOW_TITLE,
                               fullscreen=True, resizable=False)

    # Import StartMenuView here
    from start_menu import StartMenuView  # Or whatever file you put StartMenuView in

    # Show the start menu first instead of going directly to game
    start_menu = StartMenuView()
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()
