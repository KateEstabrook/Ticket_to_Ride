"""
Ticket to Ride Board
"""

import platform
import arcade
import globals as game_globals
import constants as c
import popups

from win_screen import WinScreenView


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

        check_list = arcade.SpriteList()
        dest_list = arcade.SpriteList()

        # keep these available to mouse handler
        self.game_view.dest_card_sprites = dest_list
        self.game_view.dest_card_objects = []

        # Destination cards set up
        i = 0
        if game_globals.player_obj.get_destination_cards().get_len() > 0:
            for number, (sx, sy) in c.DEST_CARDS.items():
                if i >= game_globals.player_obj.get_destination_cards().get_len():
                    break  # stop if there are no more cards to draw

                card = arcade.Sprite()
                dest_card = game_globals.player_obj.get_destination_cards().get_card_at_index(i)
                card.texture = arcade.load_texture(dest_card.get_sprite())

                player_map = game_globals.player_obj.get_map()
                if player_map.check_completed(dest_card):
                    check_sprite = arcade.Sprite()
                    check_tex = arcade.load_texture("images/green_check.png")
                    check_sprite.append_texture(check_tex)
                    check_sprite.set_texture(0)
                    self.place_card(check_sprite, sx, sy, top_left=True, scale=0.045)
                    check_list.append(check_sprite)

                self.game_view.dest_card_objects.append(dest_card)
                self.place_card(card, sx, sy, top_left=True, scale=c.DEST_SCALE)
                dest_list.append(card)
                i += 1

        # Draw all the sprites
        self.game_view.train_list.draw()
        self.game_view.city_list.draw()
        self.game_view.card_list.draw()
        self.game_view.dest_deck_sprite.draw()
        dest_list.draw()
        check_list.draw()

        self.game_view.write_log()
        for line in self.game_view.log_lines:
            line.draw()

        # Draw sprites for beginning
        self.game_view.deck_sprite.draw()
        tmp = arcade.SpriteList()
        tmp.append(self.game_view.dest_cards_banner)
        tmp.append(self.game_view.train_cards_banner)
        tmp.append(self.game_view.leaderboard_banner)
        tmp.append(self.game_view.info_button)
        tmp.draw()

        # draw popups
        if self.game_view.showing_popup:
            if game_globals.card_drawn == 0:
                popups.route_popup(self.game_view, self.game_view.popup_city1,
                               self.game_view.popup_city2)
            else:
                print("NOT ALLOWED")
                self.game_view.showing_allowed_popup = True
                self.game_view.showing_popup = False

        if len(game_globals.dest_draw) == 0:
            for _ in range(4):
                game_globals.dest_draw.append(game_globals.dest_deck.remove(-1))

        if self.game_view.showing_allowed_popup:
            popups.not_allowed_popup(self.game_view)

        if self.game_view.showing_dest_popup:
            #popups.show_dest_popup(self.game_view, game_globals.dest_draw, game_globals.num_choose)
            if game_globals.card_drawn == 0:
                popups.show_dest_popup(self.game_view, game_globals.dest_draw,
                                   self.game_view.min_dest_cards_to_keep)
            else:
                print("NOT ALLOWED")
                self.game_view.showing_allowed_popup = True
                self.game_view.showing_dest_popup = False

        if self.game_view.showing_deck_popup:
            if game_globals.card_drawn == 0:
                popups.deck_pop_up(self.game_view)
                game_globals.card_drawn += 1
            else:
                popups.deck_pop_up(self.game_view)
                game_globals.card_drawn == 0

        if (self.game_view.showing_dest_card_popup and
                getattr(self.game_view, "active_dest_card", None) is not None):
            popups.show_dest_card_pop_up(self.game_view, self.game_view.active_dest_card)

        if self.game_view.showing_faceup_popup:
            if game_globals.card_drawn == 0:
                popups.faceup_card_popup(self.game_view, self.game_view.selected_faceup_card_index)
                game_globals.card_drawn += 1
            else:
                popups.faceup_card_popup(self.game_view, self.game_view.selected_faceup_card_index)
                game_globals.card_drawn == 0

        self.draw_leaderboard()

        for line in self.game_view.index_cards:
            if line.text != "0":
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

    def draw_leaderboard(self):
        """Draws leaderboard"""
        player_train_count = game_globals.player_obj.get_trains()
        player_points = game_globals.player_obj.get_points()


        # Starting positions for two columns
        start_x1, start_y = self.img_to_screen(850, -35, top_left=True)
        start_x2, _ = self.img_to_screen(1650, -35, top_left=True)
        line_height = 25  # Space between lines

        # Clear existing leaderboard lines
        self.game_view.leaderboard_lines.clear()

        players = [
            {"name": "You", "score": player_points, "trains": player_train_count,
             "color": arcade.color.WHITE}
        ]
        for comp in game_globals.computers:
            comp_player = comp.get_player()
            players.append({
                "name": comp.get_color().upper(),
                "score": comp_player.get_points(),
                "trains": comp_player.get_trains(),
                "color": arcade.color.WHITE
            })

        # Draw each player's info in 2 columns
        for i, player_data in enumerate(players):
            y_pos = start_y - ((i // 2) * line_height)

            # Alternate between left and right columns
            if i % 2 == 0:  # Even indices: left column
                x_pos = start_x1
            else:  # Odd indices: right column
                x_pos = start_x2

            player_text = (f"{player_data['name']} - {player_data['score']} pts - "
                           f"{player_data['trains']} trains")

            text_obj = arcade.Text(
                player_text,
                x_pos,
                y_pos,
                player_data["color"],
                15,
                anchor_x="left"
            )
            self.game_view.leaderboard_lines.append(text_obj)

        # Draw leaderboard lines and card counts
        for line in self.game_view.leaderboard_lines:
            line.draw()

    def ui_scale(self, px: float) -> float:
        """Scale a pixel value from board-image space to current board size."""
        # Choose height (or width) as your canonical axis; height is fine:
        return px * (self.game_view.board_rect.height / self.game_view.background.height)

    def place_ui_anchor(self, sprite: arcade.Sprite, *, anchor: str,
                        margin_x: float, margin_y: float,
                        base_scale: float):
        """
        Position + scale a UI sprite relative to board_rect corners/edges.
        anchor in {"topleft","topright","bottomleft","bottomright",
        "topcenter","rightcenter","leftcenter","bottomcenter"}
        margin_* are in BOARD-IMAGE pixels (will be scaled with ui_scale()).
        """
        br = self.game_view.board_rect
        mx = self.ui_scale(margin_x)
        my = self.ui_scale(margin_y)

        # Scale sprite proportionally to board
        sprite.scale = base_scale * (br.height / self.game_view.background.height)

        anchors = {
            "topleft": (br.left + mx, br.top - my),
            "topright": (br.right - mx, br.top - my),
            "bottomleft": (br.left + mx, br.bottom + my),
            "bottomright": (br.right - mx, br.bottom + my),
            "topcenter": ((br.left + br.right) / 2, br.top - my),
            "bottomcenter": ((br.left + br.right) / 2, br.bottom + my),
            "leftcenter": (br.left + mx, (br.bottom + br.top) / 2),
            "rightcenter": (br.right - mx, (br.bottom + br.top) / 2),
        }
        cx, cy = anchors[anchor]
        sprite.center_x = cx
        sprite.center_y = cy


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
                self.game_view.add_log("You opened the info popup")
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
                    return 1
            # If click is elsewhere while popup is up, just consume it
            return

        if self.game_view.showing_dest_card_popup:
            if hasattr(self.game_view, 'exit_button_bounds'):
                left, right, bottom, top = self.game_view.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.game_view.showing_dest_card_popup = False
                    self.game_view.active_dest_card = None
                    return
            return  # consume clicks while popup open

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
                    if taken_card.get_color() == "wild" and game_globals.turn_val != 1:
                        return 2
                    return 1

            # Handle exit button click
            if hasattr(self.game_view, 'exit_button_bounds'):
                left, right, bottom, top = self.game_view.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.game_view.showing_faceup_popup = False
                    self.game_view.selected_faceup_card_index = None
                    return
            # If click is elsewhere while popup is up, just consume it
            return

        if self.game_view.showing_allowed_popup:
            # Check if exit button was clicked
            if hasattr(self.game_view, 'exit_button_bounds'):
                left, right, bottom, top = self.game_view.exit_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    self.game_view.showing_allowed_popup = False
                    self.game_view.deselect_all_cities()
                    game_globals.card_drawn = 1
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

            # Check if color button was clicked
            if hasattr(self.game_view, 'color_buttons'):
                selected_color_info = self.handle_color_selection(x, y)
                if selected_color_info:
                    self.game_view.selected_color = selected_color_info['color']
                    # Store route index
                    if 'route_index' in selected_color_info:
                        self.game_view.selected_route_index = selected_color_info['route_index']
                    return

            # Check if save button was clicked
            if hasattr(self.game_view, 'save_button_bounds') and self.game_view.save_button_bounds:
                left, right, bottom, top = self.game_view.save_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    if game_globals.player_obj.get_trains() < self.game_view.popup_route_length:
                        # Show error or just return without claiming
                        self.game_view.add_log(
                            f"Not enough trains for {self.game_view.popup_route_length}-length route!")
                        return
                    if (self.game_view.selected_color == "wild"
                            and not hasattr(self.game_view, 'showing_route_selection')):
                        # Only show second popup for double routes, not single routes
                        city_pair = (self.game_view.popup_city1, self.game_view.popup_city2)
                        reverse_pair = (self.game_view.popup_city2, self.game_view.popup_city1)

                        if city_pair in c.TRAINS:
                            routes_data = c.TRAINS[city_pair]
                            pair = city_pair
                        elif reverse_pair in c.TRAINS:
                            routes_data = c.TRAINS[reverse_pair]
                            pair = reverse_pair

                        # Count available routes
                        available_routes = []
                        for i, route_data in enumerate(routes_data):
                            route_taken = self.game_view.route_taken[pair][i]
                            if not route_taken and route_data["color"] != "colorless":
                                available_routes.append((i, route_data))

                        # Only show route selection if there are multiple colored available routes
                        # For colorless routes, just claim directly without second popup
                        if len(available_routes) > 1:
                            self.game_view.showing_route_selection = True
                            self.game_view.update_card_counts()
                            return
                        else:
                            # For single available route
                            self.game_view.showing_popup = False
                            self.game_view.claim_route(self.game_view.popup_city1,
                                                       self.game_view.popup_city2)
                            self.game_view.deselect_all_cities()
                            self.game_view.selected_color = None
                            self.game_view.update_card_counts()
                            return
                    else:
                        self.game_view.showing_popup = False
                        self.game_view.claim_route(self.game_view.popup_city1,
                                                   self.game_view.popup_city2)
                        self.game_view.deselect_all_cities()
                        self.game_view.selected_color = None
                        # Clean up route selection state
                        if hasattr(self.game_view, 'showing_route_selection'):
                            del self.game_view.showing_route_selection
                        if hasattr(self.game_view, 'selected_route_index'):
                            del self.game_view.selected_route_index
                    self.game_view.update_card_counts()
                    return

        if self.game_view.showing_dest_popup:
            # Check if save button was clicked
            if hasattr(self.game_view, 'save_button_bounds') and self.game_view.save_button_bounds:
                left, right, bottom, top = self.game_view.save_button_bounds
                if left <= x <= right and bottom <= y <= top:
                    min_required = getattr(self.game_view,
                                           'min_dest_cards_to_keep', game_globals.num_choose)
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

                        # Shuffle the destination deck so cards are randomized
                        game_globals.dest_deck.shuffle()

                        # Clear dest_draw so next time we draw 4 new cards
                        game_globals.dest_draw.clear()
                        self.game_view.showing_dest_popup = False
                        self.game_view.selected_dests = []

                        # From now on, only 1 dest required next times
                        if self.game_view.dest_first_time:
                            self.game_view.dest_first_time = False
                            return
                        return 2
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
            hit_dest_card_sprites = arcade.get_sprites_at_point((x, y),
                                                                self.game_view.dest_card_sprites)
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

            # after deck check:
            if hit_dest_card_sprites:
                # clicked_sprite is the first sprite under the mouse
                clicked_sprite = hit_dest_card_sprites[0]
                idx = self.game_view.dest_card_sprites.index(clicked_sprite)
                dest_card_obj = self.game_view.dest_card_objects[idx]

                self.game_view.active_dest_card = dest_card_obj
                self.game_view.showing_dest_card_popup = True
                return

            # Show the destination deck popup
            if hit_dest_deck:
                game_globals.num_choose = 1
                # Check how many destination cards the player currently has
                current_dest_cards = game_globals.player_obj.get_destination_cards().get_len()
                # Maximum of 8 destination cards allowed
                max_dest_cards = 8
                # If player already has 8 or more, don't allow drawing more
                if current_dest_cards >= max_dest_cards or current_dest_cards >= (max_dest_cards):
                    return
                # Calculate how many cards the player can keep (but still draw 4 to show)
                remaining_slots = max_dest_cards - current_dest_cards
                # If dest_draw is empty, draw 4 new cards
                if len(game_globals.dest_draw) == 0:
                    for i in range(4):
                        if game_globals.dest_deck.get_len() > 0:
                            game_globals.dest_draw.append(
                                game_globals.dest_deck.remove(-1))

                # Store how many cards can be kept
                # (e.g., if player has 6, they can only keep 2 more)
                self.game_view.max_dest_cards_to_keep = remaining_slots

                # First time require 2, later only 1; clamp by remaining slots
                min_required = 2 if self.game_view.dest_first_time else 1
                self.game_view.min_dest_cards_to_keep = min(min_required, remaining_slots)

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
                return button
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

        if city_pair in c.TRAINS:
            routes_data = c.TRAINS[city_pair]
            pair = city_pair
            len_route = len(c.TRAINS[city_pair][0]["positions"])
        elif reverse_pair in c.TRAINS:
            routes_data = c.TRAINS[reverse_pair]
            pair = reverse_pair
            len_route = len(c.TRAINS[reverse_pair][0]["positions"])
        selected_color = self.game_view.selected_color

        # Check if we have a specific route index selected
        selected_route_index = getattr(self.game_view, 'selected_route_index', None)

        # Get the human player's color
        player_tex = arcade.load_texture(
            game_globals.player_obj.get_sprite()
        )

        if selected_route_index is not None:
            # Claim the specifically selected route
            if not self.game_view.route_taken[pair][selected_route_index]:
                self.game_view.route_taken[pair][selected_route_index] = True
                for train_sprite in self.game_view.train_map[pair][selected_route_index]:
                    train_sprite.texture = player_tex
                    train_sprite.alpha = 255
                    train_sprite.claimed_by = game_globals.player_obj.get_color()
            # Clear the selected route index
            self.game_view.selected_route_index = None

        elif selected_color == "wild":
            # For wild without specific selection, claim first available
            for i, taken in enumerate(self.game_view.route_taken[pair]):
                if not taken:
                    self.game_view.route_taken[pair][i] = True
                    for train_sprite in self.game_view.train_map[pair][i]:
                        train_sprite.texture = player_tex
                        train_sprite.alpha = 255
                        train_sprite.claimed_by = game_globals.player_obj.get_color()
                    break
        else:
            # Regular card
            for i, (taken, route_data) in enumerate(
                    zip(self.game_view.route_taken[pair], routes_data)):
                if not taken and (route_data["color"] == selected_color or
                                  route_data["color"] == "colorless"):
                    self.game_view.route_taken[pair][i] = True
                    for train_sprite in self.game_view.train_map[pair][i]:
                        train_sprite.texture = player_tex
                        train_sprite.alpha = 255
                        train_sprite.claimed_by = game_globals.player_obj.get_color()
                    break
        # Remove train cards
        removed = game_globals.player_obj.get_train_cards().remove_cards(selected_color, len_route)
        game_globals.discard_deck.add_cards(removed)

        # Remove route from deck
        game_globals.player_obj.get_map().add_path(game_globals.
                                                   game_map.remove_route(city1, city2))

    def claim_route_comp(self, city1, city2, color, computer_player, route_index=None):
        """Claim the route for a computer player"""
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)

        if city_pair in c.TRAINS:
            routes_data = c.TRAINS[city_pair]
            pair = city_pair
        elif reverse_pair in c.TRAINS:
            routes_data = c.TRAINS[reverse_pair]
            pair = reverse_pair
        else:
            return

        comp_tex = arcade.load_texture(
            computer_player.get_sprite()
        )

        # Check if we have a specific route index selected
        if route_index is not None:
            # Claim the specifically selected route
            if not self.game_view.route_taken[pair][route_index]:
                self.game_view.route_taken[pair][route_index] = True
                for train_sprite in self.game_view.train_map[pair][route_index]:
                    train_sprite.texture = comp_tex
                    train_sprite.alpha = 255
                    train_sprite.claimed_by = computer_player.get_color()
        elif color == "wild":
            # For wild without specific selection, claim first available
            for i, taken in enumerate(self.game_view.route_taken[pair]):
                if not taken:
                    self.game_view.route_taken[pair][i] = True
                    for train_sprite in self.game_view.train_map[pair][i]:
                        train_sprite.texture = comp_tex
                        train_sprite.alpha = 255
                        train_sprite.claimed_by = computer_player.get_color()
                    break
        else:
            # Regular card
            for i, (taken, route_data) in enumerate(
                    zip(self.game_view.route_taken[pair], routes_data)):
                if not taken and (route_data["color"] == color or
                                  route_data["color"] == "colorless"):
                    self.game_view.route_taken[pair][i] = True
                    for train_sprite in self.game_view.train_map[pair][i]:
                        train_sprite.texture = comp_tex
                        train_sprite.alpha = 255
                        train_sprite.claimed_by = computer_player.get_color()
                    break

        # Print the action on the screen
        self.game_view.add_log(
            f"Computer player {computer_player.get_color()} "
            f"claimed the route {city1} - {city2}")

    def valid_route_colors(self, selected_color, city1, city2):
        """Get available colors for the route and checking if double colored routes are taken"""
        for city_pair in [(city1, city2), (city2, city1)]:
            if city_pair in c.TRAINS:
                routes_data = c.TRAINS[city_pair]
                len_route = len(c.TRAINS[city_pair][0]["positions"])
                route_taken = self.game_view.route_taken[city_pair]

                # Make sure they have enough trains
                if game_globals.player_obj.get_trains() < len_route:
                    return 3

                # Check if this is a wild
                if selected_color == "wild":
                    # Check if there's at least one available route
                    for taken, route_data in zip(route_taken, routes_data):
                        if not taken:
                            if (game_globals.player_obj.
                                    get_train_cards().get_count("wild") >= len_route):
                                return 0
                            return 1
                    return 2
                # For regular colors, check if the color matches an available route
                for taken, route_data in zip(route_taken, routes_data):
                    # If route is not taken and color matches (or route is colorless)
                    if not taken and (route_data["color"] == selected_color
                                      or route_data["color"] == "colorless"):
                        if (game_globals.player_obj.
                                get_train_cards().has_cards(selected_color, len_route)):
                            return 0
                        return 1
                # If we get here, no available route matches the selected color
                return 2
        return 2

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
        wild_card_count = 0

        for i in range(min(5, game_globals.faceup_deck.get_len())):
            card = game_globals.faceup_deck.get_card_at_index(i)
            if card and card.get_color() == "wild":
                wild_card_count += 1

        if wild_card_count >= 3:
            print(f"Refreshing face-up cards due to {wild_card_count} wild cards")
            self.game_view.add_log(f"Face-up deck refreshed (3+ wild cards)")

            # Move current face-up cards to discard deck
            game_globals.faceup_deck.discard(game_globals.discard_deck)

            # refresh deck
            if game_globals.train_deck.get_len() == 0 and game_globals.discard_deck.get_len() > 0:
                game_globals.train_deck.refresh_deck(game_globals.discard_deck)
                print("Refreshed train deck for face-up card replacement")

            # Re-populate 5 face-up cards
            for i in range(5):
                if game_globals.train_deck.get_len() > 0:
                    new_card = game_globals.train_deck.remove(-1)
                    game_globals.faceup_deck.add(new_card)
                else:
                    print("Not enough cards to fully refill face-up deck")
                    break

        # Update the first 5 cards display
        for i in range(5):
            if i < len(self.game_view.card_list):
                card_sprite = self.game_view.card_list[i]
                # Make sure we don't go out of bounds of the face-up deck
                if i < game_globals.faceup_deck.get_len():
                    faceup_card = game_globals.faceup_deck.get_card_at_index(i)
                    sprite_path = faceup_card.get_sprite()

                    # Cache the texture to avoid repeated loading
                    if not hasattr(self.game_view, 'faceup_textures'):
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
            "orange": game_globals.player_obj.get_train_cards().get_count("orange"),
            "black": game_globals.player_obj.get_train_cards().get_count("black"),
            "blue": game_globals.player_obj.get_train_cards().get_count("blue"),
            "green": game_globals.player_obj.get_train_cards().get_count("green"),
            "pink": game_globals.player_obj.get_train_cards().get_count("pink"),
            "red": game_globals.player_obj.get_train_cards().get_count("red"),
            "white": game_globals.player_obj.get_train_cards().get_count("white"),
            "yellow": game_globals.player_obj.get_train_cards().get_count("yellow"),
            "wild": game_globals.player_obj.get_train_cards().get_count("wild"),
        }

        # Update the display text
        colors = ["orange", "black", "blue", "green", "pink", "red", "white", "yellow", "wild"]
        for i, color in enumerate(colors):
            if i < len(self.game_view.index_cards):
                self.game_view.index_cards[i].text = str(color_counts[color])

        # Toggle visibility of the hand sprites using normalized (lowercase) color keys
        for color_key, spr in self.game_view.hand_card_sprite_by_color.items():
            # use the counts we already computed; fallback to querying the deck if missing
            count = color_counts.get(color_key,
                                     game_globals.player_obj.get_train_cards().get_count(color_key))
            spr.alpha = 255 if count > 0 else 0


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

        self.leaderboard_lines = []

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
            ("BLACK", "black.png"), ("WHITE", "white.png"), ("WILD", "wild.png")
        ]

        for color_name, filename in color_cards:
            self.color_textures[color_name] = arcade.load_texture(f"images/{filename}")

        self.destination_textures = {}
        self.faceup_textures = {}

        # Train pieces
        # One list for all train sprites (create it ONCE)
        self.train_list = arcade.SpriteList()

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
                        train_sprite.claimed_by = None # track who claimed the route
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

            self.board_renderer.place_card(card, sx, sy, top_left=True, scale = c.CARD_SCALE)
            self.card_list.append(card)
            i += 1

        self.hand_card_sprite_by_color = {}
        # Player's hand card set up
        for name, (sx, sy, filename) in c.PLAYER_CARDS.items():
            card = arcade.Sprite()
            card.texture = self.card_textures[name]
            self.board_renderer.place_card(card, sx, sy, top_left=True, scale=c.CARD_SCALE)
            # Normalize the deck color key
            color_key = name.lower()

            # show only if the player has at least 1 of this color
            count = game_globals.player_obj.get_train_cards().get_count(color_key)
            card.alpha = 255 if count > 0 else 0

            self.hand_card_sprite_by_color[color_key] = card
            self.card_list.append(card)

        # Banners
        self.train_cards_banner = arcade.Sprite("images/train_cards_banner.png", scale=0.435)
        cx, cy = self.board_renderer.img_to_screen(2840, 910, top_left=True)
        self.train_cards_banner.center_x = cx
        self.train_cards_banner.center_y = cy

        self.dest_cards_banner = arcade.Sprite("images/dest_cards_banner.png", scale=0.435)
        cx, cy = self.board_renderer.img_to_screen(2840, -35, top_left=True)
        self.dest_cards_banner.center_x = cx
        self.dest_cards_banner.center_y = cy

        self.leaderboard_banner = arcade.Sprite("images/leaderboard_banner.png", scale=0.40)
        lx, ly = self.board_renderer.img_to_screen(1250, -40, top_left=True)
        self.leaderboard_banner.center_x = lx
        self.leaderboard_banner.center_y = ly

        # Deck sprite set up
        self.deck = arcade.Sprite("images/deck.png", scale=c.CARD_SCALE)
        sx, sy = self.board_renderer.img_to_screen(-60, 280, top_left=True)
        self.deck.center_x = sx
        self.deck.center_y = sy

        # Destination deck sprite set up
        self.dest_deck = arcade.Sprite("images/dest_deck.png", scale=c.CARD_SCALE)
        sx, sy = self.board_renderer.img_to_screen(2560, 240, top_left=True)
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
        self.show_computers_playing_popup = False
        self.computer_turn_active = False
        self.computer_turn_index = 0
        self.computer_turn_timer = 0.0
        self.computer_turn_delay = 0.75
        self.showing_allowed_popup = False
        self.popup_city1 = None
        self.popup_city2 = None
        self.popup_route_length = 0
        self.color_buttons = []
        self.dest_buttons = []
        self.min_dest_cards_to_keep = game_globals.num_choose
        self.max_dest_cards_to_keep = 8
        self.showing_faceup_popup = False # Don't show face up popup
        self.showing_dest_card_popup = False # Don't show dest card popup
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
        self.info_button = arcade.Sprite("images/info_button.png", scale=0.1)
        self.info_button.center_x = 50  # Top left position
        self.info_button.center_y = c.WINDOW_HEIGHT - 50
        self.info_button_bounds = None
        self.showing_info_popup = True

        # Calculate info button bounds
        info_button_width = self.info_button.width
        info_button_height = self.info_button.height
        self.info_button_bounds = (
            self.info_button.center_x - info_button_width / 2,
            self.info_button.center_x + info_button_width / 2,
            self.info_button.center_y - info_button_height / 2,
            self.info_button.center_y + info_button_height / 2
        )

        self.layout_ui()
        self.dest_first_time = True

        self.log_messages: list[str] = []
        self.max_log_messages = 3

        self.log_lines: list[arcade.Text] = []

        x = c.SCREEN_WIDTH * 0.1
        y = c.SCREEN_HEIGHT * 0.03
        line_size = 32

        for i in range(self.max_log_messages):
            text_obj = arcade.Text(
                "",  # start empty
                x,
                y + i * line_size,
                arcade.color.WHITE,
                15,
                anchor_x="left",
            )
            self.log_lines.append(text_obj)

    def reset(self):
        """Restart the game"""
        self.game_initializer.reset()

    def on_draw(self):
        """Render the screen"""
        self.clear()

        self.board_renderer.on_draw()

        if self.show_computers_playing_popup:
            popups.computers_playing(self)

    def on_mouse_motion(self, x, y, dx, dy):
        """Handle mouse motion"""
        self.mouse_handler.on_mouse_motion(x, y, dx, dy)

    def on_update(self, delta_time):
        """Update game state"""

        # Check if its the last turn
        if self.win_conditions():
            self.win_screen()
            return

        game_globals.train_deck.shuffle()
        if game_globals.discard_deck.get_len() > 0 and game_globals.train_deck.get_len() < 5:
            game_globals.train_deck.refresh_deck(game_globals.discard_deck)
            self.card_controller.refresh_faceup_cards()

        if game_globals.faceup_deck.get_len() < 5 \
                and game_globals.train_deck.get_len() > 0:
            new_card = game_globals.train_deck.remove(-1)
            game_globals.faceup_deck.cards.insert(4, new_card)

        if game_globals.turn_val is not None:
            if game_globals.turn_val >= 2:
                game_globals.turn_end = True
                game_globals.turn_val = None

        # Track when a human player completes their turn
        if game_globals.turn_end and not game_globals.turn_end_comp:
            # Human player just finished their turn
            if hasattr(self, 'final_round_active') and self.final_round_active:
                self.final_round_turns_completed += 1
                print(f"Human turn completed in final round. Total turns: {self.final_round_turns_completed}")

            game_globals.turn_end_comp = True

        # initialize computer-turn popup and state once
        if game_globals.turn_end and game_globals.turn_end_comp and not self.computer_turn_active:
            print("Starting computer turns")

            self.computer_turn_active = True
            self.show_computers_playing_popup = True
            self.computer_turn_index = 0
            self.computer_turn_timer = 0.0

            return

        # process computer turns one per frame
        if self.computer_turn_active:
            self.computer_turn_timer += delta_time

            # wait a short delay so popup remains visible
            if self.computer_turn_timer < self.computer_turn_delay:
                return

            self.computer_turn_timer = 0.0

            # finish computer turns
            if self.computer_turn_index >= len(game_globals.computers):
                print("All computers finished")

                self.computer_turn_active = False
                self.show_computers_playing_popup = False

                # Count computer turns for final round
                if hasattr(self, 'final_round_active') and self.final_round_active:
                    self.final_round_turns_completed += len(game_globals.computers)
                    print(f"Computer turns completed in final round. Total turns: {self.final_round_turns_completed}")

                game_globals.turn_end_comp = False
                game_globals.turn_end = False
                game_globals.card_drawn = 0

                return

            # play exactly one computer turn
            comp = game_globals.computers[self.computer_turn_index]

            if (game_globals.train_deck.get_len() == 0 and
                    game_globals.discard_deck.get_len() > 0):
                game_globals.train_deck.refresh_deck(game_globals.discard_deck)
                print("Refreshed train deck before computer turn")

            print(f"Computer {comp.get_color()} playing.")
            train_cards_before = comp.get_player().get_train_cards().get_len()
            dest_cards_before = comp.get_player().get_destination_cards().get_len()

            comp.play()

            train_cards_after = comp.get_player().get_train_cards().get_len()
            dest_cards_after = comp.get_player().get_destination_cards().get_len()

            if train_cards_after - train_cards_before > 0:
                self.add_log(f"Computer {comp.get_color()} took train cards.")
            if dest_cards_after - dest_cards_before > 0:
                self.add_log(f"Computer {comp.get_color()} drew from Destination Card Deck")

            self.card_controller.refresh_faceup_cards()
            print(comp.get_player().get_train_cards())
            print(f"Computer {comp.get_color()} completed its turn.")

            self.computer_turn_index += 1
            return

    def add_log(self, message: str):
        """Add a message to the game log"""
        self.log_messages.append(message)
        if len(self.log_messages) > 50:
            self.log_messages.pop(0)

    def write_log(self):
        """Update the log Text objects with the latest messages."""
        visible = self.log_messages[-self.max_log_messages:]

        # We want newest at the bottom, so reverse
        visible = list(reversed(visible))

        for i, text_obj in enumerate(self.log_lines):
            if i < len(visible):
                text_obj.text = visible[i]
                text_obj.alpha = 255
            else:
                text_obj.text = ""
                text_obj.alpha = 0

    def sprite_to_name(self, spr: arcade.Sprite) -> str:
        """Get city name from sprite"""
        return self.route_controller.sprite_to_name(spr)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """Handle mouse press"""
        return_val = self.mouse_handler.on_mouse_press(x, y, button, modifiers)
        if game_globals.turn_val is None and return_val is None:
            0
        elif game_globals.turn_val is not None and return_val is not None:
            game_globals.turn_val += return_val
        elif game_globals.turn_val is None and return_val > 0:
            game_globals.turn_val = return_val

    def on_key_press(self, symbol: int, modifiers: int):
        """Handle key press"""
        self.keyboard_handler.on_key_press(symbol, modifiers)

    def deselect_all_cities(self):
        """Deselect all cities"""
        self.route_controller.deselect_all_cities()

    def claim_route(self, city1, city2):
        """Claim route"""
        self.route_controller.claim_route(city1, city2)

        game_globals.player_obj.remove_trains(self.popup_route_length)
        if self.popup_route_length == 1:
            game_globals.player_obj.add_points(1)

        elif self.popup_route_length == 2:
            game_globals.player_obj.add_points(2)

        elif self.popup_route_length == 3:
            game_globals.player_obj.add_points(4)

        elif self.popup_route_length == 4:
            game_globals.player_obj.add_points(7)

        elif self.popup_route_length == 5:
            game_globals.player_obj.add_points(10)

        elif self.popup_route_length == 6:
            game_globals.player_obj.add_points(15)

        player_map = game_globals.player_obj.get_map()
        if city1 not in player_map.get_nodes():
            player_map.add_node(city1)
        if city2 not in player_map.get_nodes():
            player_map.add_node(city2)
        player_map.add_path(game_globals.game_map.remove_route(city1, city2))
        game_globals.turn_end = True
        """
        # THIS IS FOR FINDING PLAYER POINTS AND UPSATING COMPLETED ROUTES
        for dest_card in game_globals.player_obj.get_destination_cards().get_uncompleted():
            if player_map.check_completed(dest_card):
                dest_card.complete()
                game_globals.player_obj.add_points(dest_card.get_points())
        """
        print(game_globals.player_obj.get_destination_cards())
        #print(game_globals.player_obj.get_destination_cards().get_uncompleted())
        #print(player_map.check_completed(cards.DestinationCard(("Boston", "Miami", 12))))
        #print(player_map.get_nodes())
        #print(player_map)

    def claim_route_comp(self, city1, city2, color, computer_player, route_index=None):
        """Claim route for computer player"""
        # First claim the route visually
        self.route_controller.claim_route_comp(city1, city2, color, computer_player, route_index)

        # Get route length for point calculation
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)

        if city_pair in c.TRAINS:
            len_route = len(c.TRAINS[city_pair][0]["positions"])
        elif reverse_pair in c.TRAINS:
            len_route = len(c.TRAINS[reverse_pair][0]["positions"])
        else:
            len_route = 0

        if computer_player:
            # Remove trains and add points
            computer_player.remove_trains(len_route)

            # Point calculation
            if len_route == 1:
                computer_player.add_points(1)
            elif len_route == 2:
                computer_player.add_points(2)
            elif len_route == 3:
                computer_player.add_points(4)
            elif len_route == 4:
                computer_player.add_points(7)
            elif len_route == 5:
                computer_player.add_points(10)
            elif len_route == 6:
                computer_player.add_points(13)

            # Update computer's map
            player_map = computer_player.get_map()
            if city1 not in player_map.get_nodes():
                player_map.add_node(city1)
            if city2 not in player_map.get_nodes():
                player_map.add_node(city2)
            player_map.add_path(game_globals.game_map.remove_route(city1, city2))

        game_globals.turn_end = True

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

    def layout_ui(self):
        """Example margins in board-image pixels (tweak to taste)
        # These are distances from the board edges, not the window edges."""
        self.board_renderer.place_ui_anchor(self.info_button,
                                            anchor="topleft", margin_x=-50,
                                            margin_y=-20, base_scale=0.20)

        self.board_renderer.place_ui_anchor(self.train_cards_banner,
                                            anchor="bottomright", margin_x=160,
                                            margin_y=770, base_scale=1)

        self.board_renderer.place_ui_anchor(self.dest_cards_banner,
                                            anchor="topright", margin_x=160,
                                            margin_y=-20, base_scale=1)

        self.board_renderer.place_ui_anchor(self.leaderboard_banner,
                                            anchor="topleft", margin_x=1252,
                                            margin_y=-25, base_scale=0.975)

        # Update bounds after moving/scaling the info button
        w, h = self.info_button.width, self.info_button.height
        self.info_button_bounds = (
            self.info_button.center_x - w / 2,
            self.info_button.center_x + w / 2,
            self.info_button.center_y - h / 2,
            self.info_button.center_y + h / 2
        )

    def win_conditions(self):
        """Check if it is the last turn"""
        if hasattr(self, 'game_ended') and self.game_ended:
            return True

        players = [game_globals.player_obj]
        for comp in game_globals.computers:
            players.append(comp.get_player())

        # Check if last round
        if not hasattr(self, 'final_round_active'):
            for player in players:
                if player.get_trains() <= 2:
                    self.final_round_active = True
                    self.final_round_turns_completed = 0
                    self.final_round_triggered = True
                    self.add_log("Final round! Each player gets one more turn.")
                    break

        # If we're in final round, check if all players have taken their final turn
        if hasattr(self, 'final_round_active') and self.final_round_active:
            # Count how many players have taken their final turn
            total_players = len(players)

            # The game ends when all players (including the one who triggered it) have taken one final turn
            if self.final_round_turns_completed >= total_players:
                self.game_ended = True
                self.add_log("Game ended! Calculating scores...")
                return True

        return False

    def calculate_scores(self):
        """Calculate scores for all players"""
        players = [game_globals.player_obj]
        for comp in game_globals.computers:
            players.append(comp.get_player())

        for player in players:
            dest_cards = player.get_destination_cards().get_cards()
            player_map = player.get_map()
            completed_cards = 0
            not_completed_cards = 0
            for card in dest_cards:
                if player_map.check_completed(card):
                    player.add_points(card.get_points())
                    completed_cards += 1
                    self.add_log(
                        f"{player.get_color()} completed {card.get_city_1()}-{card.get_city_2()}: +{card.get_points()} points")
                else:
                    player.remove_points(card.get_points())
                    not_completed_cards += 1
                    self.add_log(
                        f"{player.get_color()} failed {card.get_city_1()}-{card.get_city_2()}: -{card.get_points()} points")


        longest_route_player = game_globals.game_map.longest_route(*players)
        if longest_route_player:
            longest_route_player.add_points(10)
            self.add_log(f"{longest_route_player.get_color()} has longest continuous route: +10 points")

        return players

    def win_screen(self):
        """Prepare and call win screen"""
        players = self.calculate_scores()

        # Prepare player data for win screen
        player_data = []
        for player in players:
            # Convert color to RGB for display
            color_map = {
                "red": (171, 38, 2),
                "blue": (10, 85, 161),
                "green": (115, 143, 43),
                "yellow": (241, 193, 19),
                "black": (0, 0, 0),
                "white": (255, 255, 255),
                "orange": (255, 165, 0),
                "pink": (255, 192, 203)
            }

            player_color = color_map.get(player.get_color().lower(), (255, 255, 255))
            # Determine if this player has the longest route
            has_longest_route = (game_globals.game_map.longest_route(*players) == player)

            player_data.append({
                "name": "You" if player == game_globals.player_obj else player.get_color().capitalize(),
                "color": player_color,
                "points": player.get_points(),
                "longest_path": has_longest_route
            })

            # Sort by points
        player_data.sort(key=lambda x: x["points"], reverse=True)
        win_view = WinScreenView()
        win_view.players = player_data
        self.window.show_view(win_view)



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


