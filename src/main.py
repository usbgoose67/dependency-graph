"""Главный модуль анализатора зависимостей."""

import sys

from src.config import read_config
from src.graph import (
    build_graph,
    find_reverse_dependencies,
    graph_edges,
)
from src.maven import get_dependencies
from src.test_repo import read_test_repo
from src.visualize import (
    ascii_tree,
    make_plantuml,
    save_svg,
)


def make_provider(args):
    """Создать источник зависимостей."""
    if args.test:
        repository = read_test_repo(args.repo)

        if args.package not in repository:
            raise ValueError(
                "Пакет отсутствует в тестовом репозитории"
            )

        return lambda name: repository.get(name, [])

    def get_children(package):
        """Получить зависимости Maven-пакета."""
        if "@" in package:
            name, version = package.rsplit("@", 1)
        else:
            name, version = package, args.version

        dependencies = get_dependencies(
            args.repo,
            name,
            version,
        )

        return [
            f"{name}@{version}"
            for name, version in dependencies
        ]

    return get_children


def analyze(args):
    """Построить и вывести граф зависимостей."""
    if args.reverse and args.test:
        repository = read_test_repo(args.repo)
        result = find_reverse_dependencies(
            repository,
            args.package,
        )

        print("Обратные зависимости:")

        for name in sorted(result):
            print("-", name)

        return

    provider = make_provider(args)
    graph = build_graph(args.package, provider)

    if args.reverse:
        result = find_reverse_dependencies(
            graph,
            args.package,
        )
        print("Обратные зависимости:", sorted(result))
        return

    print("Количество вершин:", len(graph))
    print("Количество рёбер:", len(graph_edges(graph)))

    if args.ascii:
        print("\nASCII-дерево:")
        print(ascii_tree(graph, args.package))

    print("\nPlantUML:")
    print(make_plantuml(graph))

    filename = save_svg(graph, args.output)
    print("SVG сохранён:", filename)


def main():
    """Запустить приложение."""
    args = read_config()

    try:
        analyze(args)
    except (ValueError, OSError) as error:
        print("Ошибка:", error, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()