"""
Practical 5: Uniform Cost Search (UCS) for Romania Map Problem
Finds the least-cost path from Arad to Bucharest using UCS traversal.
"""

import heapq

# ---------------------------------------------------------
# Graph representation of the Romania map (adjacency list)
# Same state space used in Practicals 3 (BFS) and 4 (DFS)
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


def ucs(graph, start, goal):
    """
    Perform Uniform Cost Search on 'graph' from 'start' to 'goal'.

    Uses a min-priority queue (implemented with heapq) as the frontier,
    ordered by cumulative path cost g(n) - the defining property that
    distinguishes UCS from BFS/DFS, which ignore edge weights entirely.
    The goal test is applied on EXPANSION (when popped), not on
    generation, which guarantees the first time the goal is popped its
    cost is optimal.

    Returns:
        path (list): least-cost sequence of cities from start to goal
        total_cost (int): the cumulative cost of that path
        expansion_order (list): order in which nodes were popped/expanded
    """
    counter = 0                                   # tie-breaker so heapq never compares lists
    frontier = [(0, counter, [start])]            # (cumulative_cost, tie_breaker, path)
    best_cost = {start: 0}                        # cheapest cost found so far to reach a node
    expansion_order = []

    while frontier:
        cost, _, path = heapq.heappop(frontier)    # pop the cheapest path so far
        current = path[-1]
        expansion_order.append(current)

        if current == goal:
            return path, cost, expansion_order      # optimal: first pop of goal = least cost

        for neighbour, weight in graph.get(current, []):
            new_cost = cost + weight
            # relax: only continue if this is a cheaper route to 'neighbour'
            if neighbour not in best_cost or new_cost < best_cost[neighbour]:
                best_cost[neighbour] = new_cost
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, path + [neighbour]))

    return None, None, expansion_order   # no path found


if __name__ == "__main__":
    start_city = "Arad"
    goal_city = "Bucharest"

    path, total_cost, order = ucs(romania_map, start_city, goal_city)

    print("=" * 55)
    print(f" UCS SEARCH: {start_city} -> {goal_city}")
    print("=" * 55)

    if path:
        print(f"\nPath found : {' -> '.join(path)}")
        print(f"Number of edges (path length) : {len(path) - 1}")
        print(f"Total real path cost (sum of edge weights) : {total_cost} km")
    else:
        print("No path found.")

    print(f"\nOrder of node expansion (nodes popped from the priority queue):\n{order}")
