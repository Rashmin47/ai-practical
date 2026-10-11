from collections import deque
 
romania_map = {
    'Arad':      [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind':    [('Arad', 75), ('Oradea', 71)],
    'Oradea':    [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu':     [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj':     [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia':   [('Lugoj', 70), ('Dobreta', 75)],
    'Dobreta':   [('Mehadia', 75), ('Craiova', 120)],
    'Craiova':   [('Dobreta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras':   [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti':   [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu':   [('Bucharest', 90)],
    'Urziceni':  [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova':   [('Urziceni', 98), ('Eforie', 86)],
    'Eforie':    [('Hirsova', 86)],
    'Vaslui':    [('Urziceni', 142), ('Iasi', 92)],
    'Iasi':      [('Vaslui', 92), ('Neamt', 87)],
    'Neamt':     [('Iasi', 87)],
}
 
def dfs(graph, start, goal):
    # Stack for DFS: stores paths
    frontier = [[start]]
    visited = set()
    visited_order = []
 
    while frontier:
        path = frontier.pop()  # LIFO
        current = path[-1]
 
        if current not in visited:
            visited.add(current)
            visited_order.append(current)
 
            if current == goal:
                return path, visited_order
 
            # Get neighbors and reverse them before adding to stack to maintain 
            # expansion order same as the list order (Zerind first, then Sibiu, then Timisoara)
            # If we push Zerind, then Sibiu, then Timisoara, Timisoara will be popped first.
            # To expand Zerind first, we push in reverse order.
            neighbors = graph.get(current, [])
            for neighbour, _weight in reversed(neighbors):
                if neighbour not in visited:
                    new_path = path + [neighbour]
                    frontier.append(new_path)
 
    return None, visited_order
 
def path_cost(graph, path):
    total = 0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        for neighbour, weight in graph[a]:
            if neighbour == b:
                total += weight
                break
    return total
 
if __name__ == "__main__":
    start_city = "Arad"
    goal_city = "Bucharest"
 
    path, order = dfs(romania_map, start_city, goal_city)
 
    print("=" * 55)
    print(f" DFS SEARCH: {start_city} -> {goal_city}")
    print("=" * 55)
 
    if path:
        print(f"\nPath found : {' -> '.join(path)}")
        print(f"Number of edges (path length) : {len(path) - 1}")
        print(f"Total real path cost (sum of edge weights) : {path_cost(romania_map, path)} km")
    else:
        print("No path found.")
 
    print(f"\nOrder of node expansion (visited order):\n{order}")

