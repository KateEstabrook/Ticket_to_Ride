"""
Ticket to Ride Board
"""

import platform
import arcade
import globals as game_globals
import constants as c
import cards
import player
import popups


class BoardRenderer:
    """Handles all rendering and display-related functionality for the game board."""

    def __init__(self, game_view):
        """Initialize the BoardRenderer with a reference to the main game view."""
        self.game_view = game_view

    def on_draw(self):
        """Render the entire game screen including background, sprites, and UI elements."""
        # This command has to happen before we start drawing
        self.game_view.clear()

        # Draw the background texture
        arcade.draw_texture_rect(
            self.game_view.background,
            self.game_view.board_rect
        )

        dest_list = arcade.SpriteList()
        # Destination cards set up
        i = 0
        if game_globals.player_obj.get_destination_cards().get_len() > 0:
            for number, (sx, sy) in c.DEST_CARDS.items():
                if i >= game_globals.player_obj.get_destination_cards().get_len():
                    break  # stop if there are no more cards to draw

                card = arcade.Sprite()

                card.texture = arcade.load_texture(game_globals.player_obj.
                                                   get_destination_cards().get_card_at_index(i).get_sprite())

                self.place_card(card, sx, sy, top_left=True, scale=0.38)
                dest_list.append(card)
                i += 1

        # Draw all the sprites
        self.game_view.train_list.draw()
        self.game_view.city_list.draw()
        self.game_view.card_list.draw()
        self.game_view.dest_deck_sprite.draw()
        dest_list.draw()

        # Draw sprites for beginning
        self.game_view.deck_sprite.draw()
        tmp = arcade.SpriteList()
        tmp.append(self.game_view.card_banner)
        tmp.append(self.game_view.leaderboard_banner)
        tmp.append(self.game_view.info_button)
        tmp.draw()

        # draw popups
        if self.game_view.showing_popup:
            popups.route_popup(self.game_view, self.game_view.popup_city1,
                               self.game_view.popup_city2)

        if len(game_globals.dest_draw) == 0:
            for _ in range(4):
                game_globals.dest_draw.append(game_globals.dest_deck.remove(-1))

        if self.game_view.showing_dest_popup:
            popups.show_dest_pop_up(self.game_view, game_globals.dest_draw, 2)

        if self.game_view.showing_deck_popup:
            popups.deck_pop_up(self.game_view)

        if self.game_view.showing_faceup_popup:
            popups.faceup_card_pop_up(self.game_view, self.game_view.selected_faceup_card_index)


        # Draw leaderboard lines and card counts
        for line in self.game_view.leaderboard_lines:
            line.draw()

        for line in self.game_view.index_cards:
            line.draw()

        if self.game_view.showing_info_popup:
            popups.show_info_pop_up(self.game_view)

        # draw cursor last
        cursor = arcade.SpriteList()
        cursor.append(self.game_view.player_sprite)
        cursor.draw()


    def _contain_rect(self, tex_w: float, tex_h: float, view_w: float, view_h: float):
        """
        Scale the texture to within the view
        """
        scale = min(view_w / tex_w, view_h / tex_h)
        draw_w = tex_w * scale
        draw_h = tex_h * scale
        left = (view_w - draw_w) / 2
        bottom = (view_h - draw_h) / 2
        return arcade.LBWH(left, bottom, draw_w, draw_h)

    def _update_board_rect(self):
        """Recompute the board rect from the current window size."""
        # Fall back to constants if window isn't ready yet
        width = getattr(self.game_view.window, "width", c.SCREEN_WIDTH)
        height = getattr(self.game_view.window, "height", c.SCREEN_HEIGHT)

        # contain the board inside the full window
        base = self._contain_rect(self.game_view.background.width,
                                  self.game_view.background.height, width, height)

        # uniformly shrink the rect and re-center it
        s = getattr(c, "BOARD_SCALE", 1.0)
        draw_w = base.width * s
        draw_h = base.height * s
        left = base.left + (base.width - draw_w) / 2
        bottom = base.bottom + (base.height - draw_h) / 2
        self.game_view.board_rect = arcade.LBWH(left, bottom, draw_w, draw_h)

    def img_to_screen(self, ix: float, iy: float, *, top_left: bool = False) -> tuple[float, float]:
        """
        Convert image pixel coords to screen coords using the current board rect.
        """
        if top_left:
            iy = self.game_view.background.height - iy

        # Use the dynamic board rect, not constants
        left = self.game_view.board_rect.left
        bottom = self.game_view.board_rect.bottom
        bw = self.game_view.board_rect.width
        bh = self.game_view.board_rect.height

        sx = bw / self.game_view.background.width
        sy = bh / self.game_view.background.height
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


