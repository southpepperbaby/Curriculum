"""
Модуль с пользовательскими исключениями для работы с дисциплинами.
"""


class DisciplineException(Exception):
    """Базовое исключение для ошибок, связанных с дисциплинами."""
    pass


class InvalidSemesterError(DisciplineException):
    """Исключение для некорректного номера семестра."""

    def __init__(self, semester, message=None):
        if message is None:
            message = f"Некорректный номер семестра: {semester}. Допустимые значения: 1-8."
        super().__init__(message)
        self.semester = semester


class InvalidDurationError(DisciplineException):
    """Исключение для некорректной продолжительности курса."""

    def __init__(self, duration, semester=None, message=None):
        if message is None:
            if semester:
                max_duration = 9 - semester
                message = (f"Некорректная продолжительность курса: {duration}. "
                          f"Для семестра {semester} максимальная продолжительность: {max_duration}.")
            else:
                message = f"Некорректная продолжительность курса: {duration}."
        super().__init__(message)
        self.duration = duration


class InvalidHoursError(DisciplineException):
    """Исключение для некорректного количества часов."""

    def __init__(self, hours, message=None):
        if message is None:
            message = f"Некорректное количество часов: {hours}. Допустимые значения: 36-216."
        super().__init__(message)
        self.hours = hours


class InvalidReportTypeError(DisciplineException):
    """Исключение для некорректного вида отчётности."""

    def __init__(self, report_type, message=None):
        if message is None:
            message = f"Некорректный вид отчётности: '{report_type}'. Допустимые значения: 'зачёт', 'экзамен'."
        super().__init__(message)
        self.report_type = report_type


class FileOperationError(DisciplineException):
    """Исключение для ошибок работы с файлами."""

    def __init__(self, filename, operation, message=None):
        if message is None:
            message = f"Ошибка при {operation} файла: {filename}"
        super().__init__(message)
        self.filename = filename
        self.operation = operation


class EmptyDatabaseError(DisciplineException):
    """Исключение для пустой базы данных."""

    def __init__(self, message=None):
        if message is None:
            message = "База данных пуста. Сначала загрузите данные из файла."
        super().__init__(message)
