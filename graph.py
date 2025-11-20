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
        paths = []
        for path in self.paths:
            if city1 in path.get_cities() and city2 in path.get_cities():
                paths.append(path)
        return paths
    
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
            if route != None:
                cities = route.get_cities()
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

    def longest_route(self, player1, player2, player3, player4):
        """Return the player with the longest continuous route."""

        def dfs(city, visited, current_length, current_path, routes_dict):
            """Depth first search exploring all paths from the starting city."""
            visited.add(city)

            max_length = current_length
            best_path = current_path.copy()

            # Explore neighbors
            for neighbor, weight in routes_dict.get(city, {}).items():
                if neighbor not in visited:
                    length, path = dfs(
                        neighbor,
                        visited,
                        current_length + weight,
                        current_path + [neighbor],
                        routes_dict
                    )
                    if length > max_length:
                        max_length = length
                        best_path = path

            visited.remove(city)  # remove in case the city is also in other routes
            return max_length, best_path

        players = [player1, player2, player3, player4]
        results = []

        for player in players:
            player_map = player.get_map()
            routes_dict = {}

            # Convert player's claimed routes to a dictionary
            for route in player_map.get_paths():
                if route:
                    city1, city2 = route.get_cities()
                    weight = route.get_weight()

                    # Symmetry
                    if city1 not in routes_dict:
                        routes_dict[city1] = {}
                    routes_dict[city1][city2] = weight

                    if city2 not in routes_dict:
                        routes_dict[city2] = {}
                    routes_dict[city2][city1] = weight

            overall_max = 0
            best_path = []

            # If player has at least one route, run DFS
            if routes_dict:
                for start_city in routes_dict:
                    length, path = dfs(start_city, set(), 0, [start_city], routes_dict)
                    if length > overall_max:
                        overall_max = length
                        best_path = path

            results.append((player, overall_max, best_path))

        # Return only the winning player
        winner = max(results, key=lambda x: x[1])
        return winner[0]

    # To string
    def __str__(self):
        s = "Routes:\n"
        for path in self.paths:
            s += str(path) + '\n'
        return f"{s}"