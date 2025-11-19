"""
Graph class:
- List of Nodes (cities)
- List of paths (routes)
"""

import route
import constants as c
import heapq

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
    
    def get_path_by_cities(self, city1, city2):
        for path in self.paths:
            if city1 in path.get_cities() and city2 in path.get_cities():
                return path
    
    # Setters
    def set_path(self, paths):
        self.paths = paths

    def set_nodes(self, nodes):
        self.nodes = nodes

    def add_node(self, city):
        self.nodes.append(city)

    def add_path(self, path):
        self.paths.append(path)

    def has_path(self, city1, city2):
        for path in self.paths:
            if city1 in path.get_cities() and city2 in path.get_cities():
                return True
        return False
    
    def get_nodes(self):
        return self.nodes
    
    def get_paths(self):
        return self.paths
    
    def get_path_reqs(self, city1, city2):
        for path in self.paths:
            if city1 in path.get_cities() and city2 in path.get_cities():
                return path.get_weight(), path.get_color()

    def add_route(self, route):
        self.paths.append(route)
    
    def remove_route(self, city1, city2):
        for route in self.paths:
            if city1 in route.get_cities() and city2 in route.get_cities():
                self.paths.remove(route)
                return route
        
    # This is used by all players to check if they have completed a destination card
    def check_completed(self, dest_card):
        """"Check if a graph contains the routes required to complete a dest card"""
        if dest_card == None:
            return False
        adj = {}

        for route in self.paths: # add self paths with weight 0
            cities = route.get_nodes()
            if cities[0] not in adj:
                adj[cities[0]] = [(cities[1], 0)]
            else:
                adj[cities[0]].append((cities[1], 0))
            if cities[1] not in adj:
                adj[cities[1]] = [(cities[0], 0)]
            else:
                adj[cities[1]].append((cities[0], 0))

        src = dest_card.get_city_1()
        dist, route_lists = self.djikstra(src, adj)

        if dest_card.get_city_2() not in dist:
            return False
        if dist[dest_card.get_city_2()] >= 999:
            return False
        return True

    # pass in src, adjacency list
    def djikstra(self, src, adj):
        """Djikstra's algorithm to find shortest path from source to all other nodes in graph"""
        if src not in adj:
            return {}, {}
        # Creating priority queue for routes
        pq = []
        # create dict for all distances from src node
        dist = {}
        route_lists = {}

        for node in list(adj.keys()):
            dist[node] = 999
            route_lists[node] = []

        heapq.heappush(pq, [0, src])
        dist[src] = 0

        while pq:
            curr_city = heapq.heappop(pq)[1]



            # Get all adjacent of u.
            for adjacents in adj[curr_city]:
                # Get vertex label and weight of current
                # adjacent of u.
                city, weight = adjacents[0], adjacents[1]

                # If there is shorter path to v through u.
                if dist[city] > dist[curr_city] + weight:
                    # Updating distance of v
                    dist[city] = dist[curr_city] + weight
                    new_path = route_lists[curr_city].copy()
                    new_path.append(city)
                    route_lists[city] = new_path
                    heapq.heappush(pq, [dist[city], city])
        # Return the shortest distance array
        return dist, route_lists

    # To string
    def __str__(self):
        s = "Routes:\n"
        for path in self.paths:
            s += str(path) + '\n'
        return f"{s}"