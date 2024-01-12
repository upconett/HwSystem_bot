# <---------- Python modules ---------->
from aiogram import types
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.parser._parser import ParserError

# <---------- Local modules ---------->
from exceptions.ex_handlers import NotEnoughDays, InvalidWeekDay, \
	SundayException, NoLesson, InvalidLessonNumber, NotSuitableLessonNumber, \
	NoTask, NoMainSchedule, NoSubject, InvalidSubject, InvalidDate, TimeTravel
from messages import ms_regular
from data_base.operations import getMainSchedule, findNextLesson
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


def quotate(message: types.Message, quote: str):
	return types.ReplyParameters(
		message_id=message.message_id,
		chat_id=message.chat.id,
		quote=quote
	)


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
						raise NoLesson(line)
					else:
						lesson_num = line.split()[0].replace('.', '').replace(')', '')
						try:
							int(lesson_num)
						except:
							raise InvalidLessonNumber(line)
						if int(lesson_num) not in range(0, 11):
							raise NotSuitableLessonNumber(line)
						subject = " ".join([x for x in line.split()[1:]]).lower()
						if subject == '-':
							subject = None
						result[weekday][str(int(lesson_num))] = subject
				else:
					raise InvalidWeekDay(line)
		if len(result) < 5:
			raise NotEnoughDays	
	elif mode == 1:
		# print("Mode: 1", data)
		for num, line in enumerate(data):
			if line.replace(' ', '') != '':
				if len(line.split()) < 2:
					raise NoLesson(line)
				else:
					lesson_num = line.split()[0].replace('.', '').replace(')', '')
					try:
						int(lesson_num)
					except:
						raise InvalidLessonNumber(line)
					if int(lesson_num) not in range(0, 11):
						raise NotSuitableLessonNumber(line)
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


async def homeworkExtractDataUpload(id: int, text: str) -> tuple():
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

	first = text.split('\n')[0].lower()
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
	if standart_schedule is None or standart_schedule == {}:
		raise NoMainSchedule
	subjects = await scheduleEnumSubjects(standart_schedule, 0)

	for word in first:
		if word.lower() == 'воскресенье':
			raise SundayException()
		if word.lower() in ms_regular.weekdays:
			weekday = word.lower()
		else:
			try:
				date = parse(word, dayfirst=True)
				if date.date() < datetime.now().date():
					raise TimeTravel(word)
			except ParserError:
				pass
				# raise InvalidDate(word)
				
	l = len(first)
	for i in range(l):
		subject = " ".join(first[:i+1]).lower()
		offset = i
		if subject in subjects:
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

	return (subject, task, weekday, date)


async def homeworkExtractDataShow(id: int, text: str) -> datetime:
	date = None
	text = text.lower()
	for f in ms_regular.homeworkShow:
		if f in text:
			text = text.replace(f, '')
	text = text.replace(' ', '')
	if text in ms_regular.weekdays:
		current_wd = datetime.now().weekday()
		input_wd = ms_regular.weekdays.index(text)
		if input_wd == current_wd:
			date = datetime.now()
		elif input_wd > current_wd:
			date = datetime.now() + timedelta(days=(input_wd-current_wd))
		else:
			date = datetime.now() + timedelta(days=((6-current_wd)+(input_wd+1)))
	elif text in ms_regular.weekdays_smol:
		current_wd = datetime.now().weekday()
		input_wd = ms_regular.weekdays_smol.index(text)
		if input_wd == current_wd:
			date = datetime.now()
		elif input_wd > current_wd:
			date = datetime.now() + timedelta(days=(input_wd-current_wd))
		else:
			date = datetime.now() + timedelta(days=((6-current_wd)+(input_wd+1)))
	else:			
		try:
			date = parse(text, dayfirst=True)
		except ParserError:
			raise InvalidDate(text)
	return date