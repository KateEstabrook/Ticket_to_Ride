"""
Route class:
- City1 Name
- City2 Name
- Color (of weight, could be colorless)
- Weight (num)
"""
class Route:
        def __init__(self, route_info):
            self.cities = (route_info[0], route_info[1])
            self.weight = route_info[2]
            self.color = route_info[3]

        def get_cities (self):
            return self.cities
        
        def get_weight (self):
            return self.weight
        
        def get_color (self):
            return self.color