class MouseHandler:
    """Handles all mouse input and interaction for the game."""

    def __init__(self, game_view):
        """Initialize the MouseHandler with a reference to the main game view."""
        self.game_view = game_view

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.game_view.player_sprite.center_x = x
        self.game_view.player_sprite.center_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press events including popup interactions and city selection."""
        if (hasattr(self.game_view, 'info_button_bounds') and
                self.game_view.info_button_bounds and
                button == arcade.MOUSE_BUTTON_LEFT):
            left, right, bottom, top = self.game_view.info_button_bounds
            if left <= x <= right and bottom <= y <= top:
                self.game_view.showing_info_popup = True
                return

            # Handle info popup exit
        if self.game_view.showing_info_popup:
            if hasattr(self.game_view, 'exit_button_bounds'):
                left, right, bottom, top = self.game_view.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.game_view.showing_info_popup = False
                    return
            # If click is elsewhere while info popup is up, just consume it
            return

        if self.game_view.showing_deck_popup:
            # Handle exit click
            if hasattr(self.game_view, 'continue_button_bounds'):
                left, right, bottom, top = self.game_view.continue_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    # Add the drawn card to the player's hand before closing
                    if self.game_view.drawn_card is not None:
                        game_globals.player_obj.get_train_cards().add(self.game_view.drawn_card)
                        self.game_view.drawn_card = None
                        self.game_view.update_card_counts()
                    self.game_view.showing_deck_popup = False
                    self.game_view.selected_color = None
                    return
            # If click is elsewhere while popup is up, just consume it
            return

        if self.game_view.showing_faceup_popup:
            # Handle take card button click
            if hasattr(self.game_view, 'take_button_bounds'):
                left, right, bottom, top = self.game_view.take_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    # Add the selected face-up card to player's hand
                    if self.game_view.selected_faceup_card_index is not None:
                        # Store which position we're replacing
                        replacement_index = self.game_view.selected_faceup_card_index
                        # Remove the card from face-up deck
                        taken_card = game_globals.faceup_deck.remove(replacement_index)
                        if taken_card:
                            # Add the card to player's hand
                            game_globals.player_obj.get_train_cards().add(taken_card)

                            # Replace the taken card with a card from the train deck
                            if game_globals.train_deck.get_len() > 0:
                                new_card = game_globals.train_deck.remove(-1)  # Draw from top
                                # Insert the new card at the same position we removed from
                                game_globals.faceup_deck.cards.insert(replacement_index, new_card)

                            # Refresh the face-up cards display
                            self.game_view.refresh_faceup_cards()
                            # Update the card count display
                            self.game_view.update_card_counts()
                    # Close pop up
                    self.game_view.showing_faceup_popup = False
                    self.game_view.selected_faceup_card_index = None
                    return

            # Handle exit button click
            if hasattr(self.game_view, 'exit_button_bounds'):
                left, right, bottom, top = self.game_view.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.game_view.showing_faceup_popup = False
                    self.game_view.selected_faceup_card_index = None
                    return
            # If click is elsewhere while popup is up, just consume it
            return

        if self.game_view.showing_popup:
            # Check if exit button was clicked
            if hasattr(self.game_view, 'exit_button_bounds'):
                left, right, bottom, top = self.game_view.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.game_view.showing_popup = False
                    self.game_view.deselect_all_cities()
                    self.game_view.selected_color = None
                    return

            # Check if save button was clicked
            if hasattr(self.game_view, 'save_button_bounds') and self.game_view.save_button_bounds:
                left, right, bottom, top = self.game_view.save_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    if (self.game_view.selected_color and
                            self.game_view.valid_route_colors(
                            self.game_view.selected_color, self.game_view.popup_city1,
                                self.game_view.popup_city2)):
                        self.game_view.showing_popup = False
                        self.game_view.claim_route(self.game_view.popup_city1,
                                                   self.game_view.popup_city2)
                        self.game_view.deselect_all_cities()
                        self.game_view.selected_color = None
                    return

            # Check if color button was clicked
            selected_color = self.game_view.handle_color_selection(x, y)
            if selected_color:
                self.game_view.selected_color = selected_color
                return
            # If neither button was pressed keep going
            return

        if self.game_view.showing_dest_popup:
            # Check if save button was clicked
            if hasattr(self.game_view, 'save_button_bounds') and self.game_view.save_button_bounds:
                left, right, bottom, top = self.game_view.save_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    min_required = getattr(self.game_view, 'min_dest_cards_to_keep', 2)
                    max_allowed = getattr(self.game_view, 'max_dest_cards_to_keep', 8)

                    # Check if player selected the right amount
                    if min_required <= len(self.game_view.selected_dests) <= max_allowed:
                        # Add selected cards to player's hand
                        for card in self.game_view.selected_dests:
                            game_globals.player_obj.get_destination_cards().add(card)

                        # Return unselected cards back to the deck
                        for card in game_globals.dest_draw:
                            if card not in self.game_view.selected_dests:
                                game_globals.dest_deck.cards.append(card)

                        # Clear dest_draw so next time we draw 4 new cards
                        game_globals.dest_draw.clear()
                        self.game_view.showing_dest_popup = False
                        self.game_view.selected_dests = []
                    return

            # Check if dest card was clicked
            selected_dest = self.game_view.handle_dest_selection(x, y)
            if selected_dest in self.game_view.selected_dests:
                self.game_view.selected_dests.remove(selected_dest)
            elif selected_dest is None:
                return
            else:
                # Check if player can still select more cards
                max_allowed = getattr(self.game_view, 'max_dest_cards_to_keep', 8)
                if len(self.game_view.selected_dests) < max_allowed:
                    self.game_view.selected_dests.append(selected_dest)
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            # Use the actual mouse coordinates for collision detection
            hit_deck = arcade.get_sprites_at_point((x, y), self.game_view.deck_sprite)
            hit_dest_deck = arcade.get_sprites_at_point((x, y), self.game_view.dest_deck_sprite)
            hits = arcade.get_sprites_at_point((x, y), self.game_view.city_list)
            hit_faceup_cards = arcade.get_sprites_at_point((x, y), self.game_view.card_list)

            # Show the deck popup
            if hit_deck:
                if game_globals.train_deck.get_len() > 0:
                    # draw the top card
                    self.game_view.drawn_card = game_globals.train_deck.remove(-1)
                    self.game_view.showing_deck_popup = True
                    self.game_view.selected_color = None
                return

            # Show the destination deck popup
            if hit_dest_deck:
                # Check how many destination cards the player currently has
                current_dest_cards = game_globals.player_obj.get_destination_cards().get_len()

                # Maximum of 8 destination cards allowed
                max_dest_cards = 8

                # If player already has 8 or more, don't allow drawing more
                if current_dest_cards >= max_dest_cards or current_dest_cards >= (max_dest_cards - 1):
                    return

                # Calculate how many cards the player can keep (but still draw 4 to show)
                remaining_slots = max_dest_cards - current_dest_cards

                # If dest_draw is empty, draw 4 new cards
                if len(game_globals.dest_draw) == 0:
                    for i in range(4):
                        if game_globals.dest_deck.get_len() > 0:
                            game_globals.dest_draw.append(game_globals.dest_deck.remove(-1))

                # Store how many cards can be kept (e.g., if player has 6, they can only keep 2 more)
                self.game_view.max_dest_cards_to_keep = remaining_slots
                # Minimum to keep is 2, or all remaining slots if less than 2
                self.game_view.min_dest_cards_to_keep = min(2, remaining_slots)

                self.game_view.showing_dest_popup = True
                return

            # Add face-up card detection
            if hit_faceup_cards:
                # Find which face-up card was clicked
                clicked_sprite = hit_faceup_cards[0]
                if clicked_sprite in self.game_view.card_list:
                    card_index = self.game_view.card_list.index(clicked_sprite)
                    # Only the first 5 cards are face-up cards
                    if card_index < 5:
                        self.game_view.selected_faceup_card_index = card_index
                        self.game_view.showing_faceup_popup = True
                return

            if not hits:
                return

            city = hits[0]
            # If this city is already selected then deselect it
            if city in self.game_view.selected_cities:
                city.set_texture(0)
                city.scale = c.CITY_SCALE
                self.game_view.selected_cities.remove(city)
                return

            if len(self.game_view.selected_cities) == 0:
                # If no city is already selected, select it
                city.set_texture(1)
                city.scale = c.CITY_SCALE_YELLOW
                self.game_view.selected_cities.append(city)
                return

            # If 2 cities are selected
            if len(self.game_view.selected_cities) == 2:
                newest = self.game_view.selected_cities.pop(1)
                newest.set_texture(0)
                newest.scale = c.CITY_SCALE
                oldest = self.game_view.selected_cities.pop(0)
                oldest.set_texture(0)
                oldest.scale = c.CITY_SCALE

            first_city_name = self.game_view.sprite_to_name(self.game_view.selected_cities[0])
            second_city_name = self.game_view.sprite_to_name(city)

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
                    self.game_view.deselect_all_cities()
                    return

                # Check if any routes are available
                available_count = sum(1 for taken in self.game_view.route_taken[pair] if not taken)

                if available_count > 0:
                    # Mark this one as selected
                    city.set_texture(1)
                    city.scale = c.CITY_SCALE_YELLOW
                    self.game_view.selected_cities.append(city)

                    # Show pop-up with route information
                    self.game_view.showing_popup = True
                    self.game_view.popup_city1 = first_city_name
                    self.game_view.popup_city2 = second_city_name
                    self.game_view.popup_route_length = c.ROUTES[first_city_name][second_city_name]
                    self.game_view.selected_color = None
                    return

            # If we get here, either cities aren't connected or all routes are claimed
            self.game_view.deselect_all_cities()

    def is_point_in_button(self, x, y, button_bounds):
        """Check if a point is inside a button's bounds"""
        left, right, bottom, top = button_bounds
        return left <= x <= right and bottom <= y <= top

    def handle_color_selection(self, x, y):
        """Handle color button clicks"""
        if not hasattr(self.game_view, 'color_buttons'):
            return None

        for button in self.game_view.color_buttons:
            if self.is_point_in_button(x, y, button['bounds']):
                return button['color']
        return None

    def handle_dest_selection(self, x, y):
        """Handle dest button clicks"""
        if not hasattr(self.game_view, 'dest_buttons'):
            return None

        for button in self.game_view.dest_buttons:
            if self.is_point_in_button(x, y, button['bounds']):
                return button['card']
        return None


