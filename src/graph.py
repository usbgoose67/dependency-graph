"""Построение и обработка графа зависимостей."""


def build_graph(start, get_children):
    """Обойти зависимости алгоритмом DFS без рекурсии."""
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
    """Получить множество рёбер графа."""
    edges = set()
    for package, children in graph.items():
        for child in children:
            edges.add((package, child))
    return edges


def reverse_graph(graph):
    """Поменять направления всех рёбер."""
    result = {package: [] for package in graph}

    for package, children in graph.items():
        for child in children:
            result.setdefault(child, [])
            result[child].append(package)

    return result


def find_reverse_dependencies(graph, package):
    """Найти все обратные зависимости через DFS."""
    if package not in graph:
        raise ValueError("Пакет отсутствует в графе")

    reversed_data = reverse_graph(graph)
    result = build_graph(
        package, lambda name: reversed_data[name]
    )
    result.pop(package, None)
    return list(result)
