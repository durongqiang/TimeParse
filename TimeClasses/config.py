# -*- coding: utf-8 -*-

from enum import Enum

TimeUnit = Enum('TimeUnit', 'year month day hour minute second week')
TimeType = Enum('TimeType', 'point interval')