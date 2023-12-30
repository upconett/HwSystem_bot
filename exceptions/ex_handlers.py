class NotEnoughDays(Exception):
    """
    Triggered when there is less than 5 days in schedule.
    """
    pass


class InvalidWeekDay(Exception):
    """
    Triggered when invalid weekday name detected.
    Example: 'пондельник'
    """
    def __init__(self, num:int, line:str):
        self.num = num
        self.line = line


# class InvalidLesson(Exception):
#     """
#     Triggered when invalid lesson detected.
#     Example: '1. алгеьа'
#     """
#     def __init__(self, num:int, line:str):
#         """
#         Triggered when invalid lesson detected.
#         Example: '1. алгеьа'
#         """
#         self.num = num
#         self.line = line


class NoLesson(Exception):
    """
    Triggered when no lesson detected.
    Example: '2. '
    """
    def __init__(self, num:int, line:str):
        """
        Triggered when no lesson detected.
        Example: '2. '
        """
        self.num = num
        self.line = line

    
class InvalidLessonNumber(Exception):
    """
    Triggered when invalid lesson number detected.
    Example: '1u. Алгебра'
    """
    def __init__(self, num:int, line:str):
        """
        Triggered when invalid lesson number detected.
        Example: '1u. Алгебра'
        """
        self.num = num
        self.line = line


class NotSuitableLessonNumber(Exception):
    """
    Raised when lesson number not in [0,11].
    Example: '40. Алгебра'
    """
    def __init__(self, num:int, line:str):
        """
        Raised when lesson number not in [0,11].
        Example: '40. Алгебра'
        """
        self.num = num
        self.line = line


class SundayException(Exception):
    """
    Triggered if someone enters 'воскресенье' in schedule.\n
    We will use it because why the frick would somebody have lessons on sundays?!
    """
    pass