# main.py

from app.parser_public import find_pastes
from app.parser_onion import parse_onion_forum  # обязательно создай этот файл / make sure this file exists
from app.exporter import export_to_txt


def run_public_parser():
    """
    Запускает парсер публичных paste-сайтов и сохраняет результат.
    Runs the parser for public paste sites and saves the result.
    """
    print("\n[>>>] Запуск парсера публичных источников...")  # Starting public source parser
    public_results = find_pastes(query="email password", limit=5)
    export_to_txt(public_results, filename="public_leaks.txt")
    print(f"[OK] Сохранено {len(public_results)} записей в public_leaks.txt")  # Saved X records


def run_onion_parser():
    """
    Запускает парсер onion-сайтов через Tor и сохраняет результат.
    Runs the parser for onion sites via Tor and saves the result.
    """
    print("\n[>>>] Запуск парсера onion-источников...")  # Starting onion source parser
    onion_results = parse_onion_forum(limit=3)
    export_to_txt(onion_results, filename="onion_leaks.txt")
    print(f"[OK] Сохранено {len(onion_results)} записей в onion_leaks.txt")  # Saved X records


if __name__ == "__main__":
    # Основной запуск скрипта / Main script run
    run_public_parser()
    run_onion_parser()
    print("\n[✔] Пробный анализ завершён.")  # Test analysis complete
