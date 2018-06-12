# -*- coding: utf-8 -*-

from datetime import datetime,timedelta
import json
#类TimePoint的构建
class TimePoint: 
    year,month,day,hour,minute,second = None,None,None,None,None,None 
    weekday = None
    #isAccurateTo不同整数值代表0：year，1：month，2：day，3：hour, 4:minute,5:second,6:isweek None:isvaildday
    isAccurateTo = None
    whichFestival = None
    season = None
    
    #构造函数，存在三种清理，依次进行判断处理
    def __init__(self,tu=None,isWeek=None,tp  = None):
        #采用list进行初始化,后接参数isWeek进行判断是否是周
        if(tu is not None and isWeek is not None):
            #设置长度为6的存储单元
            time_unit = [None,None,None,None,None,None]
            if(isWeek):
                cale = datetime(tu[0],tu[1],tu[2])
                #找到最近的已经过去的礼拜天
                cale = cale-timedelta(days = cale.isoweekday())
                tu[0],tu[1],tu[2] = cale.year, cale.month, cale.day
            #tu赋值到time_unit单元内
            for i in range(0,len(tu)):
                if(tu[i] == -1):
                    break
                time_unit[i] = tu[i]
            #进行精确位置设置
            if(isWeek):
                self.isAccurateTo = 6
            else:
                if(tu[i] is  -1):
                    self.isAccurateTo = i-1
                else:
                    self.isAccurateTo = i
            #初始化年、月、日，时、分、秒
            self.year,self.month,self.day = time_unit[0],time_unit[1],time_unit[2]
            self.hour,self.minute,self.second = time_unit[3],time_unit[4],time_unit[5]
            #判断输入时间是否为有效时间
            if(not self.isValidDate()):
                self.isAccurateTo = None
              
            
        #第二种构造情况，只有一个输入，且其为TimePoint类型
        if(tp is not None):
            if(tp.isAccurateTo is not None):
                self.isAccurateTo = tp.isAccurateTo
                self.year,self.month,self.day = tp.year,tp.month,tp.day
                self.hour,self.minute,self.second = tp.hour,tp.minute,tp.second

            else:
                pass
         
        
    #内置方法转化为string类型
    def toString(self):
        res = ''
        if(self.year is not None):
            res = res + str(self.year) + '年'
            if(self.month is not None):
                res = res + str(self.month) + '月'
                if(self.day is not None):
                    res = res + str(self.day) + '日'
                    if(self.hour is not None):
                        res = res + str(self.hour) + '时'
                        if(self.minute  is not None):
                            res = res + str(self.minute) + '分'
                            if(self.second is not None):
                                res = res +str(self.second) + '秒'
        
        if(self.isAccurateTo is None):
            return "CANNOT UNDERSTAND or INVALID"
        if(self.isAccurateTo == 6):
            res = res + " 开始的那一周"
        return res
    
    
    #判断读入的时间是否是有效时间
    def isValidDate(self):
        if(self.year is None):
            #print("This is a empty TimePoint.")
            return True
        if(self.year is not None):
            if(self.year < 0):
                return False
            else:
                if(self.month is None):
                    return True
                if(self.month is not None):
                    if(self.month>12 or self.month<1):
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
                
    #将此对象转换成json格式字符
    def toJson(self):
        if(self.isAccurateTo is None):
            return json.dumps("CANNOT UNDERSTAND or INVALID")
        else:
            return json.dumps(vars(self))
    
    #转换成为一个时间的list
    def toTimeUnitsArray(self):
        timeUnitArray = [-1,-1,-1,-1,-1,-1]
        if(self.year is not None):
            timeUnitArray[0] = self.year
        if(self.month is not None):
            timeUnitArray[1] = self.month  
        if(self.day is not None):
            timeUnitArray[2] = self.day
        if(self.hour is not None):
            timeUnitArray[3] = self.hour
        if(self.minute is not None):
            timeUnitArray[4] = self.minute
        if(self.second is not None):
            timeUnitArray[5] = self.second
        return timeUnitArray
    
    
    #设置类对象的某一位为val，timeUnit为枚举类，可以为整数，也可以为名字
    def setUnitValue(self,timeUnit, val):
        if(timeUnit is 0 or timeUnit is 'year'):
            self.year = val
        elif(timeUnit is 1 or timeUnit is 'month'):
            self.month = val
        elif(timeUnit is 2 or timeUnit is 'day'):
            self.day = val
        elif(timeUnit is 3 or timeUnit is 'hour'):
            self.hour = val
        elif(timeUnit is 4 or timeUnit is 'minute'):
            self.minute = val
        elif(timeUnit is 5 or timeUnit is 'second'):
            self.second = val


