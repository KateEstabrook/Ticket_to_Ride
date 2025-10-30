"""
Ticket to Ride Board
"""

import platform
import random
import arcade
from arcade import SpriteList

import globals
import constants as c
import deck
import cards
import route
import player
import popups

class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self, player_obj):
        """Initializer"""

        # Call the parent class initializer
        super().__init__()

        self.player = player_obj  # keep the player
        self.drawn_card = None  # slot for the card you draw from the deck

        # Background image will be stored in this variable
        self.background = arcade.load_texture("images/board_borders.png")

        self.board_rect = None
        self._update_board_rect()  # compute once before placing sprites

        text_x1, text_y1 = self.img_to_screen(1150, -55, top_left=True)
        text_x2, text_y2 = self.img_to_screen(1150, 25, top_left=True)
        text_x3, text_y3 = self.img_to_screen(1700, -55, top_left=True)
        text_x4, text_y4 = self.img_to_screen(1700, 25, top_left=True)
        self.leaderboard_lines = [
            arcade.Text("BLUE - 312", text_x1, text_y1, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("GREEN - 343", text_x2, text_y2, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("RED - 232", text_x3, text_y3, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("YELLOW - 123", text_x4, text_y4, arcade.color.WHITE, 15, anchor_x="left"),
        ]

        orange_num_x, orange_num_y = self.img_to_screen(2670, 1075, top_left=True)
        black_num_x, black_num_y = self.img_to_screen(2950, 1075, top_left=True)
        blue_num_x, blue_num_y = self.img_to_screen(3230, 1075, top_left=True)
        green_num_x, green_num_y = self.img_to_screen(2670, 1255, top_left=True)
        pink_num_x, pink_num_y = self.img_to_screen(2950, 1255, top_left=True)
        red_num_x, red_num_y = self.img_to_screen(3230, 1255, top_left=True)
        white_num_x, white_num_y = self.img_to_screen(2670, 1435, top_left=True)
        yellow_num_x, yellow_num_y = self.img_to_screen(2950, 1435, top_left=True)
        wild_num_x, wild_num_y = self.img_to_screen(3230, 1435, top_left=True)

        self.index_cards = [
            arcade.Text("0", orange_num_x, orange_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", black_num_x, black_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", blue_num_x, blue_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", green_num_x, green_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", pink_num_x, pink_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", red_num_x, red_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", white_num_x, white_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", yellow_num_x, yellow_num_y, arcade.color.WHITE, 13, anchor_x="left"),
            arcade.Text("0", wild_num_x, wild_num_y, arcade.color.WHITE, 13, anchor_x="left"),
        ]

        # Train pieces
        # One list for all train sprites (create it ONCE)
        self.train_list = arcade.SpriteList()
        train_piece = arcade.load_texture(player_obj.get_sprite())

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

                train_piece = arcade.load_texture(player_obj.get_sprite())
                for position in positions:
                    if isinstance(position, tuple) and len(position) == 3:
                        ix, iy, angle = position
                        train_sprite = arcade.Sprite()
                        train_sprite.append_texture(train_piece)
                        train_sprite.set_texture(0)
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
                # for position in positions:
                #     if isinstance(position, tuple) and len(position) == 3:
                #         ix, iy, angle = position
                #         train_sprite = arcade.Sprite()
                #         train_sprite.append_texture(blue_train)
                #         train_sprite.append_texture(green_train)
                #         train_sprite.append_texture(red_train)
                #         train_sprite.append_texture(yellow_train)
                #         if self.player_color == 'BLUE':
                #             train_sprite.set_texture(0)
                #         elif self.player_color == 'GREEN':
                #             train_sprite.set_texture(1)
                #         elif self.player_color == 'RED':
                #             train_sprite.set_texture(2)
                #         elif self.player_color == 'YELLOW':
                #             train_sprite.set_texture(3)
                #         train_sprite.scale = c.TRAIN_SCALE
                #         train_sprite.angle = angle
                #         train_sprite.alpha = 0  # start fully transparent
                #         # Store route information with the sprite
                #         train_sprite.route_color = color
                #         train_sprite.route_name = train
                #         self.place_train_sprite(ix, iy, train_sprite, top_left=True)

                #         self.train_list.append(train_sprite)
                #         route_sprites.append(train_sprite)

                self.train_map[train].append(route_sprites)
        self.city_list = arcade.SpriteList()

        # Load textures
        base_tex = arcade.load_texture("images/city.png")
        hover_tex = arcade.load_texture("images/button_yellow.png")
        self.selected_color = None
        self.selected_dests = []

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
            scale=c.PLAYER_SCALING / 2,
        )

        self.card_textures = {
            name : arcade.load_texture(f"images/{filename}")
            for name, (_, _, filename) in c.PLAYER_CARDS.items()
        }

        self.card_list = arcade.SpriteList()

        #faceup_deck = faceup_deck
        i = 0
        for name, (sx, sy) in c.FACEUP_CARDS.items():
            card = arcade.Sprite()

            # Grab cards from the faceup deck
            card.texture = arcade.load_texture(globals.faceup_deck.
                                               get_card_at_index(i).get_sprite())

            self.place_card(card, sx, sy, top_left=True, scale = 0.37)

            self.card_list.append(card)
            i += 1

        for name, (sx, sy, filename) in c.PLAYER_CARDS.items():
            card = arcade.Sprite()
            card.texture = self.card_textures[name]

            self.place_card(card, sx, sy, top_left=True, scale=0.37)

            self.card_list.append(card)

        self.card_banner = arcade.Sprite("images/card_banner.png", scale=0.435)
        cx, cy = self.img_to_screen(2840, 910, top_left=True)
        self.card_banner.center_x = cx
        self.card_banner.center_y = cy

        self.leaderboard_banner = arcade.Sprite("images/leaderboard_banner.png", scale=0.40)
        lx, ly = self.img_to_screen(1250, -40, top_left=True)
        self.leaderboard_banner.center_x = lx
        self.leaderboard_banner.center_y = ly

        self.deck = arcade.Sprite("images/deck.png", scale=0.37)
        sx, sy = self.img_to_screen(-60, 280, top_left=True)
        self.deck.center_x = sx
        self.deck.center_y = sy

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        self.showing_deck_popup = False

        self.deck_sprite = arcade.SpriteList()
        self.deck_sprite.append(self.deck)

        self.showing_popup = False
        self.showing_dest_popup = False
        self.popup_city1 = None
        self.popup_city2 = None
        self.popup_route_length = 0
        self.color_buttons = []
        self.dest_buttons = []

        self.showing_faceup_popup = False
        self.selected_faceup_card_index = None
        self.take_button_bounds = None

    def reset(self):
        """Restart the game."""
        # Set up the player
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

    def _contain_rect(self, tex_w: float, tex_h: float, view_w: float, view_h: float):
        """
        Scale the texture to *contain* within the view while preserving aspect,
        and return an LBWH rect centered in the view.
        """
        scale = min(view_w / tex_w, view_h / tex_h)
        draw_w = tex_w * scale
        draw_h = tex_h * scale
        left = (view_w - draw_w) / 2
        bottom = (view_h - draw_h) / 2
        return arcade.LBWH(left, bottom, draw_w, draw_h)

    def _update_board_rect(self):
        """Recompute the board rect from the current window size."""
        # Fall back to constants if window isn’t ready yet
        width = getattr(self.window, "width", c.SCREEN_WIDTH)
        height = getattr(self.window, "height", c.SCREEN_HEIGHT)

        # contain the board inside the full window
        base = self._contain_rect(self.background.width, self.background.height, width, height)

        # uniformly shrink the rect and re-center it
        s = getattr(c, "BOARD_SCALE", 1.0)
        draw_w = base.width * s
        draw_h = base.height * s
        left = base.left + (base.width - draw_w) / 2
        bottom = base.bottom + (base.height - draw_h) / 2

        self.board_rect = arcade.LBWH(left, bottom, draw_w, draw_h)

    def img_to_screen(self, ix: float, iy: float, *, top_left: bool = False) -> tuple[float, float]:
        """
        Convert image pixel coords to screen coords using the current board rect.
        """
        if top_left:
            iy = self.background.height - iy

        # Use the dynamic board rect, not constants
        left = self.board_rect.left
        bottom = self.board_rect.bottom
        bw = self.board_rect.width
        bh = self.board_rect.height

        sx = bw / self.background.width
        sy = bh / self.background.height
        return ix * sx + left, iy * sy + bottom

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

    # In your GameView class, update the on_draw method:
    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_texture_rect(
            self.background,
            self.board_rect
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
            popups.route_popup(self, self.popup_city1, self.popup_city2)  # Pass self as first argument

        if self.showing_dest_popup:
            popups.show_dest_pop_up()
            0

        if self.showing_deck_popup:
            popups.deck_pop_up(self)  # Pass self as first argument

        if self.showing_faceup_popup:
            popups.faceup_card_pop_up(self, self.selected_faceup_card_index)  # Add this line

        self.deck_sprite.draw()

        tmp = arcade.SpriteList()
        tmp.append(self.card_banner)
        tmp.append(self.leaderboard_banner)
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
        if self.showing_deck_popup:
            # Handle exit click
            if hasattr(self, 'continue_button_bounds'):
                left, right, bottom, top = self.continue_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    # Add the drawn card to the player's hand before closing
                    if self.drawn_card is not None:
                        self.player.get_train_cards().add(self.drawn_card)
                        self.drawn_card = None
                    self.showing_deck_popup = False
                    self.selected_color = None
                    return

            # If click is elsewhere while popup is up, just consume it
            return

        # Add this section after the deck popup handling but before the route popup handling
        if self.showing_faceup_popup:
            # Handle take card button click
            if hasattr(self, 'take_button_bounds'):
                left, right, bottom, top = self.take_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    # Add the selected face-up card to player's hand
                    if self.selected_faceup_card_index is not None:
                        taken_card = globals.faceup_deck.remove(self.selected_faceup_card_index)
                        if taken_card:
                            self.player.get_train_cards().add(taken_card)
                            # Refresh the face-up cards display
                            self.refresh_faceup_cards()
                    self.showing_faceup_popup = False
                    self.selected_faceup_card_index = None
                    return

            # Handle exit button click
            if hasattr(self, 'exit_button_bounds'):
                left, right, bottom, top = self.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.showing_faceup_popup = False
                    self.selected_faceup_card_index = None
                    return

            # If click is elsewhere while popup is up, just consume it
            return

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

        if self.showing_dest_popup:
            # Check if save button was clicked
            if hasattr(self, 'save_button_bounds') and self.save_button_bounds:
                left, right, bottom, top = self.save_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    if (len(self.selected_dests) >= 2):

                        self.showing_dest_popup = False
                        # ADD DEST CARDS TO PLAYER DEST DECK
                        self.selected_dests = []
                    return
            # Check if dest card was clicked
            selected_dest = self.handle_dest_selection(x, y)
            if selected_dest in self.selected_dests:
                self.selected_dests.remove(selected_dest)
            else:
                self.selected_dests.append(selected_dest)
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            # Use the actual mouse coordinates for collision detection
            hit_deck = arcade.get_sprites_at_point((x, y), self.deck_sprite)
            hits = arcade.get_sprites_at_point((x, y), self.city_list)
            hit_faceup_cards = arcade.get_sprites_at_point((x, y), self.card_list)

            # If we clicked the deck, show the deck popup and stop processing
            if hit_deck:
                if globals.train_deck.get_len() > 0:
                    # draw the top card; choose -1 or 0, just be consistent
                    self.drawn_card = globals.train_deck.remove(-1)
                    self.showing_deck_popup = True
                    self.selected_color = None
                return

            # Add face-up card detection
            if hit_faceup_cards:
                # Find which face-up card was clicked (first 5 cards in card_list are face-up)
                clicked_sprite = hit_faceup_cards[0]
                if clicked_sprite in self.card_list:
                    card_index = self.card_list.index(clicked_sprite)
                    # Only the first 5 cards are face-up cards
                    if card_index < 5:
                        self.selected_faceup_card_index = card_index
                        self.showing_faceup_popup = True
                        print(f"Face-up card {card_index} clicked")  # Debug
                return

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

    def handle_dest_selection(self, x, y):
        """Handle dest button clicks"""
        if not hasattr(self, 'dest_buttons'):
            return None

        for button in self.dest_buttons:
            if self.is_point_in_button(x, y, button['bounds']):
                return button['cities']
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

    globals.initialize_game()
    # Import StartMenuView here
    from start_menu import StartMenuView  # Or whatever file you put StartMenuView in
    print(globals.faceup_deck)
    # Show the start menu first instead of going directly to game
    start_menu = StartMenuView()
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main()