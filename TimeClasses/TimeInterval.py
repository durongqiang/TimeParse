# -*- coding: utf-8 -*-

from config import TimeUnit, TimeType

class TimeInterval:
    def __init__(self, startTimePoint, endTimePoint):
        self.startTime = startTimePoint
        self.endTime = endTimePoint
        self.whichFestival = None
        self.season = None


    def __str__(self):
        return ''


