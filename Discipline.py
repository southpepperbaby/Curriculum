"""
Модуль с классом Discipline для представления учебной дисциплины.
"""

from DisciplineException import (
    InvalidSemesterError,
    InvalidDurationError,
    InvalidHoursError,
    InvalidReportTypeError,
    DisciplineException
)


class Discipline:
    """
    Класс, представляющий учебную дисциплину.

    Атрибуты:
        name (str): Название дисциплины
        semester (int): Номер семестра, с которого начинается изучение (1-8)
        duration (int): Продолжительность курса в семестрах
        hours (int): Общее количество часов (36-216)
        report_type (str): Вид отчётности ('зачёт' или 'экзамен')
        department (str): Название кафедры, читающей курс
    """

    VALID_REPORT_TYPES = ('зачёт', 'экзамен')
    MIN_SEMESTER = 1
    MAX_SEMESTER = 8
    MIN_HOURS = 36
    MAX_HOURS = 216

    def __init__(self, name, semester, duration, hours, report_type, department):
        """
        Инициализация объекта дисциплины.

        Args:
            name: Название дисциплины
            semester: Номер семестра начала изучения
            duration: Продолжительность курса в семестрах
            hours: Общее количество часов
            report_type: Вид отчётности
            department: Кафедра

        Raises:
            InvalidSemesterError: Если семестр вне диапазона 1-8
            InvalidDurationError: Если продолжительность некорректна
            InvalidHoursError: Если часы вне диапазона 36-216
            InvalidReportTypeError: Если вид отчётности не 'зачёт'/'экзамен'
        """
        self.name = self._validate_name(name)
        self.semester = self._validate_semester(semester)
        self.duration = self._validate_duration(duration, self.semester)
        self.hours = self._validate_hours(hours)
        self.report_type = self._validate_report_type(report_type)
        self.department = self._validate_department(department)

    def _validate_name(self, name):
        """Валидация названия дисциплины."""
        name = str(name).strip()
        if not name:
            raise DisciplineException("Название дисциплины не может быть пустым.")
        return name

    def _validate_department(self, department):
        """Валидация названия кафедры."""
        department = str(department).strip()
        if not department:
            raise DisciplineException("Название кафедры не может быть пустым.")
        return department

    def _validate_semester(self, semester):
        """Валидация номера семестра."""
        try:
            semester = int(semester)
        except (ValueError, TypeError):
            raise InvalidSemesterError(semester)

        if not (self.MIN_SEMESTER <= semester <= self.MAX_SEMESTER):
            raise InvalidSemesterError(semester)
        return semester

    def _validate_duration(self, duration, semester):
        """Валидация продолжительности курса."""
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            raise InvalidDurationError(duration)

        max_duration = self.MAX_SEMESTER - semester + 1
        if not (1 <= duration <= max_duration):
            raise InvalidDurationError(duration, semester)
        return duration

    def _validate_hours(self, hours):
        """Валидация количества часов."""
        try:
            hours = int(hours)
        except (ValueError, TypeError):
            raise InvalidHoursError(hours)

        if not (self.MIN_HOURS <= hours <= self.MAX_HOURS):
            raise InvalidHoursError(hours)
        return hours

    def _validate_report_type(self, report_type):
        """Валидация вида отчётности."""
        report_type = str(report_type).strip().lower()
        if report_type not in self.VALID_REPORT_TYPES:
            raise InvalidReportTypeError(report_type)
        return report_type

    def to_dict(self):
        """Преобразование объекта в словарь для сохранения в JSON."""
        return {
            'name': self.name,
            'semester': self.semester,
            'duration': self.duration,
            'hours': self.hours,
            'report_type': self.report_type,
            'department': self.department
        }

    @classmethod
    def from_dict(cls, data):
        """
        Создание объекта Discipline из словаря.

        Args:
            data: Словарь с данными дисциплины

        Returns:
            Discipline: Новый объект дисциплины

        Raises:
            DisciplineException: Если отсутствует обязательное поле
        """
        required_keys = ['name', 'semester', 'duration', 'hours', 'report_type', 'department']
        for key in required_keys:
            if key not in data:
                raise DisciplineException(f"Отсутствует обязательное поле: '{key}'")

        return cls(
            name=data['name'],
            semester=data['semester'],
            duration=data['duration'],
            hours=data['hours'],
            report_type=data['report_type'],
            department=data['department']
        )

    def __str__(self):
        """Строковое представление для вывода в консоль."""
        return (f"{self.name} | Семестр: {self.semester} | "
                f"Длительность: {self.duration} сем. | Часы: {self.hours} | "
                f"Отчётность: {self.report_type} | Кафедра: {self.department}")

    def __repr__(self):
        """Представление для отладки."""
        return (f"Discipline(name='{self.name}', semester={self.semester}, "
                f"duration={self.duration}, hours={self.hours}, "
                f"report_type='{self.report_type}', department='{self.department}')")
