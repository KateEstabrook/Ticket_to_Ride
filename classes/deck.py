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

STARTING_NUM_CARDS = 0

class Deck:
        def __init__(self, name):
            self.num_cards = STARTING_NUM_CARDS
            self.name = name
            self.cards = []
        
        def shuffle(self):
            self.cards.random.shuffle()
        
        def get_count(self, color):
            count = 0
            for card in self.cards:
                if card.get_color() == color:
                    count += 1
            return count

        def remove(self, index):
            return self.cards.pop(index)
        
        def add(self, card):
             self.cards.append(card)

        def sort(self):
             self.cards.sort(key=operator.attrgetter('color'))
        
        def __str__(self):
            s = ""
            for card in self.cards:
                 s += str(card) + '\n'
            return f"{s}"