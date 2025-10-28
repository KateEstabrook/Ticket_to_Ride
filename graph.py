"""
Graph class:
- List of Nodes (cities)
- List of paths (routes)
"""

import route

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

    # To string
    def __str__(self):
        s = "Routes:\n"
        for path in self.paths:
            s += str(path) + '\n'
        return f"{s}"
