"""Recursive file sorting by extension. Usage: python task_1.py SOURCE [DESTINATION]"""
import argparse
import shutil
from pathlib import Path


def unique_target(folder: Path, filename: str) -> Path:
    """Prevent overwriting files with identical names from different folders."""
    target = folder / filename
    number = 1
    while target.exists():
        target = folder / f"{Path(filename).stem}_{number}{Path(filename).suffix}"
        number += 1
    return target


def copy_recursive(source: Path, destination: Path) -> tuple[int, int]:
    """Recursively walk source and copy files into extension-based folders."""
    copied = 0
    errors = 0
    try:
        entries = list(source.iterdir())
    except OSError as exc:
        print(f"Не вдалося прочитати {source}: {exc}")
        return 0, 1

    for entry in entries:
        try:
            if entry.is_symlink():
                print(f"Пропущено символічне посилання: {entry}")
                continue
            if entry.is_dir():
                sub_copied, sub_errors = copy_recursive(entry, destination)
                copied += sub_copied
                errors += sub_errors
            elif entry.is_file():
                extension = entry.suffix.lower().lstrip('.') or 'no_extension'
                folder = destination / extension
                folder.mkdir(parents=True, exist_ok=True)
                target = unique_target(folder, entry.name)
                shutil.copy2(entry, target)
                print(f"{entry} -> {target}")
                copied += 1
        except OSError as exc:
            errors += 1
            print(f"Помилка обробки {entry}: {exc}")
    return copied, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Рекурсивне копіювання файлів за розширеннями")
    parser.add_argument('source', type=Path, help='Вихідна директорія')
    parser.add_argument('destination', nargs='?', type=Path, default=Path('dist'), help='Директорія призначення (dist)')
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    destination = args.destination.expanduser().resolve()

    if not source.is_dir():
        parser.error(f"Вихідна директорія не існує: {source}")
    if destination == source or source in destination.parents:
        parser.error('Директорія призначення не може бути всередині вихідної директорії')
    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        parser.error(f"Не вдалося створити директорію призначення: {exc}")
    copied, errors = copy_recursive(source, destination)
    print(f"Готово. Скопійовано: {copied}; помилок: {errors}.")


if __name__ == '__main__':
    main()
