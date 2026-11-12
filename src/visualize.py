"""Визуализация графа зависимостей."""

import subprocess
from pathlib import Path

from src.graph import graph_edges


def make_plantuml(graph):
    """Создать описание графа в формате PlantUML."""
    nodes = set(graph)
    for children in graph.values():
        nodes.update(children)

    names = {
        name: f"n{index}"
        for index, name in enumerate(sorted(nodes))
    }
    lines = ["@startuml", "left to right direction"]

    for name in sorted(nodes):
        label = name.replace('"', "'")
        lines.append(f'rectangle "{label}" as {names[name]}')

    for parent, child in sorted(graph_edges(graph)):
        lines.append(f"{names[parent]} --> {names[child]}")

    lines.append("@enduml")
    return "\n".join(lines) + "\n"


def run_plantuml(source):
    """Запустить PlantUML для создания SVG."""
    jar = Path("tools") / "plantuml.jar"
    if not jar.is_file():
        raise ValueError("Не найден tools/plantuml.jar")

    try:
        subprocess.run(
            ["java", "-jar", str(jar), "-tsvg", str(source)],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise ValueError(
            "Java не установлена или не найдена"
        ) from error
    except subprocess.CalledProcessError as error:
        raise ValueError(
            f"Ошибка PlantUML: {error.stderr}"
        ) from error


def save_svg(graph, filename):
    """Сохранить PlantUML и создать SVG."""
    if Path(filename).name != filename:
        raise ValueError("Укажи только имя SVG-файла")

    if not filename.lower().endswith(".svg"):
        raise ValueError("Имя файла должно оканчиваться на .svg")

    folder = Path("output")
    folder.mkdir(parents=True, exist_ok=True)

    target = folder / filename
    source = target.with_suffix(".puml")
    source.write_text(make_plantuml(graph), encoding="utf-8")

    run_plantuml(source)

    if not target.is_file():
        raise ValueError("PlantUML не создал SVG-файл")

    return target


def add_children(stack, graph, parent, prefix):
    """Добавить потомков в стек в обратном порядке."""
    children = graph.get(parent, [])

    for index in range(len(children) - 1, -1, -1):
        last = index == len(children) - 1
        stack.append((children[index], prefix, last))


def ascii_tree(graph, start):
    """Построить ASCII-дерево без рекурсии."""
    lines = [start]
    visited = {start}
    stack = []
    add_children(stack, graph, start, "")

    while stack:
        name, prefix, last = stack.pop()
        branch = "`-- " if last else "|-- "

        if name in visited:
            lines.append(prefix + branch + name + " (повтор)")
            continue

        lines.append(prefix + branch + name)
        visited.add(name)

        next_prefix = prefix + ("    " if last else "|   ")
        add_children(stack, graph, name, next_prefix)

    return "\n".join(lines)