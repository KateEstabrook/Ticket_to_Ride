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
    def __init__(self, card_info):
        self.city_1 = card_info[0]
        self.city_2 = card_info[1]
        self.points = card_info[2]
        self.completed = False
        self.sprite = f"images/{card_info[0].replace(" ", "")}_{card_info[1].replace(" ", "")}.png"

    # Getters
    def get_points(self):
        return self.points

    def get_city_1(self):
        return self.city_1

    def get_city_2(self):
        return self.city_2

    def get_completed(self):
        return self.completed
    
    def get_sprite(self):
        return self.sprite

    # To string
    def __str__(self):
        return f"{self.city_1} to {self.city_2}: {self.points}"


class TrainCard:
    # Constructor
    def __init__(self, color):
        self.color = color
        self.sprite = f"images/{color}.png"

    # Getter
    def get_color(self):
        return self.color

    def get_sprite(self):
        return self.sprite

    # To string
    def __str__(self):
        return f"{self.color}"

    def __eq__(self, other):
        # It's good practice to first check if 'other' is an instance of the same class
        if not isinstance(other, TrainCard):
            return NotImplemented  # Or raise TypeError("Can only compare with MyClass instances")

        # Define the equality logic based on the attributes
        return self.color == other.color
