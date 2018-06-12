# -*- coding: utf-8 -*-

from datetime import datetime
import json
from TimePoint import TimePoint

class TimeResult:
    year,month,day,hour,minute,second = None,None,None,None,None,None 
    #isAccurateTo不同整数值代表0：year，1：month，2：day，3：hour, 4:minute,5:second,6:isweek None:isvaildday
    isAccurateTo = None
    #判断TimeResult的值的类型，初始化时，均为False
    isTimePoint,isTimeInterval = False,False
    attr = "TimeResult"
    #构造函数，存在两种情况，进行构造

    singleTimePoint = TimePoint()
    #start and end 均为时间点
    startTimePoint,endTimePoint = TimePoint(),TimePoint()
    def __init__(self,tu=None,isWeek=None):
             #采用list进行初始化,后接参数isWeek进行判断是否是周
        if((tu.__class__ is list) and not (isWeek.__class__ is TimePoint) and isWeek is not None):
            #设置长度为6的存储单元
            time_unit = [None,None,None,None,None,None]
            #tu赋值到time_unit单元内
            for i in range(0,len(tu)):
                if(tu[i] == -1):
                    break
                time_unit[i] = tu[i] 
            #进行精确位置设置
            if(isWeek):
                self.isAccurateTo = 6
            else:
                self.isAccurateTo = i
            #初始化年、月、日，时、分、秒
            self.year,self.month,self.day = time_unit[0],time_unit[1],time_unit[2]
            self.hour,self.minute,self.second = time_unit[3],time_unit[4],time_unit[5]
            if(not self.__isValidDate()):
                self.isAccurateTo = None
            #类型为单个点的类型
            self.singleTimePoint = TimePoint(tu,isWeek)
            self.isTimePoint = True
            
        #第二种情况，两个时间点的数据类型
        if((tu.__class__ is TimePoint) and (isWeek.__class__ is TimePoint)): #TO-DO: tp1 时间必须在 tp2 之前
            print('mark')
            self.startTimePoint = TimePoint(tu)
            self.endTimePoint = TimePoint(isWeek)
            self.isTimeInterval = True

        #第三种情况，传入的参数仅一个时间点
        if((tu.__class__ is TimePoint) and isWeek is None):
            if(tu.year is not None):
                self.year,self.month,self.day = tu.year,tu.month,tu.day
                self.hour,self.minute,self.second = tu.hour,tu.minute,tu.second
                self.isAccurateTo = tu.isAccurateTo
                self.singleTimePoint = TimePoint(tu)
                self.isTimePoint = True
                
    #判断值是否时有效的，类似于TimePointa,是一个内部方法，外部并不会使用，故不存在逻辑问题
    def __isValidDate(self):
        if(self.year is None):
            print("This is a empty TimeResult.")
            return True
        if(self.year is not None):
            if(self.year < 0):
                return False
            else:
                if(self.month is None):
                    return True
                if(self.month is not None):
                    if(self.month>12 or self.month<0):
                        return False
        if(self.day is None):
            return True
        try:
            if(self.second is not None):
                datetime(self.year,self.month,self.day,self.hour,self.minute,self.second)
            else:
                if(self.minute is not None):
                    datetime(self.year,self.month,self.day,self.hour,self.minute)
                else:
                    if(self.hour is not None):
                        datetime(self.year,self.month,self.day,self.hour)
                    else:
                        datetime(self.year,self.month,self.day)
                    
        except:
            return False
            
        return True
    
    
    #将该类型转换成string类型
    def toString(self):
        if(self.isTimePoint):
            return self.singleTimePoint.toString()
        if(self.isTimeInterval):
            return self.startTimePoint.toString() + " ->>>>- " + self.endTimePoint.toString()
        return "IS.. NULL"

    #将该类型转换成Json数据类型
    def toJson(self):
        if(self.isTimePoint):
            return self.singleTimePoint.toJson();
        elif (self.isTimeInterval):
            res = ""
            res = res +"[" + self.startTimePoint.toJson() + ","
            res = res + self.endTimePoint.toJson() + "]"
            return res
    ###需要确认一下结果的地方
            #return json.dumps(res)

        return json.dumps("Not a time point")
    
    
    #将该类型存储转换为list<string>类型
    def toStringList(self):
        res = []
        if(self.isTimePoint):
            res.append(self.singleTimePoint.toString())
            return res
        if(self.isTimeInterval):
            res.append(self.startTimePoint.toString())
            res.append('到')
            res.append(self.endTimePoint.toString())
            return res
        res.add("Is.. NULL")
        return res

    #进行代码重构，把TimeResult转换为TimePoint
    def toTimePoint(self):
        if(self.isTimePoint):
            result = TimePoint()
            result.year, result.month, result.day= self.year, self.month, self.day
            result.hour, result.minute, result.second=self.hour, self.minute, self.second
            result.isAccurateTo=self.isAccurateTo
            return result
        else:
            raise IOError("IllegalArgumentException")


tp1 = TimePoint([2018,6,7],1)
tp2 = TimePoint([2018,6,17],1)
sp = TimeResult(tp1,tp2)