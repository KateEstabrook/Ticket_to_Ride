"""
Route class:
- City1 Name
- City2 Name
- Color (of weight, could be colorless)
- Weight (num)
"""
class Route:
        def __init__(self, cities, weight, color):
            self.cities = cities
            self.weight = weight
            self.color = color

        def get_cities (self):
            return self.cities
        
        def get_weight (self):
            return self.weight
        
        def get_color (self):
            return self.color