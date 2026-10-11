class Node:
    def __init__(self, name, children=None, value=None):
        self.name = name
        self.children = children or []
        self.value = value

# The game tree exactly follows the supplied diagram.
# Root is MAX; the next level is MIN; the next level is MAX.
game_tree = Node('Root MAX', [
    Node('MIN 1', [Node('MAX 1', [Node('6', value=6), Node('4', value=4)])]),
    Node('MIN 2', [
        Node('MAX 2.1', [Node('3', value=3), Node('5', value=5)]),
        Node('MAX 2.2', [Node('2', value=2), Node('6', value=6)]),
        Node('MAX 2.3', [Node('9', value=9)])
    ]),
    Node('MIN 3', [
        Node('MAX 3.1', [Node('1', value=1)]),
        Node('MAX 3.2', [Node('1', value=1)])
    ]),
    Node('MIN 4', [
        Node('MAX 4.1', [Node('2', value=2), Node('1', value=1)]),
        Node('MAX 4.2', [Node('10', value=10), Node('8', value=8), Node('20', value=20)])
    ])
])

def minimax(node, maximizing, values):
    if not node.children:
        values[node.name] = node.value
        return node.value

    child_values = [minimax(child, not maximizing, values)
                    for child in node.children]
    node_value = max(child_values) if maximizing else min(child_values)
    values[node.name] = node_value
    return node_value

if __name__ == '__main__':
    values = {}
    result = minimax(game_tree, True, values)

    print('=' * 55)
    print(' MINIMAX GAME TREE EVALUATION')
    print('=' * 55)
    print('\nValues of MIN nodes:')
    for name in ['MIN 1', 'MIN 2', 'MIN 3', 'MIN 4']:
        print(f'{name} = {values[name]}')
    print('\nValue of root MAX node:')
    print(f'Root MAX = {result}')
    print('\nTherefore, the maximum value that the MAX node can get is', result)
