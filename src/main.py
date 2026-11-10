"""Запуск анализа зависимостей."""

from src.config import read_config
from src.graph import build_graph, graph_edges
from src.maven import get_dependencies
from src.test_repo import read_test_repo


def make_provider(args):
    """Создать функцию получения зависимостей."""
    if args.test:
        repository = read_test_repo(args.repo)
        if args.package not in repository:
            raise ValueError("Пакет отсутствует в тестовом файле")
        return lambda package: repository.get(package, [])

    def get_children(package):
        """Получить зависимости Maven-пакета."""
        if "@" not in package:
            name, version = package, args.version
        else:
            name, version = package.rsplit("@", 1)

        result = get_dependencies(args.repo, name, version)
        return [
            f"{name}@{version}" for name, version in result
        ]

    return get_children


def main():
    """Построить и вывести граф зависимостей."""
    args = read_config()

    try:
        provider = make_provider(args)
        graph = build_graph(args.package, provider)
    except (ValueError, OSError) as error:
        print("Ошибка:", error)
        return

    print("Граф зависимостей:")
    for package in graph:
        print(package, "->", ", ".join(graph[package]) or "нет")

    print("Количество вершин:", len(graph))
    print("Количество рёбер:", len(graph_edges(graph)))


if __name__ == "__main__":
    main()
