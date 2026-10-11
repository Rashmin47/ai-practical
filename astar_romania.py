import heapq

# ---------------------------------------------------------
# Graph representation of the Romania map (adjacency list)
# Same state space used in Practicals 3, 4 and 5
# ---------------------------------------------------------
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

# Straight-line distance heuristic to Bucharest (h(n))
heuristic = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Dobreta': 242,
    'Eforie': 161, 'Fagaras': 178, 'Giurgiu': 77, 'Hirsova': 151,
    'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
    'Oradea': 380, 'Pitesti': 98, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199,
    'Zerind': 374,
}

def astar(graph, h, start, goal):
    counter = 0
    # Frontier entries are (f(n), g(n), tie_breaker, city, path)
    frontier = [(h[start], 0, counter, start, [start])]
    best_g = {start: 0}
    expansion_order = []

    while frontier:
        f, g, _, current, path = heapq.heappop(frontier)
        if g != best_g.get(current):
            continue
        expansion_order.append(current)

        if current == goal:
            return path, g, expansion_order

        for neighbour, weight in graph.get(current, []):
            new_g = g + weight
            if new_g < best_g.get(neighbour, float('inf')):
                best_g[neighbour] = new_g
                counter += 1
                new_f = new_g + h[neighbour]
                heapq.heappush(frontier,
                               (new_f, new_g, counter,
                                neighbour, path + [neighbour]))

    return None, None, expansion_order

if __name__ == "__main__":
    start_city = "Arad"
    goal_city = "Bucharest"
    path, total_cost, order = astar(romania_map, heuristic,
                                    start_city, goal_city)

    print("=" * 55)
    print(f" A* SEARCH: {start_city} -> {goal_city}")
    print("=" * 55)

    if path:
        print(f"\nPath found : {' -> '.join(path)}")
        print(f"Number of edges (path length) : {len(path) - 1}")
        print(f"Total real path cost (sum of edge weights) : {total_cost} km")
    else:
        print("No path found.")

    print(f"\nOrder of node expansion (nodes popped from the priority queue):\n{order}")
