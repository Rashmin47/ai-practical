COLORS = ['Red', 'Green', 'Blue']

# Australia map CSP: neighboring regions are constraints.
adjacency = {
    'WA':  ['NT', 'SA'],
    'NT':  ['WA', 'SA', 'QLD'],
    'SA':  ['WA', 'NT', 'QLD', 'NSW', 'VIC'],
    'QLD': ['NT', 'SA', 'NSW'],
    'NSW': ['QLD', 'SA', 'VIC'],
    'VIC': ['SA', 'NSW'],
    'TAS': [],                 # island; no land neighbour in this model
}

variables = ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS']

def is_consistent(region, color, assignment):
    return all(assignment.get(neighbour) != color
               for neighbour in adjacency[region])

def backtrack(assignment):
    if len(assignment) == len(variables):
        return assignment.copy()

    # Choose the next unassigned region in the fixed map order.
    region = next(r for r in variables if r not in assignment)
    for color in COLORS:
        if is_consistent(region, color, assignment):
            assignment[region] = color
            result = backtrack(assignment)
            if result is not None:
                return result
            del assignment[region]
    return None

def verify_solution(assignment):
    return all(assignment[a] != assignment[b]
               for a, neighbours in adjacency.items()
               for b in neighbours)

if __name__ == '__main__':
    solution = backtrack({})
    print('=' * 55)
    print(' CSP AUSTRALIA MAP COLORING')
    print('=' * 55)
    print('\nAllowed colors : Red, Green, Blue')
    print('Color assignment:')
    for region in variables:
        print(f'{region} = {solution[region]}')
    print(f'\nAll constraints satisfied : {verify_solution(solution)}')
