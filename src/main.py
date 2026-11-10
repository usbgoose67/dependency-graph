"""Главный файл анализа зависимостей."""

from src.config import read_config
from src.graph import (
    build_graph,
    find_reverse_dependencies,
    graph_edges,
)
from src.maven import get_dependencies
from src.test_repo import read_test_repo


def make_provider(args):
    """Выбрать источник зависимостей."""
    if args.test:
        repository = read_test_repo(args.repo)
        if args.package not in repository:
            raise ValueError("Пакет отсутствует в тестовом файле")
        return lambda package: repository.get(package, [])

    def get_children(package):
        """Получить зависимости Maven."""
        if "@" in package:
            name, version = package.rsplit("@", 1)
        else:
            name, version = package, args.version

        result = get_dependencies(args.repo, name, version)
        return [
            f"{name}@{version}" for name, version in result
        ]

    return get_children


def main():
    """Выполнить прямой или обратный анализ."""
    args = read_config()

    try:
        provider = make_provider(args)
        if args.reverse and args.test:
            repository = read_test_repo(args.repo)
            dependencies = find_reverse_dependencies(
                repository, args.package
            )
            print("Обратные зависимости:", args.package)
            for package in dependencies:
                print("-", package)
            return

        graph = build_graph(args.package, provider)
        if args.reverse:
            dependencies = find_reverse_dependencies(
                graph, args.package
            )
            print("Обратные зависимости:", dependencies)
            return
    except (ValueError, OSError) as error:
        print("Ошибка:", error)
        return

    print("Граф зависимостей:")
    for package, children in graph.items():
        print(package, "->", ", ".join(children) or "нет")

    print("Количество вершин:", len(graph))
    print("Количество рёбер:", len(graph_edges(graph)))


if __name__ == "__main__":
    main()
