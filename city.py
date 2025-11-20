"""
City class:
- Name
- Sprite (not yet?)
"""


class City:
    """Class for city nodes"""
    def __init__(self, name):
        self.name = name

    def set_name(self, name):
        """Set the name"""
        self.name = name

    def get_name(self):
        """Returns the city name"""
        return self.name
