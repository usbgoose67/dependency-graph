"""Настройки приложения из командной строки."""

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse


def package_name(value):
    """Проверить имя пакета Maven или тестового пакета."""
    pattern = r"[A-Za-z0-9_.-]+(:[A-Za-z0-9_.-]+)?"
    if not re.fullmatch(pattern, value):
        raise argparse.ArgumentTypeError(
            "Имя пакета должно быть NAME или group:artifact"
        )
    return value


def version_name(value):
    """Проверить версию пакета."""
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise argparse.ArgumentTypeError("Некорректная версия")
    return value


def output_name(value):
    """Проверить имя выходного SVG-файла."""
    path = Path(value)
    if path.suffix.lower() != ".svg" or path.name != value:
        raise argparse.ArgumentTypeError(
            "Укажите имя файла с расширением .svg"
        )
    return value


def make_parser():
    """Создать обработчик аргументов."""
    parser = argparse.ArgumentParser(
        description="Анализ зависимостей Maven"
    )
    parser.add_argument(
        "--package", required=True, type=package_name
    )
    parser.add_argument("--repo", required=True)
    parser.add_argument("--test", action="store_true")
    parser.add_argument(
        "--version", default="1.0", type=version_name
    )
    parser.add_argument(
        "--output", default="graph.svg", type=output_name
    )
    parser.add_argument("--ascii", action="store_true")
    return parser


def read_config(arguments=None):
    """Прочитать и проверить настройки."""
    parser = make_parser()
    args = parser.parse_args(arguments)

    if args.test:
        if not Path(args.repo).is_file():
            parser.error("Тестовый файл не найден")
        if not re.fullmatch(r"[A-Z]+", args.package):
            parser.error("Тестовый пакет должен быть A-Z")
    else:
        url = urlparse(args.repo)
        if url.scheme not in ("http", "https") or not url.netloc:
            parser.error("Нужен корректный URL репозитория")
        if ":" not in args.package:
            parser.error("Для Maven укажите group:artifact")

    return args
