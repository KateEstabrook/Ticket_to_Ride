"""
- Destination cards
    - City names
    - Points
    - Completed/Uncompleted

- Train Cards
    - Colors of card
    - Sprites by color (not yet)
"""

class DestinationCard:
    def __init__(self, cities, points):
        self.city_1 = cities[0]
        self.city_2 = cities[1]
        self.points = points
        completed = False


class TrainCard:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color
