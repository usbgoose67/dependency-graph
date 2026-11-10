"""Получение прямых зависимостей Maven-пакетов."""

import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def pom_url(repository, package, version):
    """Построить URL POM-файла."""
    group, artifact = package.split(":")
    folder = group.replace(".", "/")
    name = f"{artifact}-{version}.pom"
    return (
        f"{repository.rstrip('/')}/{folder}/"
        f"{artifact}/{version}/{name}"
    )


def download_pom(repository, package, version):
    """Загрузить POM-файл из репозитория."""
    url = pom_url(repository, package, version)
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return response.read()
    except (urllib.error.URLError, TimeoutError) as error:
        raise ValueError(
            f"Не удалось получить POM: {url}"
        ) from error


def child_text(element, name):
    """Получить текст дочернего XML-элемента."""
    child = element.find(f"{{*}}{name}")
    if child is None or child.text is None:
        return ""
    return child.text.strip()


def get_properties(root):
    """Собрать свойства Maven-проекта."""
    properties = {}
    section = root.find("{*}properties")
    if section is not None:
        for child in section:
            key = child.tag.split("}")[-1]
            properties[key] = child.text or ""
    return properties


def resolve(value, properties):
    """Заменить простую переменную Maven на значение."""
    for _ in range(10):
        if not value.startswith("${") or not value.endswith("}"):
            break
        key = value[2:-1]
        if key not in properties:
            break
        value = properties[key]
    return value


def parse_pom(content):
    """Извлечь прямые зависимости из XML."""
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        raise ValueError("Некорректный XML POM") from error

    properties = get_properties(root)
    properties["project.version"] = child_text(root, "version")
    dependencies = []
    section = root.find("{*}dependencies")
    if section is None:
        return dependencies

    for item in section.findall("{*}dependency"):
        group = resolve(child_text(item, "groupId"), properties)
        artifact = resolve(child_text(item, "artifactId"), properties)
        version = resolve(child_text(item, "version"), properties)
        scope = child_text(item, "scope") or "compile"
        optional = child_text(item, "optional")
        if scope in ("test", "provided", "system"):
            continue
        if optional == "true":
            continue
        if group and artifact and version:
            dependencies.append((f"{group}:{artifact}", version))
    return dependencies


def get_dependencies(repository, package, version):
    """Получить прямые зависимости указанного пакета."""
    content = download_pom(repository, package, version)
    return parse_pom(content)
