graph = {'A': ['B', 'C'],
         'B': ['C', 'D','E'],
         'C': ['D'],
         'D': [],
         'E': ['F'],
         'F': []}





def find_all_paths(graph, start, path=[]):
    path = path + [start]
    # if start == end:
    #     return [path]
    if graph[start] == []:
        return [path]
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


print(find_all_paths(graph, 'A'))
