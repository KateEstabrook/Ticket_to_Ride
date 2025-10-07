""" 
Player class: 
- Train Pieces Num
- Points
- Destination Cards Deck
- Train Cards Deck
- Claimed Routes??
- Color (ID)
"""
# Constants

INIT_TRAIN_PEICES = 45
STARTING_POINTS = 0

class Player:
    def __init__(self, color):
        self.color = color
        self.train_peices = INIT_TRAIN_PEICES
        self.points = STARTING_POINTS
        # TODO Destinations deck
        # TODO Train cards deck