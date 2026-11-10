"""Тесты чтения Maven POM."""

import unittest
from src.maven import parse_pom, pom_url


POM = b"""
<project>
    <dependencies>
        <dependency>
            <groupId>org.example</groupId>
            <artifactId>core</artifactId>
            <version>1.0</version>
        </dependency>
        <dependency>
            <groupId>org.example</groupId>
            <artifactId>tests</artifactId>
            <version>1.0</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
"""


class MavenTests(unittest.TestCase):
    """Проверки работы с POM."""

    def test_pom_url(self):
        """Адрес POM формируется правильно."""
        url = pom_url("https://repo.test", "org.demo:app", "1.0")
        self.assertEqual(
            url,
            "https://repo.test/org/demo/app/1.0/app-1.0.pom"
        )

    def test_dependencies(self):
        """Прямые зависимости читаются из XML."""
        result = parse_pom(POM)
        self.assertEqual(result, [("org.example:core", "1.0")])

    def test_invalid_xml(self):
        """Некорректный XML вызывает ошибку."""
        with self.assertRaises(ValueError):
            parse_pom(b"<broken>")
