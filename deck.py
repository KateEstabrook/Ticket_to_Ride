"""
Train Cards Deck (essential, hard)
- Amount of each card remaining
- Shuffle
- Add card
- Remove card
- Name (Draw, Discard, Faceup, Player, …)
- Deck sprites (not yet)

Route Card Deck (30 routes) (essential, hard)
- Amount of cards remaining
- Shuffle
- Add card
- Remove card                                  
- Name (Draw, Discard, Faceup, Player, …)
- Deck sprites (not yet)
"""

import operator
import cards
import random

STARTING_NUM_CARDS = 0

class Deck:
        # Constructor
        def __init__(self, name):
            self.num_cards = STARTING_NUM_CARDS
            self.name = name
            self.cards = []
        
        # Randomizes order of cards in deck
        def shuffle(self):
            random.shuffle(self.cards)

        # Removes a card from the deck at a certian index and return it
        def remove(self, index):
            return self.cards.pop(index)
        
        # Remove a list of cards of a color + wild cards to make up for the count
        def remove_cards(self, color, count):
            if (self.has_cards(color, count)):
                i = 0
                while i < count:
                    try:
                        self.remove(self.get_card_index(color))
                    except TypeError:
                        self.remove(self.get_card_index("wild"))
                    i += 1
                
        # Adds a card
        def add(self, card):
            self.cards.append(card)

        # Checks if the passed cards are in the deck
        def has_cards(self, color, count):
            cards = []
            if self.get_count(color) >= count:
                return True
            elif self.get_count("wild") + self.get_count(color) >= count:
                return True
            else:
                return False

        # Sorts the deck
        def sort(self):
            self.cards.sort(key=operator.attrgetter('color'))

        # Getter
        def get_count(self, color):
            count = 0
            for card in self.cards:
                if card.get_color() == color:
                    count += 1
            return count
        
        # returns the index of a train card of a certain color
        def get_card_index(self, color):
            for card in self.cards:
                if card.get_color() == color:
                    return int(self.cards.index(card))
        
        # Returns the card at a certain index in the deck
        def get_card_at_index(self, index):
            lst = []
            for card in self.cards:
                lst.append(card)
            return lst[index]
        
        # Returns length of deck
        def get_len(self):
            count = 0
            for _ in self.cards:
                count += 1
            return count

        # To string
        def __str__(self):
            s = ""
            for card in self.cards:
                 s += str(card) + '\n'
            return f"{s}"
        
        def __eq__(self, other):
            # It's good practice to first check if 'other' is an instance of the same class
            if not isinstance(other, Deck):
                return NotImplemented  # Or raise TypeError("Can only compare with MyClass instances")

            # Define the equality logic based on the attributes
            return self.cards == other.cards