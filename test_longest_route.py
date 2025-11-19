def longest_route(player1, player2, player3, player4):
    """Return the player with the longest continuous route."""

    def dfs(city, visited, current_length, current_path, routes_dict):
        """Depth-first search exploring all paths from the starting city."""
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

        visited.remove(city) # remove in case the city is also in other routes
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