class RouteController:
    """Manages route functionality including claiming routes and city connections."""

    def __init__(self, game_view):
        """Initialize the RouteController with a reference to the main game view."""
        self.game_view = game_view

    def deselect_all_cities(self):
        """Deselect all currently selected cities"""
        for city in self.game_view.selected_cities:
            city.set_texture(0)
            city.scale = c.CITY_SCALE
        self.game_view.selected_cities.clear()

    def claim_route(self, city1, city2):
        """Claim the route after pop-up interaction"""
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)

        # Determine which pair exists
        if city_pair in self.game_view.train_map:
            pair = city_pair
        elif reverse_pair in self.game_view.train_map:
            pair = reverse_pair
        else:
            return

        # Find first available route and claim it
        for i, taken in enumerate(self.game_view.route_taken[pair]):
            if not taken:
                # Mark this route as taken
                self.game_view.route_taken[pair][i] = True

                # Make all sprites for this route visible
                for train_sprite in self.game_view.train_map[pair][i]:
                    train_sprite.set_texture(0)
                    train_sprite.alpha = 255
                break

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

    def sprite_to_name(self, spr: arcade.Sprite) -> str:
        """
        Helper to get the name of the city sprite in self.selected_cities
        """
        idx = self.game_view.city_list.index(spr)
        return list(c.CITIES.keys())[idx]


