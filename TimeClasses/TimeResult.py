# -*- coding: utf-8 -*-

from config import TimeUnit, TimeType
from TimePoint import TimePoint

class TimeResult:
    def __init__(self, value, type=TimeType.point):
        self.type = type
        if type == TimeType.point:
            self.timePoint = value
        elif type == TimeType.interval:
            self.timeInterval = value


    def __str__(self):
        return ''


