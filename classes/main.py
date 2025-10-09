"""
Main / testing
"""

#import city
#import player
import route
import deck
import cards
import graph


ROUTES = [("Vancouver", "Seattle", 1, "colorless"), ("Vancouver", "Seattle", 1, "colorless"),
          ("Vancouver", "Calgary", 3, "colorless"), ("Seattle", "Portland", 1, "colorless"),
          ("Seattle", "Portland", 1, "colorless"), ("Seattle", "Calgary", 4, "colorless"),
          ("Seattle", "Helena", 6, "yellow"), ("Portland", "San Francisco", 5, "green"),
          ("Portland", "San Francisco", 5, "pink"), ("Portland", "Salt Lake City", 6, "blue"),
          ("San Francisco", "Salt Lake City", 5, "white"),
          ("San Francisco", "Salt Lake City", 5, "orange"),
          ("San Francisco", "Los Angeles", 3, "yellow"),
          ("San Francisco", "Los Angeles", 3, "pink"),
          ("Los Angeles", "Las Vegas", 2, "colorless"), ("Los Angeles", "Phoenix", 3, "colorless"),
          ("Los Angeles", "El Paso", 6, "black"), ("Calgary", "Helena", 4, "colorless"),
          ("Calgary", "Winnipeg", 6, "white"), ("Helena", "Salt Lake City", 3, "pink"),
          ("Helena", "Winnipeg", 4, "blue"), ("Helena", "Duluth", 6, "orange"),
          ("Helena", "Omaha", 5, "red"), ("Helena", "Denver", 4, "green"),
          ("Salt Lake City", "Denver", 3, "red"), ("Salt Lake City", "Denver", 3, "yellow"),
          ("Salt Lake City", "Las Vegas", 3, "orange"), ("Phoenix", "Denver", 5, "white"),
          ("Phoenix", "Santa Fe", 3, "colorless"), ("Phoenix", "El Paso", 3, "colorless"),
          ("Winnipeg", "Duluth", 4, "black"), ("Winnipeg", "Sault St. Marie", 6, "colorless"),
          ("Denver", "Omaha", 4, "pink"), ("Denver", "Oklahoma City", 4, "red"),
          ("Denver", "Santa Fe", 2, "colorless"), ("Denver", "Kansas City", 4, "black"),
          ("Denver", "Kansas City", 4, "orange"), ("Santa Fe", "El Paso", 2, "colorless"),
          ("Santa Fe", "Oklahoma City", 3, "blue"), ("El Paso", "Oklahoma City", 5, "yellow"),
          ("El Paso", "Dallas", 4, "red"), ("El Paso", "Houston", 6, "green"),
          ("Duluth", "Omaha", 2, "colorless"), ("Duluth", "Omaha", 2, "colorless"),
          ("Duluth", "Sault St. Marie", 3, "colorless"),
          ("Duluth", "Chicago", 3, "red"), ("Duluth", "Toronto", 6, "pink"),
          ("Omaha", "Chicago", 4, "blue"), ("Omaha", "Kansas City", 1, "colorless"),
          ("Omaha", "Kansas City", 1, "colorless"), ("Kansas City", "Saint Louis", 2, "pink"),
          ("Kansas City", "Saint Louis", 2, "blue"),
          ("Kansas City", "Oklahoma City", 2, "colorless"),
          ("Kansas City", "Oklahoma City", 2, "colorless"),
          ("Oklahoma City", "Dallas", 2, "colorless"),
          ("Oklahoma City", "Dallas", 2, "colorless"),
          ("Oklahoma City", "Little Rock", 2, "colorless"),
          ("Dallas", "Houston", 1, "colorless"), ("Dallas", "Houston", 1, "colorless"),
          ("Dallas", "Little Rock", 2, "colorless"), ("Houston", "New Orleans", 2, "colorless"),
          ("Sault St. Marie", "Montreal", 5, "black"),
          ("Sault St. Marie", "Toronto", 2, "colorless"),
          ("Chicaco", "Toronto", 4, "white"), ("Chicaco", "Saint Louis", 2, "white"),
          ("Chicaco", "Saint Louis", 2, "green"), ("Chicaco", "Pittsburgh", 3, "black"),
          ("Chicaco", "Pittsburgh", 3, "orange"), ("Saint Louis", "Pittsburgh", 5, "green"),
          ("Saint Louis", "Nashville", 2, "colorless"),
          ("Saint Louis", "Little Rock", 2, "colorless"),
          ("Little Rock", "Nashville", 3, "white"), ("Little Rock", "New Orleans", 3, "green"),
          ("New Orleans", "Atlanta", 4, "yellow"), ("New Orleans", "Atlanta", 4, "orange"),
          ("New Orleans", "Miami", 6, "red"), ("Toronto", "Montreal", 3, "colorless"),
          ("Toronto", "Pittsburgh", 2, "colorless"), ("Pittsburgh", "New York", 2, "white"),
          ("Pittsburgh", "New York", 2, "green"), ("Pittsburgh", "Nashville", 4, "yellow"),
          ("Pittsburgh", "Washington", 2, "colorless"), ("Pittsburgh", "Raleigh", 2, "colorless"),
          ("Nashville", "Atlanta", 1, "colorless"), ("Nashville", "Raleigh", 3, "black"),
          ("Atlanta", "Raleigh", 2, "colorless"),  ("Atlanta", "Raleigh", 2, "colorless"),
          ("Atlanta", "Charleston", 2, "colorless"), ("Atlanta", "Miami", 5, "blue"),
          ("Charleston", "Raleigh", 2, "colorless"), ("Charleston", "Miami", 4, "pink"),
          ("Raleigh", "Washington", 2, "colorless"), ("Raleigh", "Washington", 2, "colorless"),
          ("Washington", "New York", 2, "orange"), ("Washington", "New York", 2, "black"),
          ("New York", "Montreal", 4, "blue"), ("New York", "Boston", 2, "red"),
          ("New York", "Boston", 2, "yellow"), ("Boston", "Montreal", 2, "colorless"),
          ("Boston", "Montreal", 2, "colorless")]


def train_deck_test():
    """
    train test
    """
    train_deck = deck.Deck('Test')
    train_deck.add(cards.TrainCard('blue'))
    train_deck.add(cards.TrainCard('red'))
    train_deck.add(cards.TrainCard('blue'))
    train_deck.add(cards.TrainCard('yellow'))
    train_deck.add(cards.TrainCard('green'))
    train_deck.sort()

    print(train_deck)

def destination_deck_test():
    """
    destination deck test
    """
    destination_deck = deck.Deck('Test')
    destination_deck.add(cards.DestinationCard(('Deluth', 'Denver'), 1))
    destination_deck.add(cards.DestinationCard(('Boston', 'New York'), 4))
    destination_deck.add(cards.DestinationCard(('Salt Lake City', 'Montrael'), 2))
    destination_deck.add(cards.DestinationCard(('Deluth', 'New York'), 1))
    destination_deck.add(cards.DestinationCard(('Charleston', 'Denver'), 5))

    print(destination_deck)

def route_test():
    """
    route test
    """
    routes = []
    for rt in ROUTES:
        routes.append(route.Route((rt)))

    for r in routes:
        print(r)


map = graph.Graph("", ROUTES)

train_deck_test()
destination_deck_test()
route_test()
print(len(ROUTES))
print(map)