class CardController:
    """Manages card-related functionality including face-up cards and card counting."""

    def __init__(self, game_view):
        """Initialize the CardController with a reference to the main game view."""
        self.game_view = game_view

    def refresh_faceup_cards(self):
        """Refresh the face-up card sprites after changes"""
        # Update the first 5 cards
        for i in range(5):
            if i < len(self.game_view.card_list):
                card_sprite = self.game_view.card_list[i]
                # Make sure we don't go out of bounds of the face-up deck
                if i < game_globals.faceup_deck.get_len():
                    faceup_card = game_globals.faceup_deck.get_card_at_index(i)
                    sprite_path = faceup_card.get_sprite()

                    # Cache the texture to avoid repeated loading
                    if not hasattr(self.game_view, ''
                                                   'faceup_textures'):
                        self.game_view.faceup_textures = {}

                    if sprite_path not in self.game_view.faceup_textures:
                        self.game_view.faceup_textures[sprite_path] = (
                            arcade.load_texture(sprite_path))

                    card_sprite.texture = self.game_view.faceup_textures[sprite_path]
                    card_sprite.alpha = 255  # Make sure it's visible
                else:
                    # If there are fewer than 5 cards, hide the extra sprites
                    card_sprite.alpha = 0

    def update_card_counts(self):
        """Update the displayed card counts for each color"""
        # Count cards in player's hand by color
        color_counts = {
            "orange": 0, "black": 0, "blue": 0, "green": 0,
            "pink": 0, "red": 0, "white": 0, "yellow": 0, "wild": 0
        }

        # Get the player's train cards deck
        player_train_cards = game_globals.player_obj.get_train_cards()

        # Count cards by color
        for i in range(player_train_cards.get_len()):
            card = player_train_cards.get_card_at_index(i)
            color = card.get_color().lower()
            if color in color_counts:
                color_counts[color] += 1

        # Update the display text
        colors = ["orange", "black", "blue", "green", "pink", "red", "white", "yellow", "wild"]
        for i, color in enumerate(colors):
            if i < len(self.game_view.index_cards):
                self.game_view.index_cards[i].text = str(color_counts[color])


