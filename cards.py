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
    """Class for destination cards"""
    def __init__(self, card_info):
        self.city_1 = card_info[0]
        self.city_2 = card_info[1]
        self.points = card_info[2]
        self.completed = False
        self.sprite = f"images/Dest_cards/{card_info[0].replace(' ', '')}" \
            f"_{card_info[1].replace(' ', '')}.png"

    def complete(self):
        """Complete destination card"""
        self.completed = True

    # Getters
    def get_points(self):
        """Gets the points of destination card"""
        return self.points

    def get_city_1(self):
        """Gets the name of the first city"""
        return self.city_1

    def get_city_2(self):
        """Gets the name of the second city"""
        return self.city_2

    def get_completed(self):
        """Gets the completed destination card"""
        return self.completed

    def get_sprite(self):
        """Gets the sprite of destination card"""
        return self.sprite

    # To string
    def __str__(self):
        """To string"""
        return f"{self.city_1} to {self.city_2}: {self.points}, Completed: {self.completed}"

    def __eq__(self, other):
        # It's good practice to first check if 'other' is an instance of the same class
        if not isinstance(other, DestinationCard):
            return NotImplemented  # Or raise TypeError("Can only compare with MyClass instances")

        # Define the equality logic based on the attributes
        return self.city_1 == other.city_1 and self.city_2 == other.city_2


class TrainCard:
    """Class for train cards"""
    def __init__(self, color):
        self.color = color
        self.sprite = f"images/{color}.png"

    # Getter
    def get_color(self):
        """Gets the color of train card"""
        return self.color

    def get_sprite(self):
        """Gets the sprite of train card"""
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
