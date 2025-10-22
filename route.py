"""
Route class:
- City1 Name
- City2 Name
- Color (of weight, could be colorless)
- Weight (num)
"""
class Route:
        # Constructor
        def __init__(self, route_info):
            self.cities = (route_info[0], route_info[1])
            self.weight = route_info[2]
            self.color = route_info[3]

        # Getters
        def get_cities (self):
            return self.cities
        
        def get_weight (self):
            return self.weight
        
        def get_color (self):
            return self.color
        
        # To string
        def __str__(self):
            return f"{self.cities[0]} to {self.cities[1]}: {self.weight} {self.color}(s)"