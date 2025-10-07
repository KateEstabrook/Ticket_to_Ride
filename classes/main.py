import city
import player
import route
import deck
import cards


ROUTES = [("Vancouver", "Seattle", 1, "colorless"), ("Vancouver", "Calgary", 3, "colorless"), 
          ("Seattle", "Portland", 1, "colorless"), ("Seattle", "Calgary", 4, "colorless"),
          ("Seattle", "Helena", 6, "yellow"), ("Portland", "San Francisco", 5, "green"),
          ("Portland", "San Francisco", 5, "pink"), ("Portland", "Salt Lake City", 6, "blue"),
          ("San Francisco", "Salt Lake City", 5, "white"), ("San Francisco", "Salt Lake City", 5, "orange")
          ("San Francisco", "Los Angeles", 3, "yellow"), ("San Francisco", "Los Angeles", 3, "pink"),
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
          ("Duluth", "Omaha", 2, "colorless"), ("Duluth", "Sault St. Marie", 3, "colorless"),
          ("Duluth", "Chicago", 3, "red"), ("Duluth", "Totonto", 6, "pink"), 
          ("Omaha", "Chicago", 4, "blue"), ("Omaha", "Kansas City", 1, "colorless"), 
          ("Omaha", "Kansas City", 1, "colorless"), ("Kansas City", "Saint Louis", 2, "pink"),
          ("Kansas City", "Saint Louis", 2, "blue"),
          ] 



ROUTES = {
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


def train_deck_test():
    train_deck = deck.Deck('Test')
    train_deck.add(cards.TrainCard('blue'))
    train_deck.add(cards.TrainCard('red'))
    train_deck.add(cards.TrainCard('blue'))
    train_deck.add(cards.TrainCard('yellow'))
    train_deck.add(cards.TrainCard('green'))
    train_deck.sort()

    print(train_deck)

def destination_deck_test():
    destination_deck = deck.Deck('Test')
    destination_deck.add(cards.DestinationCard(('Deluth', 'Denver'), 1))
    destination_deck.add(cards.DestinationCard(('Boston', 'New York'), 4))
    destination_deck.add(cards.DestinationCard(('Salt Lake City', 'Montrael'), 2))
    destination_deck.add(cards.DestinationCard(('Deluth', 'New York'), 1))
    destination_deck.add(cards.DestinationCard(('Charleston', 'Denver'), 5))

    print(destination_deck)

train_deck_test()
destination_deck_test()