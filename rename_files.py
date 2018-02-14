#!/usr/bin/python

import string
from datetime import datetime

if __name__ == '__main__':
	now = datetime.now()
	year = str(now.year)
	month = str(now.month)
	month = month.zfill(2)
	day = str(now.day)
	day = day.zfill(2)
	hour = str(now.hour)
	hour = hour.zfill(2)
	minute = str(now.minute)
	minute = minute.zfill(2)
	second = str(now.second)
	second = second.zfill(2)
	microsecond = str(now.microsecond)
	microsecond = microsecond.zfill(7)
	
	print year + month + day + hour + minute + second + microsecond
