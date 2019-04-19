import collections
n, m = list(map(int, input().split()))

input_roads = [list(map(int, input().split())) for i in range(m)]
sorted_roads = sorted(input_roads)

old_graph = {}
for i in range(1, n+1):
    graph_new = []
    for j, v in sorted_roads:
        if j == i:
            graph_new.append((j, v))
    old_graph.update({i: graph_new})
            
def connected_components(neighbors): 
    seen = set() 
    def component(node): 
            nodes = set([node]) 
            while nodes: 
                node = nodes.pop() 
                seen.add(node) 
                nodes |= neighbors[node] - seen 
                yield node 
    for node in neighbors: 
        if node not in seen: 
            yield component(node) 

            
new_graph = {node: set(each for edge in edges for each in edge) 
      for node, edges in old_graph.items()} 
components = [] 
for component in connected_components(new_graph): 
    c = set(component) 
    components.append([edge for edges in old_graph.values() 
          for edge in edges 
          if c.intersection(edge)]) 

if len(components) > 1:
    print('YES')

elif m > 3:
    graph_list= []
    for i in old_graph.values():
        for j, v in i:
            graph_list.append(j)
            graph_list.append(v)

    deg = collections.Counter(graph_list)

    cnt = 0
    for i in deg.values():
        if i <= 2:
            cnt += 1
    if cnt == n:
        print('YES')
    else:
        print('NO')
else:
    print('NO')
