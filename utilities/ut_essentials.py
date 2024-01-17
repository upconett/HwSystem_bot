# <---------- Python modules ---------->
from datetime import datetime


# <---------- Functions ---------->
def dateToday(date: datetime = None) -> datetime:
	"""
	Returns datetime object with the time set to zero.
	"""
	if date:
		return date.replace(
			hour=0,
			minute=0,
			second=0,
			microsecond=0
		)
	else:
		return datetime.now().replace(
			hour=0,
			minute=0,
			second=0,
			microsecond=0
		)