# <---------- Python modules ---------->
from datetime import datetime
from dateutil.parser import parse
from dateutil.parser._parser import ParserError

# <---------- Local modules ---------->
from exceptions.ex_handlers import NotEnoughDays, InvalidWeekDay, \
	SundayException, NoLesson, InvalidLessonNumber, NotSuitableLessonNumber, \
	NoTask, NoMainSchedule, NoSubject, InvalidSubject, InvalidDate, TimeTravel
from messages import ms_regular
from data_base.operations import getMainSchedule
from difflib import SequenceMatcher


# <---------- Main handlers ---------->
async def ut_filterForMDV2(text: str) -> str:
	"""
	Formats the string to prevent MarkdownV2 from screwing everything up.
	:param text: Text for formatting
	:return: Formatted text
	"""
	for char in ms_regular.filter_chars:
		if char in text:
			text = text.replace(char, f'\{char}')
	return text


async def scheduleMessageToDict(text: str, mode: int) -> dict:
	"""
	Formats dict structure from text schedule.
	:param text: Schedule as String
	:param mode:
	:raises NotEnoughDays:
	:raises InvalidWeekDay:
	:raises SundayException:
	:return: Schedule as Dict
	"""
	result = {}
	data = text.split('\n')
	if mode == 0:
		weekday = None
		for num, line in enumerate(data):
			if num == 0:
				continue
			if line.replace(' ', '').lower() in ms_regular.weekdays:
				if line.lower() == 'воскресенье':
					raise SundayException
				weekday = line.capitalize()
				result[weekday] = {}
				for i in range(11):
					result[weekday][str(i)] = None
			elif line.replace(' ', '') != '':
				if weekday:
					if len(line.split()) < 2:
						raise NoLesson(num, line)
					else:
						lesson_num = line.split()[0].replace('.', '').replace(')', '')
						try:
							int(lesson_num)
						except:
							raise InvalidLessonNumber(num, line)
						if int(lesson_num) not in range(0, 11):
							raise NotSuitableLessonNumber(num, line)
						subject = " ".join([x for x in line.split()[1:]]).lower()
						if subject == '-':
							subject = None
						result[weekday][str(int(lesson_num))] = subject
				else:
					raise InvalidWeekDay(num, line)
		if len(result) < 5:
			raise NotEnoughDays	
	elif mode == 1:
		# print("Mode: 1", data)
		for num, line in enumerate(data):
			if line.replace(' ', '') != '':
				if len(line.split()) < 2:
					raise NoLesson(num, line)
				else:
					lesson_num = line.split()[0].replace('.', '').replace(')', '')
					try:
						int(lesson_num)
					except:
						raise InvalidLessonNumber(num, line)
					if int(lesson_num) not in range(0, 11):
						raise NotSuitableLessonNumber(num, line)
					subject = " ".join([x for x in line.split()[1:]]).lover()
					if subject == '-':
						subject = None
					result[str(int(lesson_num))] = subject
	else:
		raise ValueError('Mode can be [0,1]')
	return result


async def scheduleDictToMessage(schedule: dict, mode: int) -> str:
	"""
	Formats text from dict schedule.\n
	mode [0,1]:\n
	0) Working with whole schedule
	1) Working with one day schedule\n
	:param schedule: Schedule as Dict
	:param mode: 0,1
	:return: Schedule as String
	"""
	result = ''
	if mode == 0:
		for day in schedule:
			lesson_nums = [x for x in schedule[day] if schedule[day][x] is not None]
			for i, j in enumerate(lesson_nums):
				lesson_nums[i] = int(j)
			end = max(lesson_nums)
			result += f'<b>{day}</b>\n'
			for lesson in schedule[day]:
				if int(lesson) in range(0, end+1):
					subject = schedule[day][lesson]
					if lesson == '0' and subject is None:
						continue
					if subject is None:
						subject = '-'
					result += f' {lesson}. {subject.capitalize()}\n'
			result += '\n'
	elif mode == 1:
		for day in schedule:
			lesson_nums = map(int(), [x for x in schedule[day] if schedule[x] is not None])
			for i, j in enumerate(lesson_nums):
				lesson_nums[i] = int(j)
			end = max(lesson_nums)
			result += f'<b>{day}</b>\n'
			for lesson in schedule:
				if int(lesson) in range(0, end+1):
					subject = schedule[lesson]
					if lesson == '0' and subject is None:
						continue
					if subject is None:
						subject = '-'
					result += f' {lesson}. {subject}\n'
			result += '\n'
	else:
		raise ValueError('Mode can be [0,1]')
	return result


async def scheduleEnumSubjects(schedule: dict, mode: int) -> list[str]:
	"""
	Enumerates all subjects in schedule.\n
	mode [0,1]:\n
	0) Working with whole schedule
	1) Working with one day schedule\n
	Returns list of subjects in schedule.\n
	:param schedule:
	:param mode:
	:return: list
	"""
	result = []
	if mode == 0:
		for day in schedule:
			for lesson in schedule[day]:
				subject = schedule[day][lesson]
				if subject is not None and subject not in result:
					result.append(subject)
	elif mode == 1:
		for lesson in schedule:
			subject = schedule[lesson]
			if subject is not None and subject not in result:
				result.append(subject)
	else:
		raise ValueError('Mode can be [0,1]')
	return result


async def homeworkExtractData(id: int, text: str) -> tuple():
	"""
	Read users message and find 'subject', 'task', and 'weekday'/'date'.
	:param id: User id
	:param text: User message.text
	:return tuple: subject, task, weekday, date
	"""
	subject = None
	subject_invalid = None
	task = None
	weekday = None
	date = None

	first = text.split('\n')[0]
	if len(text.split('\n')) == 1:
		task = None
	else:
		task = "\n".join(text.split('\n')[1:])
	for w in ms_regular.hw_keywords:
		if w in first: first = first.replace(w, '')
	first = first.split()

	if len(first) == 0:
		raise NoSubject 

	standart_schedule = await getMainSchedule(id)
	# print(standart_schedule)
	if standart_schedule is None or standart_schedule == {}:
		raise NoMainSchedule
	subjects = await scheduleEnumSubjects(standart_schedule, 0)

	l = len(first)
	for i in range(l):
		subject = " ".join(first[:i+1]).lower()
		if subject in subjects:
			offset = i
			break
	else:
		max_similarity = 0
		best_subject = None
		for sub in subjects:
			sim = SequenceMatcher(None, sub, first[0].lower()).ratio()
			if sim > max_similarity:
				max_similarity = sim
				best_subject = sub
		subject = best_subject
		subject_invalid = first[0]

	if subject_invalid:
		raise InvalidSubject(
			subject_invalid = subject_invalid,
			task = task,
			subject = subject,
			weekday = weekday,
			date = date
		)

	if offset < l-1:
		if first[offset+1].lower() == 'воскресенье':
			raise SundayException()
		if first[offset+1].lower() in ms_regular.weekdays:
			weekday = first[offset+1]
		else:
			try:
				date = parse(first[offset+1])
				print(date.date(), datetime.now().date(), date.date() < datetime.now().date())
				if date.date() < datetime.now().date():
					raise TimeTravel(first[offset+1])
			except ParserError:
				raise InvalidDate(first[offset+1])

	return (subject, task, weekday, date)

