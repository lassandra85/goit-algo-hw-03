import argparse
from pathlib import Path
import shutil


def parse_arguments():
    parser = argparse.ArgumentParser(description="Рекурсивне копіювання та сортування файлів за розширеннями.")
    parser.add_argument("src", help="Шлях до вихідної директорії.")
    parser.add_argument("dst", nargs="?", default="dist", help="Шлях до директорії призначення (за замовчуванням: dist).")
    return parser.parse_args()


def process_directory(src: Path, dst: Path) -> None:
    try:
        # Перебір елементів директорії
        for item in src.iterdir():
            # Якщо елемент — директорія, викликаємо функцію рекурсивно
            if item.is_dir():
                process_directory(item, dst)

            # Якщо елемент — файл, копіюємо його
            elif item.is_file():
                extension = item.suffix.lower()[1:]  # Отримуємо розширення файлу (без крапки)
                if extension:
                    target_dir = dst / extension
                    target_dir.mkdir(parents=True, exist_ok=True)  # Створюємо піддиректорію, якщо її не існує
                    shutil.copy(item, target_dir / item.name)

    except PermissionError:
        print(f"Помилка доступу до директорії: {src}")
    except Exception as e:
        print(f"Невідома помилка: {e}")


def main():
    # Отримуємо аргументи командного рядка
    args = parse_arguments()
    src = Path(args.src).resolve()
    dst = Path(args.dst).resolve()

    # Перевіряємо, чи існує вихідна директорія
    if not src.exists() or not src.is_dir():
        print(f"Директорія '{src}' не існує, або не являється директорією.")
        return

    # Створюємо директорію призначення, якщо її не існує
    dst.mkdir(parents=True, exist_ok=True)

    process_directory(src, dst)


if __name__ == "__main__":
    main()