#Date and time operations
"""A data in Python is not a data type of its own
but we can import a module named datetime to 
work with dates as date objects"""



# Import the datetime module and display the current date:
import datetime
x = datetime.datetime.now()
print(x)
print(x.year)
print(x.strftime("%A"))
#output: 
# 2026-xx-xx xx:xx:xx.xxxxx
# 2026
# Saturday

"""To create a date, we can use the datetime()
class(constructor) of the datetime module"""
x = datetime.datetime(2020,5,17)
print(x)


"""The strftime() Method
the mathod called strftime(), 
and takes one parameter, format, 
to specify the format of the returned string:"""

x = datetime.datetime(2018,6,1)
print(x.strftime("%B"))
"""
%a - Weekday, short version 
%w - weekday as a num 0-6, 0 is Sunday
%A - Weekday, full version
%B - MONTH full
%b - month short
%m - month as a num 01-12
%d - day of month 01- 31
%y	Year, short version, without century	18	
%Y	Year, full version	2018	
%H	Hour 00-23	17	
%I	Hour 00-12	05	
%p	AM/PM	PM	
%M	Minute 00-59	41	
%S	Second 00-59	08	
%f	Microsecond 000000-999999	548513	
%z	UTC offset	+0100	
%Z	Timezone	CST	
%j	Day number of year 001-366	365	
%U	Week number of year, Sunday as the first day of week, 00-53	52	
%W	Week number of year, Monday as the first day of week, 00-53	52	
%c	Local version of date and time	Mon Dec 31 17:41:00 2018	
%C	Century	20	
%x	Local version of date	12/31/18	
%X	Local version of time	17:41:00	
%%	A % character	%	
%G	ISO 8601 year	2018	
%u	ISO 8601 weekday (1-7)	1	
%V	ISO 8601 weeknumber (01-53)	01	
"""

#1
from datetime import datetime, timedelta

current_date = datetime.now()
new_date = current_date - timedelta(days=5)

print("Current date:", current_date)
print("5 days ago:", new_date)

#2
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

#3
from datetime import datetime

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("Original:", now)
print("Without microseconds:", without_microseconds)

#4
from datetime import datetime

date1 = datetime(2024, 1, 1, 12, 0, 0)
date2 = datetime(2024, 1, 2, 12, 0, 0)

difference = date2 - date1

print("Difference in seconds:", difference.total_seconds())

