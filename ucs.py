import heapq

def get_path(search_tree,goal):
    path=list()
    while True:
        if search_tree[goal]==None:
            path.append(goal)
            break
        path.append(goal)
        goal=search_tree[goal][1]
    path.reverse()
    return path

def update_cost(open,successor,gn,parent,search_tree):
    for i in range(len(open)):
        if open[i][1]==successor:
            if open[i][0]>gn:
                open.pop(i)
                heapq.heapify(open)
                heapq.heappush(open, (gn, successor))
                search_tree[successor]=(gn,parent)
                break


def expand(node,open,closed,search_tree,graph):
    successors = list(graph[node[1]])
    for (edge_cost,successor) in successors:
        gn = node[0] + edge_cost
        if successor not in closed and successor not in search_tree:
            heapq.heappush(open,(gn,successor))
            search_tree[successor] = (gn, node[1])
        elif successor in search_tree:
            update_cost(open,successor,gn,node[1],search_tree)
        elif successor in closed and gn<closed[successor]:
            heapq.heappush(open,(gn,successor))
            search_tree[successor]=(gn,node[1])
            closed.pop(successor)
    

def ucs(graph,start,goals):
    open = list()
    closed = dict()
    search_tree = dict()
    open.append(start)
    search_tree[start[1]] = None
    
    

    heapq.heapify(open)
    while True:
        if len(open) == 0:
            return "failed"
        node = heapq.heappop(open)
        
        closed[node[1]] = node[0]
        if node[1] in goals:
            return search_tree,node[1]
        expand(node, open, closed, search_tree, graph)




graph={
    'S':[(2,'A'),(3,'B'),(5,'D')],
    'A':[(4,'C')],
    'B':[(4,'D')],
    'C':[(1,'D'),(2,'G')],
    'D':[(5,'G')]
}
start=(0,'S')
goals=set()
goals.add('G')
search_tree,goal=ucs(graph,start,goals)
solution=get_path(search_tree,goal)

print("Solution is ", solution)
print("Solution cos =",search_tree[goal][0])

# graph={
#     'S':[(1,'A'),(5,'B'),(15,'C')],
#     'C':[(5,'G')],
#     'B':[(5,'G')],
#     'A':[(10,'G')]
# }
# start=(0,'S')
# goals=set()
# goals.add('G')
# search_tree,goal=ucs(graph,start,goals)
# solution=get_path(search_tree,goal)

# print("Solution is ", solution)
# print("Solution cos =",search_tree[goal][0])
