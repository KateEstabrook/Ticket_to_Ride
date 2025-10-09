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
        
        # Adds a card
        def add(self, card):
            self.cards.append(card)

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