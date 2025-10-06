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

STARTING_NUM_CARDS = 0

class Deck:
        def __init__(self, name):
            self.num_cards = STARTING_NUM_CARDS
            self.name = name
            self.cards = []
        
        def shuffle(self):
              cards.random.shuffle()