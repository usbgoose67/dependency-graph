"""Построение графа зависимостей алгоритмом DFS."""


def build_graph(start, get_children):
    """Обойти зависимости без рекурсии."""
    graph = {}
    visited = set()
    stack = [start]

    while stack:
        package = stack.pop()
        if package in visited:
            continue

        visited.add(package)
        children = list(get_children(package))
        graph[package] = children

        for child in reversed(children):
            if child not in visited:
                stack.append(child)

    return graph


def graph_edges(graph):
    """Получить все рёбра графа."""
    edges = set()
    for package, children in graph.items():
        for child in children:
            edges.add((package, child))
    return edges
