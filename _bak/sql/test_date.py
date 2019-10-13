from datetime import datetime
from datetime import timedelta
from enum import Enum

# x = datetime.datetime.now()


class WeekDay(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


def strDateTime(x, format='%Y-%m-%d %H:%M:%S'):
    return x.strftime(format)


def strDate(x, format='%Y-%m-%d'):
    return x.strftime(format)



def getDay(x):
    return int(x.strftime('%d'))


def getMonth(x):
    return int(x.strftime('%m'))


def getYear(x):
    return int(x.strftime('%Y'))


# x = datetime(2020, 5, 17, 11, 59, 23)
# y = x + timedelta(days=7)
# print (y)
#
# print(x.year)
#
# print(x.month)
# print(x.day)
# print(strDate(x))
# print(strDateTime(x))


# 0 1 2 3 4 5 6
# 7 8 9 10111213
# M T W T F S S
#         1 2 3
# 4 5 6 7 8 9 10

def get_monthly_lesson_date(y, m, w):
    d = []
    first_day = datetime(y, m, 1)

    if w.value > first_day.weekday():
        first_day = first_day + timedelta(days=(w.value - first_day.weekday()))
    elif w.value < first_day.weekday():
        first_day = first_day + timedelta(days=(7 + w.value - first_day.weekday()))
    else:
        pass

    # print(first_day)
    while first_day.month == m:
        d.append(first_day)
        first_day = first_day + timedelta(days=7)

    return d


print(get_monthly_lesson_date(2019, 5, WeekDay.MON))
print(get_monthly_lesson_date(2019, 5, WeekDay.TUE))
print(get_monthly_lesson_date(2019, 5, WeekDay.WED))
print(get_monthly_lesson_date(2019, 5, WeekDay.THU))
print(get_monthly_lesson_date(2019, 5, WeekDay.FRI))
print(get_monthly_lesson_date(2019, 5, WeekDay.SAT))
print(get_monthly_lesson_date(2019, 5, WeekDay.SUN))
