"""
Route class:
- City1 Name
- City2 Name
- Color (of weight, could be colorless)
- Weight (num) 
"""
class Route:
        def __init__(self, city_1, city_2, weight, color):
            self.city_1 = city_1
            self.city_2 = city_2
            self.weight = weight
            self.color = color