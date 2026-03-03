#!/usr/bin/env python3
"""
vt_scan.py — учебный скрипт для отправки файла на проверку в VirusTotal.
Я нашел github-репозиторий VirusTotal, там почти все уже реализовано.
Требования:
API-ключ VirusTotal

Как запускать:
1) pip install -r requirements.txt
2) export VT_API_KEY="ключ"
3) python vt_scan.py /path/to/file.exe

Скрипт ждёт завершения анализа на сайте и печатает JSON в консоль.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import vt


def get_api_key() -> str:
    key = os.getenv("VT_API_KEY")
    if not key:
        raise SystemExit(
            "Не найден VT_API_KEY.\n"
            "Задайте переменную окружения:\n"
            "export VT_API_KEY=\"...\""
        )
    return key


def wait_until_completed(client: vt.Client, analysis_id: str, interval: int) -> vt.Object:
    while True:
        analysis = client.get_object("/analyses/{}", analysis_id)
        status = analysis.get("status")

        # статус печатаем в stderr, чтобы stdout оставался чистым JSON
        print(f"[i] status={status}", file=sys.stderr)

        if status == "completed":
            return analysis

        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Отправка файла на проверку в VirusTotal, ожидание результата, вывод JSON."
    )
    parser.add_argument("path", help="Путь к файлу для проверки.")
    parser.add_argument(
        "--interval",
        type=int,
        default=20,
        help="Пауза (сек) между проверками статуса (по умолчанию 20 секунд).",
    )
    args = parser.parse_args()

    api_key = get_api_key()
    file_path = Path(args.path)

    if not file_path.exists() or not file_path.is_file():
        raise SystemExit(f"Файл не найден: {file_path}")

    try:
        with vt.Client(api_key, agent="student-vt-script/1.0", trust_env=True) as client:
            # 1) Отправляем файл на анализ
            with file_path.open("rb") as f:
                analysis = client.scan_file(f)

            # 2) Ждём завершения анализа
            analysis = wait_until_completed(client, analysis.id, args.interval)

    except vt.APIError as err:
        raise SystemExit(f"VirusTotal API error: {err}") from err
    except KeyboardInterrupt:
        raise SystemExit("Остановлено.")

    # 3) Вывод JSON в stdout
    print(json.dumps(analysis.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()