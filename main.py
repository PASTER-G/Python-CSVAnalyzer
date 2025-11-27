import argparse
import csv
import sys

try:
    from tabulate import tabulate
except ImportError:
    print("Ошибка: библиотека tabulate не установлена.\nУстановите: pip install tabulate")
    sys.exit(1)

def stream_employee_data(filenames):
    """
    Потоковое чтение CSV.
    Строки не сохраняются — функция генерирует очищенные записи.
    """
    global err_counter
    for filename in filenames:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                if reader.fieldnames is None:
                    print(f"Ошибка: файл {filename} пустой или повреждён.")
                    continue
                reader.fieldnames = [name.strip() for name in reader.fieldnames]

                for row in reader:
                    clean_row = {}

                    for key, value in row.items():
                        if key is None:
                            continue
                        clean_row[key.strip()] = value.strip() if value is not None else ""
                    yield clean_row

        except FileNotFoundError:
            err_counter += 1
            print(f"Ошибка: файл {filename} не найден.")
            continue
        except UnicodeDecodeError:
            err_counter += 1
            print(f"Ошибка: неверная кодировка в файле {filename}. Используйте UTF-8.")
            continue
        except Exception as e:
            err_counter += 1
            print(f"Ошибка при чтении {filename}: {e}")
            continue

def calculate_average_performance_streaming(filenames):
    """
    Потоковый подсчёт средних значений:
    храним только сумму и количество по каждой должности.
    """
    totals = {}      # {position: sum}
    counts = {}      # {position: count}
    for employee in stream_employee_data(filenames):
        if "position" not in employee:
            print("Предупреждение: отсутствует поле 'position'. Строка пропущена.")
            continue
        if "performance" not in employee:
            print("Предупреждение: отсутствует поле 'performance'. Строка пропущена.")
            continue
        position = employee["position"]

        try:
            score = float(employee["performance"])
        except ValueError:
            print(f"Предупреждение: performance '{employee['performance']}' не является числом. Строка пропущена.")
            continue

        if position not in totals:
            totals[position] = 0.0
            counts[position] = 0
        totals[position] += score
        counts[position] += 1
    report = [
        [position, round(totals[position] / counts[position], 2)]
        for position in totals
    ]
    report.sort(key=lambda x: x[1], reverse=True)
    return report

def tasks_report(filenames):
    return [["test", "test_answ"]]

REPORTS = {
    "performance": calculate_average_performance_streaming,
    "tasks": tasks_report
}
err_counter = 0

def main():
    parser = argparse.ArgumentParser(description="Генератор отчётов (стриминговый)")
    parser.add_argument("--files", nargs="+", required=True, help="CSV файлы")
    parser.add_argument("--report", required=True, choices=REPORTS.keys())
    args, unknown = parser.parse_known_args()
    report = REPORTS[args.report](args.files)
    if err_counter < len(args.files):
        print(tabulate(report, headers=["position", "performance"], tablefmt="simple"))

if __name__ == "__main__":
    main()
