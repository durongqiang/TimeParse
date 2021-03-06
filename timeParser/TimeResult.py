# -*- coding: utf-8 -*-

import json
from datetime import datetime

from .TimePoint import TimePoint


class TimeResult:
    year, month, day, hour, minute, second = None, None, None, None, None, None
    # isAccurateTo不同整数值代表0：year，1：month，2：day，3：hour, 4:minute,5:second,6:isweek None:isvaildday
    isAccurateTo = None
    # 判断TimeResult的值的类型，初始化时，均为False
    isTimePoint, isTimeInterval = False, False
    attr = "TimeResult"
    # 构造函数，存在两种情况，进行构造

    singleTimePoint = TimePoint()
    # start and end 均为时间点
    startTimePoint, endTimePoint = TimePoint(), TimePoint()

    def __init__(self, tu=None, tp1=None, tp2=None, isWeek=None):
        # 采用list进行初始化,后接参数isWeek进行判断是否是周
        if tu is not None and isWeek is not None:
            # 设置长度为6的存储单元
            time_unit = [None, None, None, None, None, None]
            # tu赋值到time_unit单元内
            for i in range(0, len(tu)):
                if tu[i] == -1:
                    break
                time_unit[i] = tu[i]
                # 进行精确位置设置
            if isWeek:
                self.isAccurateTo = 6
            else:
                self.isAccurateTo = i
            # 初始化年、月、日，时、分、秒
            self.year, self.month, self.day = time_unit[0], time_unit[1], time_unit[2]
            self.hour, self.minute, self.second = time_unit[3], time_unit[4], time_unit[5]
            if not self.__isValidDate():
                self.isAccurateTo = None
            # 类型为单个点的类型
            self.singleTimePoint = TimePoint(tu=tu, isWeek=isWeek)
            self.isTimePoint = True

            # 第二种情况，两个时间点的数据类型
        if tp1 is not None and tp2 is not None:  # TO-DO: tp1 时间必须在 tp2 之前
            self.startTimePoint = TimePoint(tp=tp1)
            self.endTimePoint = TimePoint(tp=tp2)
            self.isTimeInterval = True

            # 第三种情况，传入的参数仅一个时间点
        if tp1 is not None and tp2 is None:
            if tu.year is not None:
                self.year, self.month, self.day = tp1.year, tp1.month, tp1.day
                self.hour, self.minute, self.second = tp1.hour, tp1.minute, tp1.second
                self.isAccurateTo = tp1.isAccurateTo
                self.singleTimePoint = TimePoint(tp=tp1)
                self.isTimePoint = True

    # 判断值是否时有效的，类似于TimePointa,是一个内部方法，外部并不会使用，故不存在逻辑问题
    def __isValidDate(self):
        if self.year is None:
            # print("This is a empty TimeResult.")
            return True
        if self.year is not None:
            if self.year < 0:
                return False
            else:
                if self.month is None:
                    return True
                if self.month is not None:
                    if self.month > 12 or self.month < 0:
                        return False
        if self.day is None:
            return True
        try:
            if self.second is not None:
                datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
            else:
                if self.minute is not None:
                    datetime(self.year, self.month, self.day, self.hour, self.minute)
                else:
                    if self.hour is not None:
                        datetime(self.year, self.month, self.day, self.hour)
                    else:
                        datetime(self.year, self.month, self.day)

        except:
            return False

        return True

    # 将该类型转换成string类型
    def toString(self):
        if self.isTimePoint:
            return self.singleTimePoint.toString()
        if self.isTimeInterval:
            return self.startTimePoint.toString() + " ->>>>- " + self.endTimePoint.toString()
        return "IS.. NULL"

    def toDict(self):
        if self.isTimePoint:
            return self.singleTimePoint.toDict()
        elif self.isTimeInterval:
            res = dict()
            res['startTime'] = self.startTimePoint.toDict()
            res['endTime'] = self.endTimePoint.toDict()
            return res
        # 需要确认一下结果的地方
        return json.dumps("Not a time point")

    # 将该类型转换成Json数据类型
    def toJson(self):
        if self.isTimePoint:
            return self.singleTimePoint.toJson()
        elif self.isTimeInterval:
            res = ""
            res = res + "[" + self.startTimePoint.toJson() + ","
            res = res + self.endTimePoint.toJson() + "]"
            return res
        ###需要确认一下结果的地方
        return json.dumps("Not a time point")

    # 将该类型存储转换为list<string>类型
    def toStringList(self):
        res = []
        if self.isTimePoint:
            res.append(self.singleTimePoint.toString())
            return res
        elif self.isTimeInterval:
            res.append(self.startTimePoint.toString())
            res.append('到')
            res.append(self.endTimePoint.toString())
            return res
        else:
            return ['Is.. NULL']

    # 进行代码重构，把TimeResult转换为TimePoint
    def toTimePoint(self):
        if self.isTimePoint:
            result = TimePoint()
            result.year, result.month, result.day = self.year, self.month, self.day
            result.hour, result.minute, result.second = self.hour, self.minute, self.second
            result.isAccurateTo = self.isAccurateTo
            return result
        else:
            raise IOError("IllegalArgumentException")

    def isFestival(self):
        if self.isTimePoint:
            return self.singleTimePoint.isFestival()
        else:
            return None
