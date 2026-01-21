"""
Модуль с классом Curriculum для управления учебным планом.
Содержит логику загрузки данных, сортировки и формирования отчётов.
"""

import json
from Discipline import Discipline
from DisciplineException import (
    FileOperationError,
    EmptyDatabaseError,
    DisciplineException
)


class Curriculum:
    """
    Класс для управления учебным планом.

    Реализует загрузку данных из JSON-файла, сортировку бинарными вставками
    и формирование отчётов по различным критериям.
    """

    def __init__(self):
        """Инициализация пустого учебного плана."""
        self.disciplines = []

    def load_from_file(self, filename):
        """
        Загрузка данных о дисциплинах из JSON-файла.

        Args:
            filename: Путь к файлу с данными

        Raises:
            FileOperationError: При ошибке чтения файла
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            raise FileOperationError(filename, "чтении",
                                    f"Файл '{filename}' не найден.")
        except json.JSONDecodeError:
            raise FileOperationError(filename, "чтении",
                                    f"Файл '{filename}' содержит некорректный JSON.")
        except PermissionError:
            raise FileOperationError(filename, "чтении",
                                    f"Нет прав доступа к файлу '{filename}'.")

        self.disciplines = []
        errors = []

        for i, item in enumerate(data, 1):
            try:
                discipline = Discipline.from_dict(item)
                self.disciplines.append(discipline)
            except DisciplineException as e:
                errors.append(f"Запись {i}: {e}")

        if errors:
            print("\nПредупреждения при загрузке:")
            for error in errors:
                print(f"  - {error}")

        print(f"\nУспешно загружено дисциплин: {len(self.disciplines)}")

    def _check_not_empty(self):
        """Проверка, что база данных не пуста."""
        if not self.disciplines:
            raise EmptyDatabaseError()

    # ========================================================================
    # СОРТИРОВКА БИНАРНЫМИ ВСТАВКАМИ
    # ========================================================================

    def _binary_search_insert_position(self, sorted_list, element, key_func):
        """
        Бинарный поиск позиции для вставки элемента в отсортированный список.

        Алгоритм:
        1. Устанавливаем границы поиска: left=0, right=len(sorted_list)
        2. Пока left < right:
           - Находим середину: mid = (left + right) // 2
           - Сравниваем ключ элемента в середине с ключом вставляемого элемента
           - Если ключ в середине меньше, сдвигаем левую границу: left = mid + 1
           - Иначе сдвигаем правую границу: right = mid
        3. Возвращаем left - это позиция для вставки

        Args:
            sorted_list: Уже отсортированная часть списка
            element: Элемент для вставки
            key_func: Функция получения ключа сортировки

        Returns:
            int: Индекс позиции для вставки
        """
        left = 0
        right = len(sorted_list)
        element_key = key_func(element)

        while left < right:
            mid = (left + right) // 2
            if key_func(sorted_list[mid]) < element_key:
                left = mid + 1
            else:
                right = mid

        return left

    def _binary_insertion_sort(self, items, key_func):
        """
        Сортировка бинарными вставками.

        Алгоритм:
        1. Создаём пустой результирующий список
        2. Для каждого элемента исходного списка:
           - Находим позицию для вставки с помощью бинарного поиска
           - Вставляем элемент в найденную позицию
        3. Возвращаем отсортированный список

        Сложность: O(n^2) по времени (из-за вставок), O(n) по памяти
        Бинарный поиск ускоряет нахождение позиции до O(log n),
        но сама вставка остаётся O(n).

        Args:
            items: Список элементов для сортировки
            key_func: Функция получения ключа сортировки

        Returns:
            list: Новый отсортированный список
        """
        sorted_list = []

        for element in items:
            # Находим позицию для вставки методом бинарного поиска
            position = self._binary_search_insert_position(sorted_list, element, key_func)
            # Вставляем элемент в найденную позицию
            sorted_list.insert(position, element)

        return sorted_list

    # ========================================================================
    # ОТЧЁТ 1: Полный список всех дисциплин
    # Сортировка: семестр (возрастание) + кафедра (возрастание) + часы (убывание)
    # ========================================================================

    def get_full_list_sorted(self):
        """
        Получить полный список дисциплин, отсортированный по составному ключу:
        1. Семестр начала (по возрастанию)
        2. Кафедра (по возрастанию, лексикографически)
        3. Количество часов (по убыванию)

        Returns:
            list: Отсортированный список дисциплин
        """
        self._check_not_empty()

        def sort_key(discipline):
            # Для сортировки часов по убыванию используем отрицательное значение
            return (discipline.semester, discipline.department, -discipline.hours)

        return self._binary_insertion_sort(self.disciplines, sort_key)

    # ========================================================================
    # ОТЧЁТ 2: Список дисциплин с заданным видом отчётности
    # Сортировка: продолжительность курса (возрастание) + часы (убывание)
    # ========================================================================

    def get_by_report_type(self, report_type):
        """
        Получить список дисциплин с заданным видом отчётности.

        Args:
            report_type: Вид отчётности ('зачёт' или 'экзамен')

        Returns:
            list: Отфильтрованный и отсортированный список дисциплин
        """
        self._check_not_empty()

        report_type = report_type.strip().lower()
        if report_type not in ('зачёт', 'экзамен'):
            print(f"Предупреждение: '{report_type}' - некорректный вид отчётности.")
            print("Допустимые значения: 'зачёт', 'экзамен'")
            return []

        # Фильтрация по виду отчётности
        filtered = [d for d in self.disciplines if d.report_type == report_type]

        if not filtered:
            return []

        def sort_key(discipline):
            # Продолжительность по возрастанию, часы по убыванию
            return (discipline.duration, -discipline.hours)

        return self._binary_insertion_sort(filtered, sort_key)

    # ========================================================================
    # ОТЧЁТ 3: Список дисциплин с часами в диапазоне [N1, N2]
    # Сортировка: кафедра (возрастание) + часы (убывание)
    # ========================================================================

    def get_by_hours_range(self, min_hours, max_hours):
        """
        Получить список дисциплин с количеством часов в заданном диапазоне.

        Args:
            min_hours: Минимальное количество часов (N1)
            max_hours: Максимальное количество часов (N2)

        Returns:
            list: Отфильтрованный и отсортированный список дисциплин
        """
        self._check_not_empty()

        if min_hours > max_hours:
            min_hours, max_hours = max_hours, min_hours
            print(f"Предупреждение: границы диапазона были переставлены местами.")

        # Фильтрация по диапазону часов
        filtered = [d for d in self.disciplines
                   if min_hours <= d.hours <= max_hours]

        if not filtered:
            return []

        def sort_key(discipline):
            # Кафедра по возрастанию, часы по убыванию
            return (discipline.department, -discipline.hours)

        return self._binary_insertion_sort(filtered, sort_key)

    # ========================================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ========================================================================

    def get_disciplines_count(self):
        """Получить количество загруженных дисциплин."""
        return len(self.disciplines)

    def get_unique_departments(self):
        """Получить список уникальных кафедр."""
        return sorted(set(d.department for d in self.disciplines))

    def get_unique_report_types(self):
        """Получить список уникальных видов отчётности."""
        return sorted(set(d.report_type for d in self.disciplines))

    def get_all_discipline_names(self):
        """Получить список названий всех дисциплин (отсортированный по алфавиту)."""
        return sorted(d.name for d in self.disciplines)
