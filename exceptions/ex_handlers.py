# <---------- Local modules ---------->
from messages import ms_regular


# <---------- Exception classes ---------->
class NotEnoughDays(Exception):
	"""
	Triggered when there is less than 5 days in schedule.
	"""
	def __init__(self):
		self.text = (
			'Расписание не сохранено ❌\n'
			'В расписании должно быть не менее <b>5 дней</b>!\n'
		)


class InvalidWeekDay(Exception):
	"""
	Triggered when invalid weekday name detected.
	Example: 'пондельник'
	"""
	def __init__(self, num: int, line: str):
		self.num = num
		for char in ms_regular.filter_chars:
			if char in line:
				line = line.replace(char, f'\{char}')
		self.line = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'В строке *№{self.num}* неправильно записан день недели\!\n'
			f'> {self.line}'
		)


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
	def __init__(self, num: int, line: str):
		self.num = num
		for char in ms_regular.filter_chars:
			if char in line:
				line = line.replace(char, f'\{char}')
		self.line = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'В строке *№{self.num}* не указано название предмета\!\n'
			f'> {self.line}'
		)


class InvalidLessonNumber(Exception):
	"""
	Triggered when invalid lesson number detected.
	Example: '1u. Алгебра'
	"""
	def __init__(self, num: int, line: str):
		self.num = num
		for char in ms_regular.filter_chars:
			if char in line:
				line = line.replace(char, f'\{char}')
		self.line = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'В строке *№{self.num}* неправильно указан номер урока\!\n'
			f'> {self.line}'
		)


class NotSuitableLessonNumber(Exception):
	"""
	Raised when lesson number not in [0,11].
	Example: '40. Алгебра'
	"""
	def __init__(self, num: int, line: str):
		self.num = num
		for char in ms_regular.filter_chars:
			if char in line:
				line = line.replace(char, f'\{char}')
		self.line = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'Ошибка в строке *№{self.num}*\n'
			f'Номер урока не может быть меньше *0* или больше *10*\!\n'
			f'> {self.line}'
		)
		self.exc = 'Not suitable lesson number at line {exception.num}.'


class SundayException(Exception):
	"""
	Triggered if someone enters 'воскресенье' in schedule.\n
	We will use it because why the frick would somebody have lessons on sundays?!
	"""
	def __init__(self):
		self.text = (
			'Расписание не сохранено ❌\n'
			'Вы что учитесь по воскресеньям? 😶‍🌫️\n'
			'Если и правда так, <a href="https://t.me/SteePT">напишите нам</a>, мы всё исправим!\n'
		)
