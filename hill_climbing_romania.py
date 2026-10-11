# Graph representation of the Romania road map
romania_map = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Dobreta', 75)],
    'Dobreta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Dobreta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)],
}

# Straight-line heuristic values shown in the supplied diagram
heuristic = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Dobreta': 242,
    'Eforie': 161, 'Fagaras': 178, 'Giurgiu': 77, 'Hirsova': 151,
    'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
    'Oradea': 380, 'Pitesti': 98, 'Rimnicu Vilcea': 193,
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199,
    'Zerind': 374,
}

def path_cost(graph, path):
    total = 0
    for a, b in zip(path, path[1:]):
        for neighbour, distance in graph[a]:
            if neighbour == b:
                total += distance
                break
    return total

def hill_climbing(graph, h, start, goal):
    current = start
    path = [current]
    visited = {current}
    expansion_order = [current]
    decisions = []

    while current != goal:
        candidates = [(neighbour, h[neighbour])
                      for neighbour, _ in graph.get(current, [])
                      if neighbour not in visited]
        if not candidates:
            return None, expansion_order, decisions

        # Hill climbing considers only h(n), never road distance, when choosing.
        next_city, next_h = min(candidates, key=lambda item: item[1])
        decisions.append((current, next_city, h[current], next_h))
        if next_h >= h[current]:
            return None, expansion_order, decisions

        current = next_city
        path.append(current)
        visited.add(current)
        expansion_order.append(current)

    return path, expansion_order, decisions

if __name__ == '__main__':
    start_city = 'Arad'
    goal_city = 'Bucharest'
    path, order, decisions = hill_climbing(romania_map, heuristic, start_city, goal_city)

    print('=' * 55)
    print(f' HILL CLIMBING SEARCH: {start_city} -> {goal_city}')
    print('=' * 55)
    if path:
        print(f'\nPath found : {" -> ".join(path)}')
        print(f'Number of edges (path length) : {len(path) - 1}')
        print(f'Total real path cost (for comparison only) : {path_cost(romania_map, path)} km')
    else:
        print('\nNo path found (local maximum or dead end).')
    print(f'\nOrder of node selection:\n{order}')
    print(f'Heuristic decisions (current -> selected next, h values):\n{decisions}')
