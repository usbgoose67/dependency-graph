"""Тесты настроек приложения."""

import unittest
from src.config import read_config


URL = "https://repo.maven.apache.org/maven2"


class ConfigTests(unittest.TestCase):
    """Проверка аргументов командной строки."""

    def test_correct_config(self):
        """Корректные аргументы принимаются."""
        args = read_config([
            "--package", "org.slf4j:slf4j-api",
            "--repo", URL,
            "--version", "2.0.13",
        ])
        self.assertEqual(args.version, "2.0.13")

    def test_missing_package(self):
        """Отсутствие пакета вызывает ошибку."""
        with self.assertRaises(SystemExit):
            read_config(["--repo", URL])

    def test_bad_repository(self):
        """Некорректный URL отклоняется."""
        with self.assertRaises(SystemExit):
            read_config([
                "--package", "a:b",
                "--repo", "wrong",
            ])

    def test_bad_version(self):
        """Некорректная версия отклоняется."""
        with self.assertRaises(SystemExit):
            read_config([
                "--package", "a:b",
                "--repo", URL,
                "--version", "bad version",
            ])

    def test_bad_output(self):
        """Неверное расширение отклоняется."""
        with self.assertRaises(SystemExit):
            read_config([
                "--package", "a:b",
                "--repo", URL,
                "--output", "graph.png",
            ])

    def test_missing_test_file(self):
        """Отсутствующий тестовый файл отклоняется."""
        with self.assertRaises(SystemExit):
            read_config([
                "--package", "A",
                "--repo", "missing.txt",
                "--test",
            ])

    def test_bad_test_package(self):
        """Строчные буквы в тестовом имени отклоняются."""
        with self.assertRaises(SystemExit):
            read_config([
                "--package", "a",
                "--repo", __file__,
                "--test",
            ])
