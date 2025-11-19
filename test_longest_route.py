def longest_route(routes):
    def dfs(city, visited):
        # Mark city as visited
        visited.add(city)

        max_length = 0  # maximum length starting from this city

        # Explore neighbors
        for neighbor, weight in routes.get(city, {}).items():
            if neighbor not in visited:
                # Recursively search, updating the path length
                length = weight + dfs(neighbor, visited)
                max_length = max(max_length, length)

        # Backtrack
        visited.remove(city)
        return max_length

    # Try DFS from every city
    overall_max = 0
    for start in routes.keys():
        overall_max = max(overall_max, dfs(start, set()))

    return overall_max


# look at each players map which shows the claimed routes
# look for the longest route with weights