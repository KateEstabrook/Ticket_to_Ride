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
    """Player class"""
    # Constructor
    def __init__(self, color):
        self.color = color
        self.train_peices = INIT_TRAIN_PEICES
        self.points = STARTING_POINTS
        self.train_cards = deck.Deck('train_cards')
        self.destination_cards = deck.Deck('destination_cards')
        self.sprite = f"images/train_piece_{color}.png"

    def add_points(self, points):
        """Add points to player"""
        self.points += points

    def add_card(self, deck_, card):
        """Add cards to a player deck"""
        deck_.add(card)

    def remove_points(self, points):
        """Remove points from player"""
        self.points -= points

    def remove_trains(self, trains):
        """Remove train pieces from player"""
        self.train_peices -= trains

    def remove_card(self, deck_, index):
        """Remove cards from player deck"""
        return deck_.remove(index)

    def get_points(self):
        """Getter for points"""
        return self.points

    def get_trains(self):
        """Getter for trains"""
        return self.train_peices

    def get_color(self):
        """Getter for color"""
        return self.color

    def get_train_cards(self):
        """Getter for train cards"""
        return self.train_cards

    def get_destination_cards(self):
        """Getter for destination cards"""
        return self.destination_cards

    def get_sprite(self):
        """Getter for sprite"""
        return self.sprite

    def set_color(self, color):
        self.color = color

    def __str__(self):
        """To string"""
        return f"{self.color} Player"
