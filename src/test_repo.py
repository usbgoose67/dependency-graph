"""Чтение тестового репозитория из TXT-файла."""

import re
from pathlib import Path


def read_test_repo(filename):
    """Прочитать граф из текстового файла."""
    graph = {}
    content = Path(filename).read_text(encoding="utf-8")

    for number, line in enumerate(content.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue

        if ":" not in line:
            raise ValueError(f"Ошибка строки {number}")

        name, values = line.split(":", 1)
        name = name.strip()
        dependencies = values.split()

        if not re.fullmatch(r"[A-Z]+", name):
            raise ValueError(f"Неверный пакет в строке {number}")

        for item in dependencies:
            if not re.fullmatch(r"[A-Z]+", item):
                raise ValueError(
                    f"Неверная зависимость в строке {number}"
                )

        if name in graph:
            raise ValueError(f"Повтор пакета {name}")

        graph[name] = dependencies

    for dependencies in list(graph.values()):
        for item in dependencies:
            graph.setdefault(item, [])

    return graph
