"""
Главный модуль программы "Учебный план".

"""

from Curriculum import Curriculum
from DisciplineException import DisciplineException, EmptyDatabaseError


# Путь к файлу базы данных по умолчанию
DEFAULT_DATABASE_FILE = "disciplines_database.json"


def print_separator():
    """Вывод разделительной линии."""
    print("=" * 70)


def print_header(title):
    """Вывод заголовка раздела."""
    print_separator()
    print(f"  {title}")
    print_separator()


def print_disciplines_table(disciplines):
    """
    Форматированный вывод списка дисциплин в виде таблицы.

    Args:
        disciplines: Список объектов Discipline
    """
    if not disciplines:
        print("Список пуст.")
        return

    # Заголовок таблицы
    print(f"{'№':<3} | {'Название':<30} | {'Сем.':<4} | {'Длит.':<5} | "
          f"{'Часы':<4} | {'Отчётность':<10} | {'Кафедра':<20}")
    print("-" * 100)

    # Данные таблицы
    for i, d in enumerate(disciplines, 1):
        name = d.name[:28] + ".." if len(d.name) > 30 else d.name
        dept = d.department[:18] + ".." if len(d.department) > 20 else d.department
        print(f"{i:<3} | {name:<30} | {d.semester:<4} | {d.duration:<5} | "
              f"{d.hours:<4} | {d.report_type:<10} | {dept:<20}")

    print("-" * 100)
    print(f"Всего записей: {len(disciplines)}")


def input_int(prompt, min_val=None, max_val=None):
    """
    Безопасный ввод целого числа с валидацией.

    Args:
        prompt: Текст приглашения для ввода
        min_val: Минимально допустимое значение (опционально)
        max_val: Максимально допустимое значение (опционально)

    Returns:
        int: Введённое число или None при прерывании ввода
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Ошибка: значение должно быть не меньше {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Ошибка: значение должно быть не больше {max_val}.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число.")
        except EOFError:
            print("\nВвод завершён.")
            return min_val if min_val is not None else 0


def show_main_menu():
    """Отображение главного меню."""
    print("\n" + "=" * 50)
    print("        ПРОГРАММА 'УЧЕБНЫЙ ПЛАН'")
    print("=" * 50)
    print("1. Показать полный список дисциплин (отсортированный)")
    print("2. Показать дисциплины по виду отчётности")
    print("3. Показать дисциплины по диапазону часов")
    print("4. Показать статистику")
    print("0. Выход")
    print("=" * 50)


def handle_full_list(curriculum):
    """
    Обработка вывода полного отсортированного списка.

    Сортировка: семестр (↑) + кафедра (↑) + часы (↓)

    Args:
        curriculum: Объект Curriculum
    """
    print_header("ПОЛНЫЙ СПИСОК ДИСЦИПЛИН")
    print("Сортировка: семестр (по возрастанию) → кафедра (по возрастанию) → часы (по убыванию)")
    print()

    try:
        disciplines = curriculum.get_full_list_sorted()
        print_disciplines_table(disciplines)
    except EmptyDatabaseError as e:
        print(f"Ошибка: {e}")


def handle_by_report_type(curriculum):
    """
    Обработка вывода списка по виду отчётности.

    Сортировка: продолжительность (↑) + часы (↓)

    Args:
        curriculum: Объект Curriculum
    """
    print_header("ДИСЦИПЛИНЫ ПО ВИДУ ОТЧЁТНОСТИ")
    print("Доступные виды отчётности: зачёт, экзамен")
    print("Сортировка: продолжительность курса (по возрастанию) → часы (по убыванию)")
    print()

    report_type = input("Введите вид отчётности: ").strip().lower()

    try:
        disciplines = curriculum.get_by_report_type(report_type)
        if disciplines:
            print(f"\nДисциплины с отчётностью '{report_type}':")
            print_disciplines_table(disciplines)
        else:
            print(f"Дисциплины с видом отчётности '{report_type}' не найдены.")
    except EmptyDatabaseError as e:
        print(f"Ошибка: {e}")


def handle_by_hours_range(curriculum):
    """
    Обработка вывода списка по диапазону часов.

    Сортировка: кафедра (↑) + часы (↓)

    Args:
        curriculum: Объект Curriculum
    """
    print_header("ДИСЦИПЛИНЫ ПО ДИАПАЗОНУ ЧАСОВ")
    print("Допустимый диапазон часов: 36-216")
    print("Сортировка: кафедра (по возрастанию) → часы (по убыванию)")
    print()

    min_hours = input_int("Введите минимальное количество часов (N1): ", 36, 216)
    max_hours = input_int("Введите максимальное количество часов (N2): ", 36, 216)

    try:
        disciplines = curriculum.get_by_hours_range(min_hours, max_hours)
        if disciplines:
            print(f"\nДисциплины с количеством часов от {min_hours} до {max_hours}:")
            print_disciplines_table(disciplines)
        else:
            print(f"Дисциплины с количеством часов от {min_hours} до {max_hours} не найдены.")
    except EmptyDatabaseError as e:
        print(f"Ошибка: {e}")


def handle_statistics(curriculum):
    """
    Вывод статистики по загруженным данным.

    Args:
        curriculum: Объект Curriculum
    """
    print_header("СТАТИСТИКА")

    count = curriculum.get_disciplines_count()
    if count == 0:
        print("База данных пуста. Сначала загрузите данные.")
        return

    print(f"Всего дисциплин: {count}")
    print()

    # Список всех дисциплин
    names = curriculum.get_all_discipline_names()
    print(f"Дисциплины ({len(names)}):")
    for i, name in enumerate(names, 1):
        print(f"  {i:2}. {name}")
    print()

    # Список кафедр
    departments = curriculum.get_unique_departments()
    print(f"Кафедры ({len(departments)}):")
    for dept in departments:
        print(f"  - {dept}")
    print()

    # Виды отчётности
    report_types = curriculum.get_unique_report_types()
    print(f"Виды отчётности: {', '.join(report_types)}")


def main():
    """Главная функция программы с циклическим меню."""
    curriculum = Curriculum()

    # Автоматическая загрузка базы данных при запуске
    print("Загрузка базы данных...")
    try:
        curriculum.load_from_file(DEFAULT_DATABASE_FILE)
    except DisciplineException as e:
        print(f"Ошибка при загрузке базы данных: {e}")
        print("Программа не может продолжить работу.")
        return

    try:
        while True:
            show_main_menu()
            choice = input("Выберите пункт меню: ").strip()

            if choice == '1':
                handle_full_list(curriculum)
            elif choice == '2':
                handle_by_report_type(curriculum)
            elif choice == '3':
                handle_by_hours_range(curriculum)
            elif choice == '4':
                handle_statistics(curriculum)
            elif choice == '0':
                print("\nДо свидания!")
                break
            else:
                print("\nОшибка: неверный пункт меню. Попробуйте снова.")

            input("\nНажмите Enter для продолжения")
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем. До свидания!")
    except EOFError:
        print("\n\nВвод завершён. До свидания!")


if __name__ == "__main__":
    main()
