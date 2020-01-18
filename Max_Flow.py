import numpy as np


def algorithm(u):  # Алгоритм Дейкстры
    weights = [999] * n  # список весов
    weights[u] = 0
    parents = [-1] * n  # список родителей
    for k in range(n):  # запускаем алгоритм n раз для корректной работы
        for i in range(n):
            for j in range(n):
                if weights[i] + a[i][j] < weights[j] and a[i][j]:
                    weights[j] = weights[i] + a[i][j]
                    parents[j] = i
    if weights[t] == 999:  # если не попали в сток, то возвращаем False
        return False
    path = []  # список, хранящий путь
    parent = t
    while parent != -1:
        path.append(parent)
        parent = parents[parent]
    return list(reversed(path))  # возвращаем путь


def find(u, v):  # фунция находит ребро из вершины u в вершину v и возвращает его
    for e in edges:
        if u == e[0] - 1 and v == e[1] - 1:
            return e
    return 'There is no such an edge'  # если не удалось найти такое ребро


def flow(path):
    minimal = []  # пропускные способности ребер
    flow_edges = []  # ребра пути
    for i in range(len(path)-1):
        edge = find(path[i], path[i+1])
        edge_opposite = find(path[i+1], path[i])
        flow_edges.append([edge, edge_opposite])
        minimal.append(edge[3] - edge[2])
    try:
        cmin = min(minimal)  # минимальная пропускная способность
        for edge in flow_edges:
            edge[0][2] += cmin  # увеличиваем поток ребра на cmin
            edge[1][2] -= cmin  # уменьшаем поток противоположного
            if edge[0][2] == edge[0][3]:  # пропускная способность = 0
                a[edge[0][0]-1][edge[0][1]-1] = False
    except ValueError:  # если ребра не существует
        return False


with open('test.txt') as f: # считывание данных из файла
    read_l = f.readline().split(' ')
    n = int(read_l[0])  # количество вершин
    m = int(read_l[1])  # количество ребер
    s = int(read_l[2]) - 1  # источник
    t = int(read_l[3]) - 1  # сток
    a = np.zeros((n, n), dtype=bool)  # матрица смежности
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
        edges[m+i][3] = 0  # у противоположных ребер максимальных поток = 0

        a[int(read_l[0]) - 1][int(read_l[1]) - 1] = True
        a[int(read_l[1]) - 1][int(read_l[0]) - 1] = True
    edges = sorted(edges, key=lambda x: x[0])  # сортируем список ребер для удобства


for row in a:  # печать матрицы смежности
    for el in row:
        print(int(el), end=',')
    print()

while algorithm(s):  # ищем максимальный поток, пока из источника можно попасть в сток
    flow(algorithm(s))

print('Maximal flow graph:')  # вывод пользователю ребер графа с максимальным потоком
max = 0
for edge in edges:
    if edge[2] >= 0 and edge[3]:
        print(edge)
for edge in edges:
    if edge[1] == t + 1 and edge[3]:
        max += edge[2]
print('Max flow is:', max)  # вывод максимального потока
