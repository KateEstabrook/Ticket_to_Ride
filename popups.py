"""
Stores all of the pop ups during game play
"""
import arcade
import constants as c
import globals
#import cards
#import board

def deck_pop_up(game_view):
    """
    Show a white rectangle pop-up with color selection buttons using card images
    """
    # Calculate dimensions and positions
    popup_width = c.WINDOW_WIDTH * 0.4
    popup_height = c.WINDOW_HEIGHT * 0.4
    popup_x = c.WINDOW_WIDTH // 2
    popup_y = c.WINDOW_HEIGHT // 2

    # Draw white rectangle using cached texture
    white_texture = game_view.popup_textures['white_bg']
    arcade.draw_texture_rect(
        white_texture,
        arcade.LBWH(
            popup_x - popup_width // 2,
            popup_y - popup_height // 2,
            popup_width,
            popup_height
        )
    )

    if game_view.drawn_card is not None:
        # Use cached texture for drawn card
        sprite_path = game_view.drawn_card.get_sprite()
        if sprite_path not in game_view.faceup_textures:
            game_view.faceup_textures[sprite_path] = arcade.load_texture(sprite_path)
        tex = game_view.faceup_textures[sprite_path]

        # Center it nicely inside the popup
        card_w = popup_width * 0.3
        aspect_ratio = tex.height / tex.width
        card_h = card_w * aspect_ratio
        card_rect = arcade.LBWH(popup_x - card_w / 2, popup_y - card_h / 2, card_w, card_h)
        arcade.draw_texture_rect(tex, card_rect)

    if game_view.drawn_card is not None:
        color_name = game_view.drawn_card.get_color().upper()
        arcade.draw_text(
            f"You got a(n) {color_name} card!",
            popup_x, popup_y + popup_height * 0.35,
            arcade.color.BLACK,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    # Add exit button in lower right corner
    continue_button_width = popup_width * 0.2
    continue_button_height = popup_height * 0.1
    continue_button_x = popup_x + popup_width * 0.48 - continue_button_width // 2
    continue_button_y = popup_y - popup_height * 0.45 + continue_button_height // 2

    exit_texture = game_view.popup_textures['save_button']
    exit_rect = arcade.LBWH(
        continue_button_x - continue_button_width // 2,
        continue_button_y - continue_button_height // 2,
        continue_button_width,
        continue_button_height
    )

    arcade.draw_texture_rect(exit_texture, exit_rect)
    arcade.draw_rect_outline(
        exit_rect,
        arcade.color.BLACK,
        border_width=2
    )

    arcade.draw_text(
        "CONTINUE",
        continue_button_x, continue_button_y,
        arcade.color.WHITE,
        font_size=12,
        anchor_x="center",
        anchor_y="center",
        bold=True
    )

    game_view.continue_button_bounds = (
        continue_button_x - continue_button_width // 2,  # left
        continue_button_x + continue_button_width // 2,  # right
        continue_button_y - continue_button_height // 2,  # bottom
        continue_button_y + continue_button_height // 2  # top
    )


def faceup_card_pop_up(game_view, card_index):
    """
    Show a white rectangle pop-up when a face-up card is clicked
    """
    # Calculate dimensions and positions
    popup_width = c.WINDOW_WIDTH * 0.4
    popup_height = c.WINDOW_HEIGHT * 0.4
    popup_x = c.WINDOW_WIDTH // 2
    popup_y = c.WINDOW_HEIGHT // 2

    # Draw white rectangle using cached texture
    white_texture = game_view.popup_textures['white_bg']
    arcade.draw_texture_rect(
        white_texture,
        arcade.LBWH(
            popup_x - popup_width // 2,
            popup_y - popup_height // 2,
            popup_width,
            popup_height
        )
    )

    # Get the selected face up card
    selected_card = globals.faceup_deck.get_card_at_index(card_index)

    if selected_card is not None:
        # Use cached texture for face-up card
        sprite_path = selected_card.get_sprite()
        if sprite_path not in game_view.faceup_textures:
            game_view.faceup_textures[sprite_path] = arcade.load_texture(sprite_path)
        tex = game_view.faceup_textures[sprite_path]

        # Calculate card dimensions
        card_w = popup_width * 0.3
        # Use the actual texture aspect ratio
        aspect_ratio = tex.height / tex.width
        card_h = card_w * aspect_ratio

        # Center it nicely inside the popup
        card_rect = arcade.LBWH(popup_x - card_w / 2, popup_y - card_h / 2, card_w, card_h)
        arcade.draw_texture_rect(tex, card_rect)

        # Draw card info text
        color_name = selected_card.get_color().upper()
        arcade.draw_text(
            f"You selected a(n) {color_name} card!",
            popup_x, popup_y + popup_height * 0.35,
            arcade.color.BLACK,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
            bold=True
        )

    # Add take button
    take_button_width = popup_width * 0.2
    take_button_height = popup_height * 0.1
    take_button_x = popup_x + popup_width * 0.25 - take_button_width // 2
    take_button_y = popup_y - popup_height * 0.45 + take_button_height // 2

    take_texture = game_view.popup_textures['save_button']
    take_rect = arcade.LBWH(
        take_button_x - take_button_width // 2,
        take_button_y - take_button_height // 2,
        take_button_width,
        take_button_height
    )

    arcade.draw_texture_rect(take_texture, take_rect)
    arcade.draw_rect_outline(
        take_rect,
        arcade.color.BLACK,
        border_width=2
    )

    arcade.draw_text(
        "TAKE CARD",
        take_button_x, take_button_y,
        arcade.color.WHITE,
        font_size=12,
        anchor_x="center",
        anchor_y="center",
        bold=True
    )

    game_view.take_button_bounds = (
        take_button_x - take_button_width // 2,  # left
        take_button_x + take_button_width // 2,  # right
        take_button_y - take_button_height // 2,  # bottom
        take_button_y + take_button_height // 2  # top
    )

    # Add exit button in lower right corner
    exit_button_width = popup_width * 0.2
    exit_button_height = popup_height * 0.1
    exit_button_x = popup_x + popup_width * 0.48 - exit_button_width // 2
    exit_button_y = popup_y - popup_height * 0.45 + exit_button_height // 2

    exit_texture = game_view.popup_textures['exit_button']
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

    game_view.exit_button_bounds = (
        exit_button_x - exit_button_width // 2,  # left
        exit_button_x + exit_button_width // 2,  # right
        exit_button_y - exit_button_height // 2,  # bottom
        exit_button_y + exit_button_height // 2  # top
    )

def route_popup(game_view, city1, city2):
    """
    Show a white rectangle pop-up with color selection buttons using card images
    """
    # Calculate dimensions and positions
    popup_width = c.WINDOW_WIDTH * 0.4
    popup_height = c.WINDOW_HEIGHT * 0.4
    popup_x = c.WINDOW_WIDTH // 2
    popup_y = c.WINDOW_HEIGHT // 2

    # Draw white rectangle using cached texture
    white_texture = game_view.popup_textures['white_bg']
    arcade.draw_texture_rect(
        white_texture,
        arcade.LBWH(
            popup_x - popup_width // 2,
            popup_y - popup_height // 2,
            popup_width,
            popup_height
        )
    )

    # Use pre loaded color textures
    card_textures = game_view.color_textures

    # Button dimensions and layout
    button_width = popup_width * 0.18
    button_height = popup_height * 0.15
    horizontal_spacing = popup_width * 0.1
    vertical_spacing = popup_height * 0.03

    # Starting position for the grid
    start_x = popup_x - popup_width * 0.3
    start_y = popup_y - popup_height * -0.2

    # Store button positions for click detection
    game_view.color_buttons = []

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

    # Draw cards
    for row in range(3):
        row_x = start_x

        for col in range(3):
            index = row * 3 + col
            # Calculate button position
            button_x = row_x + col * (button_width + horizontal_spacing)
            button_y = start_y - row * (button_height + vertical_spacing)
            color_name = color_cards[index][0]
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
            if game_view.selected_color == color_name.lower():
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
            game_view.color_buttons.append({
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

    exit_texture = game_view.popup_textures['exit_button']
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

    game_view.exit_button_bounds = (
        exit_button_x - exit_button_width // 2,  # left
        exit_button_x + exit_button_width // 2,  # right
        exit_button_y - exit_button_height // 2,  # bottom
        exit_button_y + exit_button_height // 2  # top
    )

    # Only show save button if a color has been selected
    if (game_view.selected_color and
            game_view.valid_route_colors(game_view.selected_color, city1, city2)):

        save_button_width = popup_width * 0.2
        save_button_height = popup_height * 0.1
        save_button_x = popup_x + popup_width * 0.25 - save_button_width // 2
        save_button_y = popup_y - popup_height * 0.45 + save_button_height // 2

        save_texture = game_view.popup_textures['save_button']
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

        game_view.save_button_bounds = (
            save_button_x - save_button_width // 2,  # left
            save_button_x + save_button_width // 2,  # right
            save_button_y - save_button_height // 2,  # bottom
            save_button_y + save_button_height // 2  # top
        )
    else:
        game_view.save_button_bounds = None

    # Add route information text
    route_length = game_view.popup_route_length
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
    if game_view.selected_color:
        status_text = f"Selected: {game_view.selected_color.upper()}"
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
    if (game_view.selected_color and
            not game_view.valid_route_colors(game_view.selected_color, city1, city2)):
        error_text = f"Cannot use {game_view.selected_color.upper()} card on this route!"
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

def show_dest_pop_up(self, dest_list, num):
    """
    Destination popup
    """
    # Popup dimensions
    popup_width = c.WINDOW_WIDTH * 0.4
    popup_height = c.WINDOW_HEIGHT * 0.4
    popup_x = c.WINDOW_WIDTH // 2
    popup_y = c.WINDOW_HEIGHT // 2

    left = popup_x - popup_width / 2
    bottom = popup_y - popup_height / 2

    # Shadow under popup using cached texture
    shadow_texture = self.popup_textures['shadow']
    shadow_rect = arcade.LBWH(left + 6, bottom - 6, popup_width, popup_height)
    arcade.draw_texture_rect(shadow_texture, shadow_rect)

    # Background color using cached texture
    bg_texture = self.popup_textures['white_bg']
    bg_rect = arcade.LBWH(left, bottom, popup_width, popup_height)
    arcade.draw_texture_rect(bg_texture, bg_rect)

    # Border
    arcade.draw_rect_outline(bg_rect, arcade.color.DARK_BROWN, border_width=3)

    # Title
    title = "Which destination cards would you like to keep?"
    arcade.draw_text(
        title,
        popup_x,
        popup_y + popup_height * 0.42,
        arcade.color.DARK_BROWN,
        font_size=18,
        anchor_x="center",
        anchor_y="center",
        bold=True
    )

    # Card layout
    card_width = popup_width * 0.26
    card_height = popup_height * 0.26
    horizontal_spacing = popup_width * 0.08
    vertical_spacing = popup_height * 0.12

    start_x = popup_x - (card_width / 2 + horizontal_spacing / 2)
    start_y = popup_y + popup_height * 0.2

    # Store card button data
    self.dest_buttons = []

    # Draw each card in a 2x2 grid
    for row in range(2):
        for col in range(2):
            index = row * 2 + col
            if index >= len(dest_list):
                continue

            # Card position
            card_x = start_x + col * (card_width + horizontal_spacing)
            card_y = start_y - row * (card_height + vertical_spacing)

            # Load card texture
            texture_path = dest_list[index].get_sprite()
            if texture_path not in self.destination_textures:
                self.destination_textures[texture_path] = arcade.load_texture(texture_path)
            texture = self.destination_textures[texture_path]

            # Card rectangle
            card_rect = arcade.LBWH(
                card_x - card_width / 2,
                card_y - card_height / 2,
                card_width,
                card_height
            )

            # Draw card
            arcade.draw_texture_rect(texture, card_rect)

            # Highlight selection
            # city1 = dest_list[index].get_city_1()
            # city2 = dest_list[index].get_city_2()
            # key = city1 + city2
            if dest_list[index] in self.selected_dests:
                border_color = arcade.color.GOLD
                border_width = 6
            else:
                border_color = arcade.color.DARK_BROWN
                border_width = 2
            arcade.draw_rect_outline(card_rect, border_color, border_width)

            # Save for click detection
            self.dest_buttons.append({
                'card': dest_list[index],
                'bounds': (
                    card_x - card_width / 2,
                    card_x + card_width / 2,
                    card_y - card_height / 2,
                    card_y + card_height / 2
                )
            })

    # Only show save button if you have selected greater than or equal to 2 dest cards
    if len(self.selected_dests) >= num:
        save_button_width = popup_width * 0.2
        save_button_height = popup_height * 0.1
        save_button_x = popup_x
        save_button_y = popup_y - popup_height * 0.42

        save_texture = self.popup_textures['save_button']
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

    return 0

def show_info_pop_up(game_view):
    """
    Help menu popup
    """
    # Popup dimensions
    popup_width = c.WINDOW_WIDTH * 0.75
    popup_height = c.WINDOW_HEIGHT * 0.75
    popup_x = c.WINDOW_WIDTH // 2
    popup_y = c.WINDOW_HEIGHT // 2

    left = popup_x - popup_width / 2
    bottom = popup_y - popup_height / 2

    # Shadow under popup using cached texture
    shadow_texture = game_view.popup_textures['shadow']
    shadow_rect = arcade.LBWH(left + 6, bottom - 6, popup_width, popup_height)
    arcade.draw_texture_rect(shadow_texture, shadow_rect)

    # Background color using cached texture
    bg_texture = game_view.popup_textures['white_bg']
    bg_rect = arcade.LBWH(left, bottom, popup_width, popup_height)
    arcade.draw_texture_rect(bg_texture, bg_rect)

    # Border
    arcade.draw_rect_outline(bg_rect, arcade.color.DARK_BROWN, border_width=3)

    # Title
    title = "How To Play"
    arcade.draw_text(
        title,
        popup_x,
        popup_y + popup_height * 0.42,
        arcade.color.DARK_BROWN,
        font_size=18,
        anchor_x="center",
        anchor_y="center",
        bold=True
    )

    # Add exit button in lower right corner
    exit_button_width = popup_width * 0.2
    exit_button_height = popup_height * 0.1
    exit_button_x = popup_x + popup_width * 0.48 - exit_button_width // 2
    exit_button_y = popup_y - popup_height * 0.45 + exit_button_height // 2

    exit_texture = game_view.popup_textures['exit_button']
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

    game_view.exit_button_bounds = (
        exit_button_x - exit_button_width // 2,  # left
        exit_button_x + exit_button_width // 2,  # right
        exit_button_y - exit_button_height // 2,  # bottom
        exit_button_y + exit_button_height // 2  # top
    )
