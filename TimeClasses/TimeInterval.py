# -*- coding: utf-8 -*-

from TimePoint import TimePoint
import json
from TimeResult import TimeResult

class TimeInterval:
    startTimePoint = TimePoint()
    endTimePoint = TimePoint()
    def __init__(self,tp1=None,tp2 = None):
        if(isinstance(tp1,TimePoint) and isinstance(tp2,TimePoint)):
            self.startTimePoint = TimePoint(tp1)
            self.endTimePoint = TimePoint(tp2)
        
        #第二种情况，如果其传入为TimeResult类型，并且isTimeInterval 为真
        if(isinstance(tp1,TimeResult) and tp2 is None):
            if(tp1.isTimeInterval):
                self.startTimePoint = tp1.startTimePoint
                self.endTimePoint = tp1.endTimePoint
            else:
                raise IOError("IllegalArgumentException")
    
    #将该类型转换为string类型
    def toString(self):
        return self.startTimePoint.toString()+ ' -到- ' +self.endTimePoint.toString()
    
    
    #将该类型转换成为Json数据类型
    def toJson(self):
        res = ''
        res = res+ "[" + self.startTimePoint.toJson() + ","
        res = res+ self.endTimePoint.toJson() + "]"
        return res
###同样需要确认得地方
        #return json.dumps(res)
