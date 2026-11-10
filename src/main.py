"""Главный файл приложения."""

from src.config import read_config
from src.maven import get_dependencies


def main():
    """Показать прямые зависимости Maven-пакета."""
    args = read_config()

    if args.test:
        print("Тестовый режим будет добавлен на этапе 3")
        return

    try:
        dependencies = get_dependencies(
            args.repo, args.package, args.version
        )
    except ValueError as error:
        print("Ошибка:", error)
        return

    print("Пакет:", args.package)
    print("Версия:", args.version)
    print("Прямые зависимости:")

    if not dependencies:
        print("Зависимости не найдены")

    for package, version in dependencies:
        print(f"- {package}:{version}")


if __name__ == "__main__":
    main()
