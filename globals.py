"""
Constants file
"""

import deck
import cards
import graph
import route
import player
import constants as c


def initialize_game():
    """Game start (shuffling, dealing, itializing player colors)"""
    global faceup_deck, train_deck, dest_deck, routes, players, player_deck

    # Initialize Train Card Deck
    train_deck = deck.Deck('Draw')
    player_deck = deck.Deck('Player')
    faceup_deck = deck.Deck('Faceup')

    # Add color cards
    for color in c.COLORS:
        i = 0
        while i < 12:
            train_deck.add(cards.TrainCard(color))
            i += 1

    # Add wild cards
    i = 0
    while i < 14:
        train_deck.add(cards.TrainCard("wild"))
        i += 1

    # SHUFFLE the train deck
    train_deck.shuffle()

    # Create faceup deck from shuffled train deck
    while faceup_deck.get_len() < 5 and train_deck.get_len() > 0:
        card = train_deck.remove(0)  # Remove from top of deck
        faceup_deck.add(card)

    # Initialize players
    players = []

    # for color in c.PLAYER_COLORS:
    #     if color != player_color:
    #         players.append(player.Player(color))

    # red = player.Player("Red")
    # players.append(red)
    # yellow = player.Player("Yellow")
    # players.append(yellow)
    # green = player.Player("Green")
    # players.append(green)
    # blue = player.Player("Blue")
    # players.append(blue)

    # TODO Have player choose color

    # Initialize Destination Card Deck
    dest_deck = deck.Deck("destination")

    for dest in c.DESTINATIONS:
        dest_deck.add(cards.DestinationCard(dest))

    dest_deck.shuffle()

    # Draw first hand of train cards, 4 each
    for p in players:
        i = 0
        while i < 4:
            p.get_train_cards().add(train_deck.remove(0))
            i += 1

    # TODO Deal Destination Cards

    # Initalize routes
    routes = []
    for rt in c.ROUTES_LST:
        routes.append(route.Route((rt)))

    # Initalize graph
    map = graph.Graph("", c.ROUTES_LST)
