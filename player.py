""" 
Player class: 
- Train Pieces Num
- Points
- Destination Cards Deck
- Train Cards Deck
- Claimed Routes??
- Color (ID)
"""
import deck

# Constants
INIT_TRAIN_PEICES = 45
STARTING_POINTS = 0

class Player:
    # Constructor
    def __init__(self, color):
        self.color = color
        self.train_peices = INIT_TRAIN_PEICES
        self.points = STARTING_POINTS
        self.train_cards = deck.Deck('train_cards')
        self.destination_cards = deck.Deck('destination_cards')
        self.sprite = f"images/train_piece_{color}.png"
        # TODO Destinations deck
        # TODO Train cards deck

    # Add points to player
    def add_points(self, points):
        self.points += points

    # Add cards to a player deck
    def add_card(self, deck, card):
        deck.add(card)

    # Remove points from player
    def remove_points(self, points):
        self.points -= points
    
    # Remove train pieces from player
    def remove_trains(self, trains):
        self.train_peices -= trains

    # Remove cards from player deck
    def remove_card(self, deck, index):
        return deck.remove(index)

    # Getters
    def get_points(self):
        return self.points
    
    def get_trains(self):
        return self.train_peices
    
    def get_color(self):
        return self.color
    
    def get_train_cards(self):
        return self.train_cards

    def get_destination_cards(self):
        return self.destination_cards
    
    def get_sprite(self):
        return self.sprite
    
    # To string
    def __str__(self):
        return f"{self.color} Player"