"""Тесты обратных зависимостей."""

import unittest
from pathlib import Path

from src.graph import find_reverse_dependencies, reverse_graph
from src.test_repo import read_test_repo


DATA = Path(__file__).parent / "data"


class ReverseTests(unittest.TestCase):
    """Проверки обратного графа."""

    def test_reverse_edges(self):
        """Рёбра меняют направление."""
        graph = {"A": ["B"], "B": []}
        result = reverse_graph(graph)
        self.assertEqual(result["B"], ["A"])

    def test_normal_reverse(self):
        """Находятся прямые и косвенные потребители."""
        graph = read_test_repo(DATA / "normal.txt")
        result = find_reverse_dependencies(graph, "F")
        self.assertEqual(set(result), set("ABCE"))

    def test_cycle_reverse(self):
        """Обратный обход обрабатывает цикл."""
        graph = read_test_repo(DATA / "cycle.txt")
        result = find_reverse_dependencies(graph, "A")
        self.assertEqual(set(result), set("BC"))

    def test_empty_reverse(self):
        """Для изолированной вершины результат пустой."""
        graph = read_test_repo(DATA / "empty.txt")
        result = find_reverse_dependencies(graph, "A")
        self.assertEqual(result, [])

    def test_unknown_package(self):
        """Неизвестный пакет вызывает ошибку."""
        with self.assertRaises(ValueError):
            find_reverse_dependencies({"A": []}, "Z")
