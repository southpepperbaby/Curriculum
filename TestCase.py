"""
Модуль с тестами для проверки корректности работы программы "Учебный план".

Запуск: python TestCase.py
"""

from Discipline import Discipline
from Curriculum import Curriculum
from DisciplineException import (
    InvalidSemesterError,
    InvalidDurationError,
    InvalidHoursError,
    InvalidReportTypeError,
    FileOperationError,
    EmptyDatabaseError
)


class TestRunner:
    """Класс для запуска тестов и вывода результатов."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []

    def add_test(self, name, test_func):
        """Добавление теста в список."""
        self.tests.append((name, test_func))

    def run_all(self):
        """Запуск всех тестов."""
        print("=" * 70)
        print("  ЗАПУСК ТЕСТОВ")
        print("=" * 70)

        for name, test_func in self.tests:
            try:
                test_func()
                self.passed += 1
                print(f"[УСПЕХ] {name}")
            except AssertionError as e:
                self.failed += 1
                print(f"[ПРОВАЛ] {name}: {e}")
            except Exception as e:
                self.failed += 1
                print(f"[ОШИБКА] {name}: {type(e).__name__}: {e}")

        print("=" * 70)
        print(f"  ИТОГО: {self.passed} успешно, {self.failed} провалено")
        print("=" * 70)


# =============================================================================
# ТЕСТЫ КЛАССА DISCIPLINE
# =============================================================================

def test_discipline_creation_valid():
    """Тест создания дисциплины с корректными данными."""
    d = Discipline("Математика", 1, 2, 108, "экзамен", "Кафедра математики")
    assert d.name == "Математика"
    assert d.semester == 1
    assert d.duration == 2
    assert d.hours == 108
    assert d.report_type == "экзамен"
    assert d.department == "Кафедра математики"


def test_discipline_invalid_semester_low():
    """Тест на некорректный семестр (меньше 1)."""
    try:
        Discipline("Тест", 0, 1, 72, "зачёт", "Кафедра")
        assert False, "Должно было возникнуть исключение"
    except InvalidSemesterError:
        pass


def test_discipline_invalid_semester_high():
    """Тест на некорректный семестр (больше 8)."""
    try:
        Discipline("Тест", 9, 1, 72, "зачёт", "Кафедра")
        assert False, "Должно было возникнуть исключение"
    except InvalidSemesterError:
        pass


def test_discipline_invalid_duration():
    """Тест на некорректную продолжительность (выход за 8 семестр)."""
    try:
        # Семестр 7 + 3 = 10 > 8
        Discipline("Тест", 7, 3, 72, "зачёт", "Кафедра")
        assert False, "Должно было возникнуть исключение"
    except InvalidDurationError:
        pass


def test_discipline_max_duration():
    """Тест на максимально допустимую продолжительность."""
    # Семестр 1 + 8 = 9, но 1 + 8 - 1 = 8 <= 8, допустимо
    d = Discipline("Тест", 1, 8, 72, "зачёт", "Кафедра")
    assert d.duration == 8


def test_discipline_invalid_hours_low():
    """Тест на некорректные часы (меньше 36)."""
    try:
        Discipline("Тест", 1, 1, 35, "зачёт", "Кафедра")
        assert False, "Должно было возникнуть исключение"
    except InvalidHoursError:
        pass


def test_discipline_invalid_hours_high():
    """Тест на некорректные часы (больше 216)."""
    try:
        Discipline("Тест", 1, 1, 217, "зачёт", "Кафедра")
        assert False, "Должно было возникнуть исключение"
    except InvalidHoursError:
        pass


def test_discipline_invalid_report_type():
    """Тест на некорректный вид отчётности."""
    try:
        Discipline("Тест", 1, 1, 72, "тест", "Кафедра")
        assert False, "Должно было возникнуть исключение"
    except InvalidReportTypeError:
        pass


def test_discipline_to_dict():
    """Тест преобразования дисциплины в словарь."""
    d = Discipline("Физика", 2, 1, 108, "экзамен", "Кафедра физики")
    data = d.to_dict()
    assert data["name"] == "Физика"
    assert data["semester"] == 2
    assert data["hours"] == 108


def test_discipline_from_dict():
    """Тест создания дисциплины из словаря."""
    data = {
        "name": "Химия",
        "semester": 3,
        "duration": 1,
        "hours": 72,
        "report_type": "зачёт",
        "department": "Кафедра химии"
    }
    d = Discipline.from_dict(data)
    assert d.name == "Химия"
    assert d.semester == 3


# =============================================================================
# ТЕСТЫ КЛАССА CURRICULUM
# =============================================================================

def test_curriculum_load_file():
    """Тест загрузки данных из файла."""
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    assert c.get_disciplines_count() >= 25


def test_curriculum_load_nonexistent_file():
    """Тест загрузки несуществующего файла."""
    c = Curriculum()
    try:
        c.load_from_file("nonexistent_file.json")
        assert False, "Должно было возникнуть исключение"
    except FileOperationError:
        pass


def test_curriculum_empty_database():
    """Тест работы с пустой базой данных."""
    c = Curriculum()
    try:
        c.get_full_list_sorted()
        assert False, "Должно было возникнуть исключение"
    except EmptyDatabaseError:
        pass


def test_curriculum_full_list_sorting():
    """
    Тест сортировки полного списка.
    Ключ: семестр (↑) + кафедра (↑) + часы (↓)
    """
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    result = c.get_full_list_sorted()

    # Проверяем, что список отсортирован правильно
    for i in range(len(result) - 1):
        curr = result[i]
        next_item = result[i + 1]

        # Сначала по семестру (возрастание)
        if curr.semester < next_item.semester:
            continue
        elif curr.semester > next_item.semester:
            assert False, f"Нарушена сортировка по семестру: {curr.semester} > {next_item.semester}"

        # При равных семестрах - по кафедре (возрастание)
        if curr.department < next_item.department:
            continue
        elif curr.department > next_item.department:
            assert False, f"Нарушена сортировка по кафедре: {curr.department} > {next_item.department}"

        # При равных кафедрах - по часам (убывание)
        if curr.hours >= next_item.hours:
            continue
        else:
            assert False, f"Нарушена сортировка по часам: {curr.hours} < {next_item.hours}"


def test_curriculum_by_report_type_exam():
    """Тест фильтрации по виду отчётности 'экзамен'."""
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    result = c.get_by_report_type("экзамен")

    assert len(result) > 0, "Должны быть дисциплины с экзаменом"
    for d in result:
        assert d.report_type == "экзамен", f"Найдена дисциплина с типом {d.report_type}"


def test_curriculum_by_report_type_credit():
    """Тест фильтрации по виду отчётности 'зачёт'."""
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    result = c.get_by_report_type("зачёт")

    assert len(result) > 0, "Должны быть дисциплины с зачётом"
    for d in result:
        assert d.report_type == "зачёт", f"Найдена дисциплина с типом {d.report_type}"


def test_curriculum_by_report_type_sorting():
    """
    Тест сортировки списка по виду отчётности.
    Ключ: продолжительность (↑) + часы (↓)
    """
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    result = c.get_by_report_type("экзамен")

    for i in range(len(result) - 1):
        curr = result[i]
        next_item = result[i + 1]

        # По продолжительности (возрастание)
        if curr.duration < next_item.duration:
            continue
        elif curr.duration > next_item.duration:
            assert False, f"Нарушена сортировка по продолжительности"

        # При равной продолжительности - по часам (убывание)
        if curr.hours >= next_item.hours:
            continue
        else:
            assert False, f"Нарушена сортировка по часам"


def test_curriculum_by_hours_range():
    """Тест фильтрации по диапазону часов."""
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    result = c.get_by_hours_range(100, 150)

    assert len(result) > 0, "Должны быть дисциплины в диапазоне 100-150 часов"
    for d in result:
        assert 100 <= d.hours <= 150, f"Часы {d.hours} вне диапазона [100, 150]"


def test_curriculum_by_hours_range_sorting():
    """
    Тест сортировки списка по диапазону часов.
    Ключ: кафедра (↑) + часы (↓)
    """
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    result = c.get_by_hours_range(50, 200)

    for i in range(len(result) - 1):
        curr = result[i]
        next_item = result[i + 1]

        # По кафедре (возрастание)
        if curr.department < next_item.department:
            continue
        elif curr.department > next_item.department:
            assert False, f"Нарушена сортировка по кафедре"

        # При равной кафедре - по часам (убывание)
        if curr.hours >= next_item.hours:
            continue
        else:
            assert False, f"Нарушена сортировка по часам"


def test_curriculum_by_hours_range_swapped():
    """Тест перестановки границ диапазона (N1 > N2)."""
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    # Передаём границы в неправильном порядке
    result = c.get_by_hours_range(150, 100)

    for d in result:
        assert 100 <= d.hours <= 150, f"Часы {d.hours} вне диапазона [100, 150]"


def test_curriculum_unique_departments():
    """Тест получения уникальных кафедр."""
    c = Curriculum()
    c.load_from_file("disciplines_database.json")
    departments = c.get_unique_departments()

    assert len(departments) >= 4, "Должно быть минимум 4 кафедры"
    assert len(departments) == len(set(departments)), "Кафедры должны быть уникальными"


# =============================================================================
# ТЕСТЫ АЛГОРИТМА БИНАРНОЙ СОРТИРОВКИ
# =============================================================================

def test_binary_insertion_sort_simple():
    """Тест сортировки простого списка чисел."""
    c = Curriculum()
    items = [5, 2, 8, 1, 9, 3]
    result = c._binary_insertion_sort(items, lambda x: x)
    assert result == [1, 2, 3, 5, 8, 9]


def test_binary_insertion_sort_reverse():
    """Тест сортировки в обратном порядке."""
    c = Curriculum()
    items = [1, 2, 3, 4, 5]
    result = c._binary_insertion_sort(items, lambda x: -x)
    assert result == [5, 4, 3, 2, 1]


def test_binary_insertion_sort_empty():
    """Тест сортировки пустого списка."""
    c = Curriculum()
    result = c._binary_insertion_sort([], lambda x: x)
    assert result == []


def test_binary_insertion_sort_single():
    """Тест сортировки списка из одного элемента."""
    c = Curriculum()
    result = c._binary_insertion_sort([42], lambda x: x)
    assert result == [42]


def test_binary_insertion_sort_duplicates():
    """Тест сортировки списка с дубликатами."""
    c = Curriculum()
    items = [3, 1, 2, 1, 3, 2]
    result = c._binary_insertion_sort(items, lambda x: x)
    assert result == [1, 1, 2, 2, 3, 3]


# =============================================================================
# ЗАПУСК ТЕСТОВ
# =============================================================================

def main():
    """Главная функция запуска тестов."""
    runner = TestRunner()

    # Тесты класса Discipline
    runner.add_test("Создание дисциплины с корректными данными", test_discipline_creation_valid)
    runner.add_test("Проверка семестра < 1", test_discipline_invalid_semester_low)
    runner.add_test("Проверка семестра > 8", test_discipline_invalid_semester_high)
    runner.add_test("Проверка продолжительности (выход за 8 семестр)", test_discipline_invalid_duration)
    runner.add_test("Максимальная продолжительность (8 семестров)", test_discipline_max_duration)
    runner.add_test("Проверка часов < 36", test_discipline_invalid_hours_low)
    runner.add_test("Проверка часов > 216", test_discipline_invalid_hours_high)
    runner.add_test("Проверка некорректного вида отчётности", test_discipline_invalid_report_type)
    runner.add_test("Преобразование в словарь (to_dict)", test_discipline_to_dict)
    runner.add_test("Создание из словаря (from_dict)", test_discipline_from_dict)

    # Тесты класса Curriculum
    runner.add_test("Загрузка данных из файла", test_curriculum_load_file)
    runner.add_test("Загрузка несуществующего файла", test_curriculum_load_nonexistent_file)
    runner.add_test("Работа с пустой базой данных", test_curriculum_empty_database)
    runner.add_test("Сортировка полного списка", test_curriculum_full_list_sorting)
    runner.add_test("Фильтрация по типу 'экзамен'", test_curriculum_by_report_type_exam)
    runner.add_test("Фильтрация по типу 'зачёт'", test_curriculum_by_report_type_credit)
    runner.add_test("Сортировка по виду отчётности", test_curriculum_by_report_type_sorting)
    runner.add_test("Фильтрация по диапазону часов", test_curriculum_by_hours_range)
    runner.add_test("Сортировка по диапазону часов", test_curriculum_by_hours_range_sorting)
    runner.add_test("Перестановка границ диапазона", test_curriculum_by_hours_range_swapped)
    runner.add_test("Получение уникальных кафедр", test_curriculum_unique_departments)

    # Тесты алгоритма сортировки
    runner.add_test("Бинарная сортировка: простой список", test_binary_insertion_sort_simple)
    runner.add_test("Бинарная сортировка: обратный порядок", test_binary_insertion_sort_reverse)
    runner.add_test("Бинарная сортировка: пустой список", test_binary_insertion_sort_empty)
    runner.add_test("Бинарная сортировка: один элемент", test_binary_insertion_sort_single)
    runner.add_test("Бинарная сортировка: дубликаты", test_binary_insertion_sort_duplicates)

    runner.run_all()


if __name__ == "__main__":
    main()
