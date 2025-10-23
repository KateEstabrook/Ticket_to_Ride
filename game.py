"""
Game Logic
"""

import deck, cards, graph, route, player

# Constants
from constants import ROUTES_LST, DESTINATIONS

if __name__ == "__main__":
    # Initailize Train Card Deck
    train_deck = deck.Deck('Draw')
    
    colors = ["pink", "blue", "orange", "white", "green", "yellow", "black", "red"]
    
    # Add color cards 
    for color in colors:
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

    red = player.Player("Red")
    players.append(red)
    yellow = player.Player("Yellow")
    players.append(yellow)
    green = player.Player("Green")
    players.append(green)
    blue = player.Player("Blue")
    players.append(blue)
    
    # TODO Have player choose color
    
    # Initialize Destination Card Deck
    dest_deck = deck.Deck("Destination")

    for dest in DESTINATIONS:
        dest_deck.add(cards.DestinationCard(dest))

    dest_deck.shuffle()

    # Draw first hand of train cards, 4 each
    for p in players:
        i = 0
        while i < 4:
            p.get_train_cards().add(train_deck.remove(0))
            i += 1
        print(f"{p} has {p.get_points()} points and {p.get_trains()} train pieces")
        print(p.get_train_cards())

    # TODO Deal Destination Cards


    # Initalize routes
    routes = []
    for rt in ROUTES_LST:
        routes.append(route.Route((rt)))

    # Initalize graph
    map = graph.Graph("", ROUTES_LST)

