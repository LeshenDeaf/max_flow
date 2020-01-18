import numpy as np


def algorithm(u):  # Dijkstra algorithm
    weights = [999] * n  # weights list
    weights[u] = 0
    parents = [-1] * n  # parents list
    for k in range(n):  # launch algorithm n times so that is works correctly
        for i in range(n):
            for j in range(n):
                if weights[i] + a[i][j] < weights[j] and a[i][j]:
                    weights[j] = weights[i] + a[i][j]
                    parents[j] = i
    if weights[t] == 999:  # if stock is not visited return False
        return False
    path = []  # list with path
    parent = t
    while parent != -1:
        path.append(parent)
        parent = parents[parent]
    return list(reversed(path))  # return path


def find(u, v):  # function finds an edge from verticle u to v and returns it
    for e in edges:
        if u == e[0] - 1 and v == e[1] - 1:
            return e
    return 'There is no such an edge'  # if edge is not found


def flow(path):
    minimal = []  # bandwidth of edges (max flow - current flow) 
    flow_edges = []  # edges of the path
    for i in range(len(path)-1):
        edge = find(path[i], path[i+1])
        edge_opposite = find(path[i+1], path[i])
        flow_edges.append([edge, edge_opposite])
        minimal.append(edge[3] - edge[2])
    try:
        cmin = min(minimal)  # minimal flow bandwidth
        for edge in flow_edges:
            edge[0][2] += cmin  # increasin flow of the edge by cmin
            edge[1][2] -= cmin  # decreasin flow of the opposite one
            if edge[0][2] == edge[0][3]:  # bandwidth = 0
                a[edge[0][0]-1][edge[0][1]-1] = False
    except ValueError:  # if edge does not exist
        return False


with open('test.txt') as f: # reading data from file
    read_l = f.readline().split(' ')
    n = int(read_l[0])  # no of verticles
    m = int(read_l[1])  # кno of edges
    s = int(read_l[2]) - 1  # a source
    t = int(read_l[3]) - 1  # stock
    a = np.zeros((n, n), dtype=bool)  # adjacency matrix
    l = m * 2
    edges = [None] * l
    for i in range(m):
        read_l = f.readline().split(' ')
        edges[i] = list()
        edges[m+i] = list()
        for el in read_l:
            edges[i].append(int(el))
            edges[m+i].append(int(el))
        edges[m + i][0], edges[m+i][1] = edges[m+i][1], edges[m+i][0]
        edges[m+i][3] = 0  # opposite edges maxflow = 0

        a[int(read_l[0]) - 1][int(read_l[1]) - 1] = True
        a[int(read_l[1]) - 1][int(read_l[0]) - 1] = True
    edges = sorted(edges, key=lambda x: x[0])  # sorting edges list for conveniene


for row in a:  # printing adjacency matrix
    for el in row:
        print(int(el), end=',')
    print()

while algorithm(s):  # searching for the max flow while stock is acceccable
    flow(algorithm(s))

print('Maximal flow graph:')  # printing edges of graph with max flow to user
max = 0
for edge in edges:
    if edge[2] >= 0 and edge[3]:
        print(edge)
for edge in edges:
    if edge[1] == t + 1 and edge[3]:
        max += edge[2]
print('Max flow is:', max)  # printing max flow
