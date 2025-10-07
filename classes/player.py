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

    def add_points(self, points):
        self.points += points

    def remove_points(self, points):
        self.points -= points
    
    def remove_trains(self, trains):
        self.train_peices -= trains

    def get_points(self):
        return self.points
    
    def get_trains(self):
        return self.train_peices
    
    def get_color(self):
        return self.color
    