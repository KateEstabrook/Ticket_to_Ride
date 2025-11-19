"""
Testing for longest continuous route calculations
"""

def longest_route(routes):
    """This function takes in four dictionaries of routes and returns
    the player that has the longest route.
    """
    def dfs(city, visited, current_length, current_path):
        """This is a depth first search algorithm that will find the longest
        path from a starting node
        """
        visited.add(city)

        max_length = current_length
        best_path = current_path.copy()

        # Explore neighbors
        for neighbor, weight in routes.get(city, {}).items():
            if neighbor not in visited:
                # Recursively search
                length, path = dfs(neighbor, visited, current_length + weight,
                                   current_path + [neighbor])
                if length > max_length:
                    max_length = length
                    best_path = path

        visited.remove(city)
        return max_length, best_path

    # Try DFS from every city as starting point
    overall_max = 0
    best_overall_path = []

    for start in routes.keys():
        length, path = dfs(start, set(), 0, [start])
        if length > overall_max:
            overall_max = length
            best_overall_path = path

    return overall_max, best_overall_path




# For each player's claimed routes
player1_routes = {
    "Seattle": {"Portland": 1, "Helena": 6},
    "Portland": {"Seattle": 1, "San Francisco": 5},
    "San Francisco": {"Portland": 5},
    "Helena": {"Seattle": 6, "Denver": 4}
}

player2_routes = {
    "Seattle": {"Portland": 1, "Helena": 6},
    "Portland": {"Seattle": 1, "San Francisco": 5},
    "San Francisco": {"Portland": 5},
}

longest_length1, longest_path1 = longest_route(player1_routes)
print(f"Longest continuous route: {longest_length1}")
print(f"Path: {' -> '.join(longest_path1)}")


longest_length2, longest_path2 = longest_route(player2_routes)
print(f"Longest continuous route: {longest_length2}")
print(f"Path: {' -> '.join(longest_path2)}")
