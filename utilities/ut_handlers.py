# <---------- Импорт сторонних функций ---------->
from json import dumps


# <---------- Импорт локальных функций ---------->
from exceptions.ex_handlers import NotEnoughDays, InvalidWeekDay,\
	SundayException, NoLesson, InvalidLessonNumber, NotSuitableLessonNumber #InvalidLesson


# <---------- Константы ---------->
valid_days = [
	'понедельник', 'вторник', 'среда', 'четверг', 
	'пятница', 'суббота', 'воскресенье'
	]
# valid_lessons = [
	# 'алгебра', 'геометрия', 'русский', 'английский', 
	# 'литература', 'биология', 'вероятность', 'география',
	# 'информатика', 'история', 'обж', 'обществознание',
	# 'физика', 'физкультура', 'химия'
	# ]
filter_chars = r'/.,!;:@#$%^&*()-_=+{[]}`~<>?'


# <---------- Основные функции ---------->
async def ut_filterForMDV2(text:str) -> str:
	"""
	Formats the string to prevent MarkdownV2 from screving everything up.
	:param text: Text for formatting 
	:return: Formatted text
	"""
	for char in filter_chars:
		if char in text:
			text = text.replace(char, f'\{char}')
	return text
	

async def ut_ScheduleMessageToDict(text:str, mode:int) -> dict:
	"""
	Formats dict structure from text schedule.
	:param text: Schedule as String
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
			if num == 0: continue
			if line.replace(' ','').lower() in valid_days:
				if line.lower() == 'воскресенье':
					raise SundayException
				weekday = line.capitalize()
				result[weekday] = {}
				for i in range(11):
					result[weekday][str(i)] = {'subject': None}
			elif line.replace(' ', '') != '':
				if weekday:
					if len(line.split()) < 2:
						raise NoLesson(num, line)
					else:
						lesson_num = line.split()[0].replace('.', '').replace(')', '')
						try: int(lesson_num)
						except: raise InvalidLessonNumber(num, line)
						if int(lesson_num) not in range(0,11):
							raise NotSuitableLessonNumber(num, line)
						subject = " ".join([x for x in line.split()[1:]])
						result[weekday][str(int(lesson_num))]['subject'] = subject
				else:
					raise InvalidWeekDay(num, line)
		if len(result) < 5:
			raise NotEnoughDays	
	elif mode == 1:
		print("Mode: 1", data)
		for num, line in enumerate(data):
			if line.replace(' ', '') != '':
				if len(line.split()) < 2:
					raise NoLesson(num, line)
				else:
					lesson_num = line.split()[0].replace('.', '').replace(')', '')
					try: int(lesson_num)
					except: raise InvalidLessonNumber(num, line)
					if int(lesson_num) not in range(0,11):
						raise NotSuitableLessonNumber(num, line)
					subject = " ".join([x for x in line.split()[1:]])
					result[str(int(lesson_num))] = {'subject': subject}
	else:
		raise ValueError('Mode can be [0,1]')
	return result


async def ut_ScheduleDictToMessage(schedule:dict, mode:int) -> str:
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
			lesson_nums = [x for x in schedule[day] if schedule[day][x]['subject'] is not None]
			for i, j in enumerate(lesson_nums): lesson_nums[i] = int(j)
			end = max(lesson_nums)
			result += f'<b>{day}</b>\n'
			for lesson in schedule[day]:
				if int(lesson) in range(0, end+1):
					subject = schedule[day][lesson]['subject']
					if lesson == '0' and subject is None:
						continue
					if subject is None:
						subject = '-'
					result += f' {lesson}. {subject}\n'
			result += '\n'
	elif mode == 1:
		lesson_nums = map(int(), [x for x in schedule[day] if schedule[x]['subject'] is not None])
		for i, j in enumerate(lesson_nums): lesson_nums[i] = int(j)
		end = max(lesson_nums)
		result += f'<b>{day}</b>\n'
		for lesson in schedule:
			if int(lesson) in range(0, end+1):
				subject = schedule[lesson]['subject']
				if lesson == '0' and subject is None:
					continue
				if subject is None:
					subject = '-'
				result += f' {lesson}. {subject}\n'
		result += '\n'
	else: raise ValueError('Mode can be [0,1]')
	return result


async def ut_ScheduleEnumSubjects(schedule:dict, mode:int) -> list[str]:
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
				subject = schedule[day][lesson]['subject']
				if subject is not None and subject not in result:
					result.append(subject)
	elif mode == 1:
		for lesson in schedule:
			subject = schedule[lesson]['subject']
			if subject is not None and subject not in result:
				result.append(subject)
	else: raise ValueError('Mode can be [0,1]')
	return result