class KeyboardHandler:
    """Handles keyboard input for the game."""

    def __init__(self, game_view):
        """Initialize the KeyboardHandler with a reference to the main game view."""
        self.game_view = game_view

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle keyboard input including game controls and navigation."""
        if symbol == arcade.key.SPACE:
            self.game_view.reset()
        elif symbol == arcade.key.ESCAPE:
            self.game_view.window.close()


class GameInitializer:
    """Handles game initialization and reset functionality."""

    def __init__(self, game_view):
        """Initialize the GameInitializer with a reference to the main game view."""
        self.game_view = game_view

    def reset(self):
        """Restart the game."""
        # Set up the player
        self.game_view.player_sprite.center_x = 50
        self.game_view.player_sprite.center_y = 50


class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        """Initializer"""

        # Call the parent class initializer
        super().__init__()

        self.drawn_card = None  # slot for the card you draw from the deck

        # Background image will be stored in this variable
        self.background = arcade.load_texture("images/board_borders.png")

        self.board_rect = None

        # Create helper classes
        self.board_renderer = BoardRenderer(self)
        self.board_renderer._update_board_rect()  # compute once before placing sprites

        # Convert image coordinates to screen coordinates for the leaderboard
        text_x1, text_y1 = self.board_renderer.img_to_screen(1150, -55, top_left=True)
        text_x2, text_y2 = self.board_renderer.img_to_screen(1150, 25, top_left=True)
        text_x3, text_y3 = self.board_renderer.img_to_screen(1700, -55, top_left=True)
        text_x4, text_y4 = self.board_renderer.img_to_screen(1700, 25, top_left=True)
        self.leaderboard_lines = [
            arcade.Text("BLUE - 312", text_x1, text_y1, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("GREEN - 343", text_x2, text_y2, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("RED - 232", text_x3, text_y3, arcade.color.WHITE, 15, anchor_x="left"),
            arcade.Text("YELLOW - 123", text_x4, text_y4, arcade.color.WHITE, 15, anchor_x="left"),
        ]

        # Train card on screen placements
        orange_num_x, orange_num_y = self.board_renderer.img_to_screen(2670, 1075, top_left=True)
        black_num_x, black_num_y = self.board_renderer.img_to_screen(2950, 1075, top_left=True)
        blue_num_x, blue_num_y = self.board_renderer.img_to_screen(3230, 1075, top_left=True)
        green_num_x, green_num_y = self.board_renderer.img_to_screen(2670, 1255, top_left=True)
        pink_num_x, pink_num_y = self.board_renderer.img_to_screen(2950, 1255, top_left=True)
        red_num_x, red_num_y = self.board_renderer.img_to_screen(3230, 1255, top_left=True)
        white_num_x, white_num_y = self.board_renderer.img_to_screen(2670, 1435, top_left=True)
        yellow_num_x, yellow_num_y = self.board_renderer.img_to_screen(2950, 1435, top_left=True)
        wild_num_x, wild_num_y = self.board_renderer.img_to_screen(3230, 1435, top_left=True)

        # Count for the train cards
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

        self.popup_textures = {
            'white_bg': arcade.make_soft_square_texture(2, (251, 238, 204), outer_alpha=255),
            'save_button': arcade.make_soft_square_texture(2, c.SAVE_BUTTON, outer_alpha=255),
            'exit_button': arcade.make_soft_square_texture(2, c.EXIT_BUTTON, outer_alpha=255),
            'shadow': arcade.make_soft_square_texture(2, (0, 0, 0), outer_alpha=100)
        }

        self.color_textures = {}
        color_cards = [
            ("RED", "red.png"), ("BLUE", "blue.png"), ("GREEN", "green.png"),
            ("YELLOW", "yellow.png"), ("ORANGE", "orange.png"), ("PINK", "pink.png"),
            ("BLACK", "black.png"), ("WHITE", "white.png"), ("LOCOMOTIVE", "wild.png")
        ]

        for color_name, filename in color_cards:
            self.color_textures[color_name] = arcade.load_texture(f"images/{filename}")

        self.destination_textures = {}
        self.faceup_textures = {}

        # Train pieces
        # One list for all train sprites (create it ONCE)
        self.train_list = arcade.SpriteList()
        train_piece = arcade.load_texture(game_globals.player_obj.get_sprite())

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

            # Create sprites for each route between cities
            for route_data in routes:
                route_sprites = []
                positions = route_data["positions"]
                color = route_data["color"]

                train_piece = arcade.load_texture(game_globals.player_obj.get_sprite())
                # Create individual train sprites for each position in the route
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
                        self.board_renderer.place_train_sprite(ix, iy, train_sprite, top_left=True)

                        self.train_list.append(train_sprite)
                        route_sprites.append(train_sprite)

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
            self.board_renderer.place_city(
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

        # Face up card set up
        i = 0
        for name, (sx, sy) in c.FACEUP_CARDS.items():
            card = arcade.Sprite()
            card.texture = arcade.load_texture(game_globals.faceup_deck.
                                               get_card_at_index(i).get_sprite())

            self.board_renderer.place_card(card, sx, sy, top_left=True, scale = 0.37)
            self.card_list.append(card)
            i += 1

        # Player's hand card set up
        for name, (sx, sy, filename) in c.PLAYER_CARDS.items():
            card = arcade.Sprite()
            card.texture = self.card_textures[name]
            self.board_renderer.place_card(card, sx, sy, top_left=True, scale=0.37)
            self.card_list.append(card)

        # Banners
        self.card_banner = arcade.Sprite("images/card_banner.png", scale=0.435)
        cx, cy = self.board_renderer.img_to_screen(2840, 910, top_left=True)
        self.card_banner.center_x = cx
        self.card_banner.center_y = cy

        self.leaderboard_banner = arcade.Sprite("images/leaderboard_banner.png", scale=0.40)
        lx, ly = self.board_renderer.img_to_screen(1250, -40, top_left=True)
        self.leaderboard_banner.center_x = lx
        self.leaderboard_banner.center_y = ly

        # Deck sprite set up
        self.deck = arcade.Sprite("images/deck.png", scale=0.37)
        sx, sy = self.board_renderer.img_to_screen(-60, 280, top_left=True)
        self.deck.center_x = sx
        self.deck.center_y = sy

        # Destination deck sprite set up
        self.dest_deck = arcade.Sprite("images/dest_deck.png", scale=0.37)
        sx, sy = self.board_renderer.img_to_screen(2560, 280, top_left=True)
        self.dest_deck.center_x = sx
        self.dest_deck.center_y = sy

        # Pop up and UI states
        self.window.set_mouse_visible(False) # Don't show the mouse cursor
        self.showing_deck_popup = False
        self.deck_sprite = arcade.SpriteList()
        self.deck_sprite.append(self.deck)
        self.dest_deck_sprite = arcade.SpriteList()
        self.dest_deck_sprite.append(self.dest_deck)
        self.showing_popup = False
        self.showing_dest_popup = True
        self.popup_city1 = None
        self.popup_city2 = None
        self.popup_route_length = 0
        self.color_buttons = []
        self.dest_buttons = []
        self.min_dest_cards_to_keep = 2
        self.max_dest_cards_to_keep = 8
        self.showing_faceup_popup = False # Don't show face up popup
        self.selected_faceup_card_index = None # Face up card that was clicked
        self.take_button_bounds = None # Bounds for "take card"

        # Initialize helper classes
        self.mouse_handler = MouseHandler(self)
        self.route_controller = RouteController(self)
        self.card_controller = CardController(self)
        self.keyboard_handler = KeyboardHandler(self)
        self.game_initializer = GameInitializer(self)

        self.card_controller.update_card_counts() # Initialize card count display

        # Info button
        self.info_button = arcade.Sprite("images/info_button.jpg", scale=0.1)
        self.info_button.center_x = 50  # Top left position
        self.info_button.center_y = c.WINDOW_HEIGHT - 50
        self.info_button_bounds = None
        self.showing_info_popup = False

        # Calculate info button bounds
        info_button_width = self.info_button.width
        info_button_height = self.info_button.height
        self.info_button_bounds = (
            self.info_button.center_x - info_button_width / 2,
            self.info_button.center_x + info_button_width / 2,
            self.info_button.center_y - info_button_height / 2,
            self.info_button.center_y + info_button_height / 2
        )

    def reset(self):
        """Restart the game"""
        self.game_initializer.reset()

    def on_draw(self):
        """Render the screen"""
        self.board_renderer.on_draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse motion"""
        self.mouse_handler.on_mouse_motion(x, y, dx, dy)

    def on_update(self, delta_time):
        """Update game state (currently empty)."""

    def sprite_to_name(self, spr: arcade.Sprite) -> str:
        """Get city name from sprite"""
        return self.route_controller.sprite_to_name(spr)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press"""
        self.mouse_handler.on_mouse_press(x, y, button, modifiers)

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle key press"""
        self.keyboard_handler.on_key_press(symbol, modifiers)

    def deselect_all_cities(self):
        """Deselect all cities"""
        self.route_controller.deselect_all_cities()

    def claim_route(self, city1, city2):
        """Claim route"""
        self.route_controller.claim_route(city1, city2)

    def is_point_in_button(self, x, y, button_bounds):
        """Check if point is in button"""
        return self.mouse_handler.is_point_in_button(x, y, button_bounds)

    def handle_color_selection(self, x, y):
        """Handle color selection"""
        return self.mouse_handler.handle_color_selection(x, y)

    def handle_dest_selection(self, x, y):
        """Handle destination selection"""
        return self.mouse_handler.handle_dest_selection(x, y)

    def valid_route_colors(self, selected_color, city1, city2):
        """Validate route colors"""
        return self.route_controller.valid_route_colors(selected_color, city1, city2)

    def refresh_faceup_cards(self):
        """Refresh face-up cards"""
        self.card_controller.refresh_faceup_cards()

    def update_card_counts(self):
        """Update card counts"""
        self.card_controller.update_card_counts()


def main(self):
    """Main function to initialize and run the game."""
    if platform.system() == "Darwin":  # macOS
        window = arcade.Window(c.SCREEN_WIDTH, c.WINDOW_HEIGHT, c.WINDOW_TITLE, resizable=False)
        window.set_location(0, 0)
    else:
        window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.WINDOW_TITLE,
                               fullscreen=True, resizable=False)

    game_globals.initialize_game()

    from start_menu import StartMenuView
    print(game_globals.faceup_deck)
    # Show the start menu
    start_menu = StartMenuView()
    window.show_view(start_menu)
    arcade.run()


if __name__ == "__main__":
    main(GameView)
