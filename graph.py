"""
Graph class:
- List of Nodes (cities)
- List of paths (routes)
"""

import route
import constants as c

class Graph:
    # Constructor
    def __init__(self, city_list, route_list):
        self.nodes = city_list
        self.paths = []
        for path in route_list:
            self.paths.append(route.Route(path))

    # Getters
    def get_nodes(self):
        return self.nodes

    def get_paths(self):
        return self.paths
    
    # Setters
    def set_path(self, paths):
        self.paths = paths

    def set_nodes(self, nodes):
        self.nodes = nodes

    def add_route(self, city1, city2):
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)
        for route in c.ROUTES_LST:
            if tuple(route[:2]) == city_pair or tuple(route[:2]) == reverse_pair:
                self.paths.append(route)
                break
        else:
            print("lol you added a path")
    
    def remove_route(self, city1, city2):
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)
        for route in self.paths:
            if tuple(route[:2]) == city_pair or tuple(route[:2]) == reverse_pair:
                return self.paths.remove(route)
        else:
            print("lol you removed a path")
            return None

    # To string
    def __str__(self):
        s = "Routes:\n"
        for path in self.paths:
            s += str(path) + '\n'
        return f"{s}"
