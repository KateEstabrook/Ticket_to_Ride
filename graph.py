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
    
    def get_path_reqs(self, city1, city2):
        for path in self.paths:
            if city1 in path.get_cities() and city2 in path.get_cities():
                return path.get_weight(), path.get_color()

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
        for route in self.paths:
            if city1 in route.get_cities() and city2 in route.get_cities():
                self.paths.remove(route)
                return route
        
    def check_completed(self, dest_card):
        """"Check if a graph contains the routes required to complete a dest card"""
        if dest_card.get_city_1() in self.nodes and dest_card.get_city_2() in self.nodes:
            src = dest_card.get_city_1()
            dist, route_lists = self.djikstra(src)
            if dist[dest_card.get_city_2()] >= 999:
                return False
            return True
        else:
            return False

    def djikstra(self, src): # Should change to pass in the adjacency list instead of using c.ROUTES, create the adjacency list elsewhere
        """Djikstra's algorithm to find shortest path from source to all other nodes in graph"""
        # create an adjacency list with just city names (dictionairy of lists)
        adj = {}
        for city1 in c.ROUTES: # not ROUTE_LST
            if city1 in self.nodes:
                adj[city1] = []
                for city2 in c.ROUTES[city1]:
                    if city2 in self.nodes:
                        if self.has_path(city1, city2):
                            adj[city1].append((city2, c.ROUTES[city1][city2]))
        for route in self.paths: # add self paths with weight 0
            cities = route.get_cities()
            adj[cities[0]].append((cities[1], 0))
            adj[cities[1]].append((cities[0], 0))
        # Creating priority queue for routes
        pq = []
        # create dict for all distances from src node
        dist = {}
        route_lists = {}

        for node in self.nodes:
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

"""
def dijkstra(V, edges, src):
    # Create adjacency list
    adj = constructAdj(edges, V)

    # Create a priority queue to store vertices that
    # are being preprocessed.
    pq = []
    
    # Create a list for distances and initialize all
    # distances as infinite
    dist = [sys.maxsize] * V

    # Insert source itself in priority queue and initialize
    # its distance as 0.
    heapq.heappush(pq, [0, src])
    dist[src] = 0

    # Looping till priority queue becomes empty (or all
    # distances are not finalized) 
    while pq:
        # The first vertex in pair is the minimum distance
        # vertex, extract it from priority queue.
        u = heapq.heappop(pq)[1]

        # Get all adjacent of u.
        for x in adj[u]:
            # Get vertex label and weight of current
            # adjacent of u.
            v, weight = x[0], x[1]

            # If there is shorter path to v through u.
            if dist[v] > dist[u] + weight:
                # Updating distance of v
                dist[v] = dist[u] + weight
                heapq.heappush(pq, [dist[v], v])

    # Return the shortest distance array
    return dist
"""