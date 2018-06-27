# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from timeParser.LunarSolarConverter import Solar, LunarSolarConverter
from timeParser.get_file_path import read_festival_regex

def get_festival_dict():
    res = read_festival_regex()
    Solar_Festival = {}
    Lunar_Festival = {}
    for each in res:
        if 'isLunar' in each:
            Lunar_Festival['{0}-{1}'.format(each['month'],each['day'])]= \
                each['Regex'].replace(')','').replace('(','').split('|')[-1]
        else:
            Solar_Festival['{0}-{1}'.format(each['month'], each['day'])] = \
                each['Regex'].replace(')', '').replace('(', '').split('|')[-1]
    return Solar_Festival,Lunar_Festival

#构建节日结合



# 获得清明那天的节日
def get_qingming_day(year):
    if 1700 < year <= 3100:
        if year == 2232:
            qingming_day = 4
        else:
            coefficient = [5.15, 5.37, 5.59, 4.82, 5.02, 5.26, 5.48, 4.70, 4.92, 5.135, 5.36, 4.60, 4.81, 5.04, 5.26]
            mod = year % 100
            qingming_day = int(mod * 0.2422 + coefficient[year // 100 - 17] - mod // 4)
        return qingming_day
    else:
        raise ValueError("Year out of conversion range")


# 类TimePoint的构建
class TimePoint:
    year, month, day, hour, minute, second = None, None, None, None, None, None
    weekday = None
    # isAccurateTo不同整数值代表0：year，1：month，2：day，3：hour, 4:minute,5:second,6:isweek None:isvaildday
    isAccurateTo = None
    whichFestival = None
    season = None

    # 构造函数，存在三种清理，依次进行判断处理
    def __init__(self, tu=None, isWeek=None, tp=None):
        # 采用list进行初始化,后接参数isWeek进行判断是否是周
        if tu is not None and isWeek is not None:
            # 设置长度为6的存储单元
            time_unit = [None, None, None, None, None, None]
            if isWeek:
                cale = datetime(tu[0], tu[1], tu[2])
                # 找到最近的已经过去的礼拜天
                cale = cale - timedelta(days=cale.isoweekday())
                tu[0], tu[1], tu[2] = cale.year, cale.month, cale.day
            # tu赋值到time_unit单元内
            for i in range(0, len(tu)):
                if tu[i] == -1:
                    break
                time_unit[i] = tu[i]
            # 进行精确位置设置
            if isWeek:
                self.isAccurateTo = 6
            else:
                if tu[i] is -1:
                    self.isAccurateTo = i - 1
                else:
                    self.isAccurateTo = i
            # 初始化年、月、日，时、分、秒
            self.year, self.month, self.day = time_unit[0], time_unit[1], time_unit[2]
            self.hour, self.minute, self.second = time_unit[3], time_unit[4], time_unit[5]
            # 判断输入时间是否为有效时间
            if not self.isValidDate():
                self.isAccurateTo = None

        # 第二种构造情况，只有一个输入，且其为TimePoint类型
        if tp is not None:
            if tp.isAccurateTo is not None:
                self.isAccurateTo = tp.isAccurateTo
                self.year, self.month, self.day = tp.year, tp.month, tp.day
                self.hour, self.minute, self.second = tp.hour, tp.minute, tp.second
            else:
                pass

    # 内置方法转化为string类型
    def toString(self):
        res = ''
        if self.year is not None:
            res = res + str(self.year) + '年'
            if self.month is not None:
                res = res + str(self.month) + '月'
                if self.day is not None:
                    res = res + str(self.day) + '日'
                    if self.hour is not None:
                        res = res + str(self.hour) + '时'
                        if self.minute is not None:
                            res = res + str(self.minute) + '分'
                            if self.second is not None:
                                res = res + str(self.second) + '秒'

        if self.isAccurateTo is None:
            return "CANNOT UNDERSTAND or INVALID"
        if self.isAccurateTo == 6:
            res = res + " 开始的那一周"
        return res

    # 判断读入的时间是否是有效时间
    def isValidDate(self):
        if self.year is None:
            # print("This is a empty TimePoint.")
            return True
        if self.year is not None:
            if self.year < 0:
                return False
            else:
                if self.month is None:
                    return True
                if self.month is not None:
                    if self.month > 12 or self.month < 1:
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

    def toDict(self):
        res = {}
        if self.isAccurateTo is None:
            return {'ans': 'CANNOT UNDERSTAND or INVALID'}
        else:
            if self.year is not None:
                res['year'] = self.year
                if self.month is not None:
                    res['month'] = self.month
                    if self.day is not None:
                        res['day'] = self.day
                        if self.hour is not None:
                            res['hour'] = self.hour
                            if self.minute is not None:
                                res['minute'] = self.minute
                                if self.second is not None:
                                    res['second'] = self.second
            return res

    # 将此对象转换成json格式字符
    def toJson(self):
        return json.dumps(self.toDict())

    # 转换成为一个时间的list
    def toTimeUnitsArray(self):
        timeUnitArray = [-1, -1, -1, -1, -1, -1]
        if self.year is not None:
            timeUnitArray[0] = self.year
        if self.month is not None:
            timeUnitArray[1] = self.month
        if self.day is not None:
            timeUnitArray[2] = self.day
        if self.hour is not None:
            timeUnitArray[3] = self.hour
        if self.minute is not None:
            timeUnitArray[4] = self.minute
        if self.second is not None:
            timeUnitArray[5] = self.second
        return timeUnitArray

    # 设置类对象的某一位为val，timeUnit为枚举类，可以为整数，也可以为名字
    def setUnitValue(self, timeUnit, val):
        if timeUnit is 0 or timeUnit is 'year':
            self.year = val
        elif timeUnit is 1 or timeUnit is 'month':
            self.month = val
        elif timeUnit is 2 or timeUnit is 'day':
            self.day = val
        elif timeUnit is 3 or timeUnit is 'hour':
            self.hour = val
        elif timeUnit is 4 or timeUnit is 'minute':
            self.minute = val
        elif timeUnit is 5 or timeUnit is 'second':
            self.second = val

    def isFestival(self):
        # 判断是不是合法的日期
        if self.isAccurateTo is None or self.isAccurateTo < 2 or self.isAccurateTo == 6:
            return False
        Solar_Festival,Lunar_Festival= get_festival_dict()
        # 判断是不是清明
        if self.month == 4:
            qingmingday = get_qingming_day(self.year)
            if qingmingday == self.day:
                return True,u'清明节'
        # 判断是不是在节假日字典当中
        tf = LunarSolarConverter()
        Lunar_day = tf.SolarToLunar(Solar(self.year, self.month, self.day))
        format_str1 = "{0}-{1}".format(self.month, self.day)
        format_str2 = "{0}-{1}".format(Lunar_day.lunarMonth, Lunar_day.lunarDay)
        if format_str1 in Solar_Festival:
            return True,Solar_Festival[format_str1]
        elif format_str2 in Lunar_Festival:
            return True,Lunar_Festival[format_str2]
        else:
            return False

    # 进行TimePoint的加法操作
    # 注意零时间不能和任意时间进行加减
    def addTime(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        if second is not 0:
            if self.isAccurateTo is not None and self.isAccurateTo == 5:
                time_this = datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
                time_this = time_this + relativedelta(years=year) + relativedelta(months=month) + relativedelta(
                    days=day) \
                            + relativedelta(hours=hour) + relativedelta(minutes=minute) + relativedelta(seconds=second)
                temp = [int(each) for each in time_this.strftime('%Y-%m-%d-%H-%M-%S').split('-')]
                self.year, self.month, self.day = temp[0], temp[1], temp[2]
                self.hour, self.minute, self.second = temp[3], temp[4], temp[5]
                return
            else:
                raise ValueError("Can't add or subtract seconds.Please check the object precise range.\n")
        if minute is not 0:
            if self.isAccurateTo is not None and (self.isAccurateTo <= 5 and self.isAccurateTo >= 4):
                time_this = datetime(self.year, self.month, self.day, self.hour, self.minute)
                time_this = time_this + relativedelta(years=year) + relativedelta(months=month) + relativedelta(
                    days=day) \
                            + relativedelta(hours=hour) + relativedelta(minutes=minute)
                temp = [int(each) for each in time_this.strftime('%Y-%m-%d-%H-%M').split('-')]
                self.year, self.month, self.day = temp[0], temp[1], temp[2]
                self.hour, self.minute = temp[3], temp[4]
                return
            else:
                raise ValueError("Can't add or subtract seconds.Please check the object precise range.\n")
        if hour is not 0:
            if self.isAccurateTo is not None and (self.isAccurateTo <= 5 and self.isAccurateTo >= 3):
                time_this = datetime(self.year, self.month, self.day, self.hour)
                time_this = time_this + relativedelta(years=year) + relativedelta(months=month) + relativedelta(
                    days=day) \
                            + relativedelta(hours=hour)
                temp = [int(each) for each in time_this.strftime('%Y-%m-%d-%H').split('-')]
                self.year, self.month, self.day = temp[0], temp[1], temp[2]
                self.hour = temp[3]
                return
            else:
                raise ValueError("Can't add or subtract seconds.Please check the object precise range.\n")
        if day is not 0:
            if self.isAccurateTo is not None and (self.isAccurateTo <= 6 and self.isAccurateTo >= 2):
                time_this = datetime(self.year, self.month, self.day)
                time_this = time_this + relativedelta(years=year) + relativedelta(months=month) + relativedelta(
                    days=day)
                temp = [int(each) for each in time_this.strftime('%Y-%m-%d').split('-')]
                self.year, self.month, self.day = temp[0], temp[1], temp[2]
                return
            else:
                raise ValueError("Can't add or subtract seconds.Please check the object precise range.\n")
        if month is not 0:
            if self.isAccurateTo is not None and (self.isAccurateTo <= 6 and self.isAccurateTo >= 1):
                time_this = datetime(self.year, self.month, 1)
                time_this = time_this + relativedelta(years=year) + relativedelta(months=month)
                temp = [int(each) for each in time_this.strftime('%Y-%m-%d').split('-')]
                self.year, self.month = temp[0], temp[1]
                return
            else:
                raise ValueError("Can't add or subtract seconds.Please check the object precise range.\n")
        if year is not 0:
            if self.isAccurateTo is not None and (self.isAccurateTo <= 6 and self.isAccurateTo >= 0):
                time_this = datetime(self.year, 1, 1)
                time_this = time_this + relativedelta(years=year)
                temp = [int(each) for each in time_this.strftime('%Y-%m-%d').split('-')]
                self.year = temp[0]
                return
            else:
                raise ValueError("Can't add or subtract seconds.Please check the object precise range.\n")

