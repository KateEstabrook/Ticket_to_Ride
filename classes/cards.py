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
    # Constructor
    def __init__(self, cities, points):
        self.city_1 = cities[0]
        self.city_2 = cities[1]
        self.points = points
        self.completed = False

    # Getters
    def get_points(self):
        return self.points
    
    def get_city_1(self):
        return self.city_1
    
    def get_city_2(self):
        return self.city_2

    def get_completed(self):
        return self.completed

    # To string
    def __str__(self):
        return f"{self.city_1} to {self.city_2}: {self.points}"


class TrainCard:
    # Constructor
    def __init__(self, color):
        self.color = color

    # Getter
    def get_color(self):
        return self.color

    # To string 
    def __str__(self):
        return f"{self.color}"
    
    def __eq__(self, other):
            # It's good practice to first check if 'other' is an instance of the same class
            if not isinstance(other, TrainCard):
                return NotImplemented  # Or raise TypeError("Can only compare with MyClass instances")

            # Define the equality logic based on the attributes
            return self.color == other.color