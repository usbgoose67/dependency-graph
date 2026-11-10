"""Тесты обхода графа."""

import unittest
from pathlib import Path

from src.graph import build_graph, graph_edges
from src.test_repo import read_test_repo


DATA = Path(__file__).parent / "data"


class GraphTests(unittest.TestCase):
    """Проверка DFS и тестовых репозиториев."""

    def test_normal_graph(self):
        """DFS находит транзитивные зависимости."""
        repository = read_test_repo(DATA / "normal.txt")
        graph = build_graph(
            "A", lambda name: repository[name]
        )
        self.assertEqual(set(graph), set("ABCDEF"))
        self.assertIn(("B", "D"), graph_edges(graph))

    def test_cycle(self):
        """Цикл не вызывает бесконечный обход."""
        repository = read_test_repo(DATA / "cycle.txt")
        graph = build_graph(
            "A", lambda name: repository[name]
        )
        self.assertEqual(set(graph), set("ABCD"))
        self.assertIn(("C", "A"), graph_edges(graph))

    def test_empty(self):
        """Изолированная вершина сохраняется."""
        repository = read_test_repo(DATA / "empty.txt")
        graph = build_graph(
            "A", lambda name: repository[name]
        )
        self.assertEqual(graph, {"A": []})

    def test_missing_file(self):
        """Отсутствующий файл вызывает ошибку."""
        with self.assertRaises(FileNotFoundError):
            read_test_repo(DATA / "missing.txt")

    def test_invalid_line(self):
        """Неверный формат TXT вызывает ошибку."""
        import tempfile

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.txt"
            path.write_text("wrong", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_test_repo(path)
