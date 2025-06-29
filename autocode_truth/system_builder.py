# -*- coding: utf-8 -*-
# system_builder.py (v2.0)
# ПРОТОКОЛ "ПОЛНАЯ КОНСОЛИДАЦИЯ КОНТЕКСТА"

import os
import glob

# --- НАСТРОЙКИ ---
# Пути к репозиториям, которые нужно обработать
REPOSITORIES_TO_SCAN = {
    "SYSTEM": r"D:\project-continuity",
    "PROJECT": r"D:\Проекты\Игры\lighthouse_keeper"
}

# Директория для хранения логов сессий
SESSIONS_PATH = r"D:\project-continuity\_ark_init\_sessions"

# Имя выходного файла
OUTPUT_FILE = r"D:\project-continuity\FLAT_CONTEXT.md"

# Типы файлов, которые нужно включить в контекст
FILE_EXTENSIONS = ('.md', '.gd', '.tscn', '.tres', '.py', '.bat')


def find_latest_session_log(path):
    """Находит самый последний файл лога в указанной директории."""
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        if not files:
            return None
        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(path, f)))
        return os.path.join(path, latest_file)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"[ERROR] Не удалось найти лог сессии: {e}")
        return None


def gather_context():
    """Собирает содержимое всех релевантных файлов в один строковый блок."""
    full_context = []
    print("[INFO] Начало сбора контекста...")

    # 1. Собираем файлы из основных репозиториев
    for repo_name, repo_path in REPOSITORIES_TO_SCAN.items():
        print(f"[INFO] Сканирование репозитория '{repo_name}' в '{repo_path}'...")
        search_pattern = os.path.join(repo_path, '**', '*')
        all_files = glob.glob(search_pattern, recursive=True)

        for file_path in all_files:
            if os.path.isfile(file_path) and file_path.endswith(FILE_EXTENSIONS):
                # Исключаем сами инструменты сборки
                if "autocode_" in file_path or "FIX_EVERYTHING" in file_path:
                    continue
                
                relative_path = os.path.relpath(file_path, os.path.dirname(repo_path))
                full_context.append(f"\n\n--- FILE: {relative_path} ---\n\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        full_context.append(f.read())
                except Exception as e:
                    full_context.append(f"!!! ОШИБКА ЧТЕНИЯ ФАЙЛА: {e} !!!")
    
    # 2. Добавляем самый последний лог сессии
    print(f"[INFO] Поиск последнего лога сессии в '{SESSIONS_PATH}'...")
    latest_log_path = find_latest_session_log(SESSIONS_PATH)
    if latest_log_path:
        relative_log_path = os.path.relpath(latest_log_path, os.path.dirname(REPOSITORIES_TO_SCAN["SYSTEM"]))
        print(f"[INFO] Найден и добавлен последний лог: {os.path.basename(latest_log_path)}")
        full_context.append(f"\n\n--- LAST SESSION LOG: {relative_log_path} ---\n\n")
        try:
            with open(latest_log_path, 'r', encoding='utf-8') as f:
                full_context.append(f.read())
        except Exception as e:
            full_context.append(f"!!! ОШИБКА ЧТЕНИЯ ЛОГА: {e} !!!")
    else:
        print("[WARN] Последний лог сессии не найден.")

    return "".join(full_context)


def write_output_file(content):
    """Записывает собранный контекст в выходной файл."""
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n[SUCCESS] Полный контекст успешно сохранен в файл: {OUTPUT_FILE}")
    except Exception as e:
        print(f"\n[FATAL ERROR] Не удалось записать выходной файл: {e}")


if __name__ == "__main__":
    context_data = gather_context()
    write_output_file(context_data)