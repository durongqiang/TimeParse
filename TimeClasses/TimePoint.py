# -*- coding: utf-8 -*-

from config import TimeUnit, TimeType

class TimePoint:
    def __init__(self, year, month=None, day=None, weekday=None, hour=None, minute=None, second=None, originExpression=None):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.weekday = weekday
        self.isAccurateTo = ''
        self.whichFestival = None
        self.season = None


    def __str__(self):
        return ''


