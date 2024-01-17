# <---------- Local modules ---------->
from messages import ms_regular
from keyboards.kb_group import inline_homeworkApprove


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
	#### MarkdowV2 required!
	"""
	def __init__(self, line: str):
		self.quote = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'Неправильно записан день недели\!\n'
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
	#### MarkdowV2 required!
	"""
	def __init__(self, line: str):
		self.quote = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'Не указано название предмета\!\n'
		)


class InvalidLessonNumber(Exception):
	"""
	Triggered when invalid lesson number detected.
	Example: '1u. Алгебра'
	#### MarkdowV2 required!
	"""
	def __init__(self, line: str):
		self.quote = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'Неправильно указан номер урока\!\n'
		)


class NotSuitableLessonNumber(Exception):
	"""
	Raised when lesson number not in [0,11].
	Example: '40. Алгебра'
	#### MarkdowV2 required!
	"""
	def __init__(self, line: str):
		self.quote = line
		self.text = (
			f'Расписание не сохранено ❌\n'
			f'Номер урока не может быть меньше *0* или больше *10*\!\n'
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
		self.alt = (
			'Домашнее задание не сохранено ❌\n'
			'Вы пытаетесь записать задание на воскресенье? 😶‍🌫️'
		)


class NoTask(Exception):
	"""
	Raised when homework uploading message has less than 2 lines.
	"""
	def __init__(self):
		self.text = (
			'Домашнее задание не сохранено ❌\n'
			'Вы не указали никакого задания!'
		)
	

class NoMainSchedule(Exception):
	"""
	Raised when there is no Main Schedule set in group.
	"""
	def __init__(self):
		self.text = (
			'Домашнее задание не сохранено ❌\n'
			'В вашей группе не установлено основное расписание!\n'
			'Попросите <b>админа группы</b> сделать это 🛠️'
		)


class InvalidSubject(Exception):
	"""
	Raised when written subject is not in subjectEnum of MainSchedule.
	"""
	def __init__(self, subject_invalid: str, task: str, subject: str = None, weekday: str = None, date: str = None):
		"""
		Raised when written subject is not in subjectEnum of MainSchedule.
		"""
		self.subject_invalid = subject_invalid
		self.subject = subject
		self.task = task
		self.weekday = weekday
		self.date = date
		if subject is None:
			self.text = (
				'Домашнее задание не сохранено ❌\n'
				f'В расписании нет урока "{self.subject_invalid}"'
			)
			self.markup = None
		else:
			self.text = (
				f'В расписании нет урока "{self.subject_invalid}"\n'
				f'Может вы имели в виду "{self.subject}"?'
			)
			self.markup = inline_homeworkApprove


class InvalidDate(Exception):
	"""
	Raised when written date string can't be parsed.\n
	#### MarkdowV2 required!
	"""
	def __init__(self, date: str):
		"""
		Raised when written date string can't be parsed.\n
		#### MarkdowV2 required!
		"""
		self.quote = date
		self.text = (
			'Домашнее задание не сохранено ❌\n'
			'Вы неправильно указали дату сохранения\!\n'	
		)


class TimeTravel(Exception):
	"""
	Raised when written date is in past.
	"""
	def __init__(self, date: str):
		"""
		Raised when written date is in past.
		#### MarkdowV2 required!
		"""
		self.quote = date
		self.text = (
			'Домашнее задание не сохранено ❌\n'
			f'Вы не можете сохранить задание в прошлое\!\n'
		)


class NoLessonAtWeekday(Exception):
	"""
	Raised when there is no lesson of given subject at date provided.
	"""
	def __init__(self, weekday: str, subject: str):
		"""
		Raised when there is no lesson of given subject at date provided.
		#### MarkdowV2 required!
		"""
		self.text = (
			'Домашнее задание не сохранено ❌\n'
			f'У вас нет {subject.capitalize()} в {weekday.capitalize()}!\n'
		)


class NoSubject(Exception):
	"""
	Raised when no subject provided.\n 
	We pass that.
	"""