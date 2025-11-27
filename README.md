# Python CSV Analyzer

Этот проект предназначен для генерации аналитических отчётов по сотрудникам на основе одного или нескольких CSV-файлов. Главная особенность - потоковая обработка данных, при которой строки читаются построчно, без загрузки всего файла в память. 

## Пример использования
```bash
python main.py --files employees1.csv --report performance
```
Неизвестные аргументы допускаются:
```bash
python main.py --files a.csv --report performance --debug --test 123
```

## Добавление отчёта
1. Создайте функцию анализа:
```python
def tasks_report(filenames):
    ...
    return [[position, value]]
```
2. Зарегистритруйте её в словаре *REPORTS*:
```python
REPORTS = {
    "performance": calculate_average_performance_streaming,
    "tasks": tasks_report
}
```
3. Готово. Отчёт доступен:
```bash
python3 main.py --files data.csv --report tasks
```

## Тестирование
Проект использует `pytest` и `pytest-cov`. На данный момент покрытие кода - **69%**