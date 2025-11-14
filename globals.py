"""
Globals
"""

import deck
import cards
import route
import player
import graph
import constants as c

faceup_deck = []
train_deck = []
discard_deck = []
dest_deck = []
dest_draw = []
routes = []
players = []
computers = []
player_obj = player.Player("none")
game_map = graph.Graph(c.CITIES_KEYS, c.ROUTES_LST)

def initialize_game():
    global faceup_deck, train_deck, dest_deck, routes, players, player_obj, \
    dest_draw, discard_deck, num_choose, turn_end, turn_val
    # Initailize Train Card Deck
    train_deck = deck.Deck('Draw')
    faceup_deck = deck.Deck('Faceup')
    discard_deck = deck.Deck('Discard')

    num_choose = 2
    turn_end = False
    turn_val = None
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

    train_deck.shuffle()

    # Initailize players
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

    # TO DO Have player choose color

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

    # Initalize routes
    routes = []
    for rt in c.ROUTES_LST:
        routes.append(route.Route((rt)))

    # Initalize graph
    #map = graph.Graph("", c.ROUTES_LST)

    faceup_deck = deck.Deck("faceup")
    while faceup_deck.get_len() < 5:
        card_ = train_deck.remove(-1)
        color = card_.get_color()
        faceup_deck.add(card_)
        i += 1
