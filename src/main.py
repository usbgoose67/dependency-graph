"""Главный файл приложения."""

from src.config import read_config


def main():
    """Показать настройки приложения."""
    args = read_config()
    print("Параметры программы:")
    print("package =", args.package)
    print("repo =", args.repo)
    print("test =", args.test)
    print("version =", args.version)
    print("output =", args.output)
    print("ascii =", args.ascii)


if __name__ == "__main__":
    main()
