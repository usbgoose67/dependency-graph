"""Автоматические тесты визуализации графа."""

import unittest

from src.visualize import (
    ascii_tree,
    make_plantuml,
)


class VisualizeTests(unittest.TestCase):
    """Проверки PlantUML и ASCII-дерева."""

    def test_plantuml_start(self):
        """Диаграмма должна начинаться с @startuml."""
        graph = {
            "A": ["B"],
            "B": [],
        }

        result = make_plantuml(graph)

        self.assertTrue(result.startswith("@startuml"))

    def test_plantuml_end(self):
        """Диаграмма должна завершаться @enduml."""
        result = make_plantuml({"A": []})

        self.assertTrue(
            result.strip().endswith("@enduml")
        )

    def test_plantuml_edge(self):
        """В диаграмме должно присутствовать ребро."""
        graph = {
            "A": ["B"],
            "B": [],
        }

        result = make_plantuml(graph)

        self.assertIn("n0 --> n1", result)

    def test_ascii_tree(self):
        """Дерево должно показывать зависимости."""
        graph = {
            "A": ["B"],
            "B": [],
        }

        result = ascii_tree(graph, "A")

        self.assertEqual(
            result,
            "A\n`-- B",
        )

    def test_ascii_cycle(self):
        """Повторные вершины не должны зацикливать обход."""
        graph = {
            "A": ["B"],
            "B": ["A"],
        }

        result = ascii_tree(graph, "A")

        self.assertIn("A (повтор)", result)

    def test_isolated_package(self):
        """Пакет без зависимостей выводится один."""
        graph = {"A": []}

        result = ascii_tree(graph, "A")

        self.assertEqual(result, "A")


if __name__ == "__main__":
    unittest.main()