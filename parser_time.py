# -*- coding: utf-8 -*-
from TimeClasses.TimeResult import TimeResult
from TimeClasses.TimePoint import TimePoint
from TimeClasses.get_file_path import read_Regex_file
from TimeClasses.StringPreHandlingModule import preHandling
from TimeClasses.LunarSolarConverter import Lunar, Solar, LunarSolarConverter
import re
import math
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class TimeParser:
    __timeBaseArray, __time_temp= [-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1]
    __TUNIT_MAP = {0:'year',1:'month',2:'day',3:'hour',4:'minute',5:'second'}
    #内部中间数据进行结果判断和中间处理结果存储
    __rawTimeExpression, __time_parsing_result_str = '',''
    __tp = TimePoint()
    __isPreferFuture, __isLunarDate, __isWeek = True,False,False
    #内存储数据，为正则表达
    __dateRex, __timeRex = '', ''
    __festivalJsonArray, __intervalJsonArray = [],[]
    __regexMap= { }
    #初始化，对节日、时间、间隔等正则规格进行读入
    def __init__(self):
        self.__dateRex = read_Regex_file('DatefilePath')
        self.__timeRex = read_Regex_file('TimeFilePath')
        self.__festivalJsonArray = read_Regex_file('FestivalFilePath')
        self.__intervalJsonArray = read_Regex_file('IntervalTermFilePath')
        self.__regexMap = read_Regex_file('timeRegexPath')
        #print(self.__dateRex)

#* 新的时间解析入口
#* @input param timeString 为string类型
#* @return TimeResul类型

#1
    def parseTimeMain(self,timeString):
        timeResult = TimeResult()
        rule = self.__regexMap['isTimePointWithBar']
        if(re.search(rule,timeString)):
            timeString = timeString.replace("-",".")
        #print(timeString)
        # from XX to XX
        rule = self.__regexMap['isFromToInterval']
        if(re.search(rule,timeString)):
            splitResults = re.split(rule, timeString)
            ##如果前面是纯数字，后面的那个带单位，把单位也赋给前面
            if(re.search("^[\\d]+$",splitResults[0])):
                temp = re.split("[\\d]+",splitResults[-1])
                splitResults[0] = splitResults[0]+temp[len(temp) - 1]
            start = self.parseTimePoint(splitResults[0])
            end = self.__parseTimePoint(splitResults[-1], start)
            timeResult = TimeResult(tp1=start,tp2=end)
        ## 周末，早上这种，先把短语替换成“xx到xx”这种，再按时间段解析
        rule = self.__regexMap['isTermInterval']
        if(re.search(rule,timeString)):
            timeResult = self.__parseTimeInterval(timeString)
        ##剩下全是时间点
        if(timeResult.isTimePoint is False and timeResult.isTimeInterval is False):
            timeResult = self.parseTimePoint(timeString)
        #print(timeResult.toString())
        return timeResult
#2解析单个时间点的情况，为TimePoint的输出
    def parseTimePoint(self,timeString):
        ##初始化
        self.__isLunarDate, self.__isWeek= False,False
        time_grid = datetime.now().strftime('%Y-%m-%d-%H-%M-%S').split('-')
        for i in range(0,6):
            self.__timeBaseArray[i] = int(time_grid[i])
        self.__rawTimeExpression = preHandling(timeString)
        ##初始化time_temp 数组
        for i in range(0,len(self.__time_temp)):
            self.__time_temp[i] = -1
        self.__mainParseProcess()
        return self.__tp


 #转换成string类型
#3
    def toString(self):
        return  self.__rawTimeExpression + " ---> "+ self.__time_parsing_result_str


# 解析周末，早上这种，结果为TimeResult
# @param timeString，输入一个时间表达字符串
# @return 结果为TimeResult类型
# 1, 先解析前面能确定的时间点，
# 2，时间段可以查json得到两个时间点表达式
# 3，因为限定词总在最后，在前面结果的基础上加入时间段
# @throws Exception
#01
    def __parseTimeInterval(self,timeString):
        self.__isLunarDate, self.__isWeek= False,False  ##初始化time_temp 数组
        for i in range(0, len(self.__time_temp)):
            self.__time_temp[i] = -1
        ##获取当前时间到self.__timeBaseArray数组内
        time_grid = datetime.now().strftime('%Y-%m-%d-%H-%M-%S').split('-')
        for i in range(0,6):
            self.__timeBaseArray[i] = int(time_grid[i])
        self.__rawTimeExpression = preHandling(timeString)

        self.__mainParseProcess()
        ##self.__tp 中已经有解析好的前面背景时间点
        ##查json调取timeString对应的两个时间点
        for i in range(0,len(self.__intervalJsonArray)):
            template = self.__intervalJsonArray[i]
            patternString = template['Regex']
            if(re.search(patternString,self.__rawTimeExpression)):
                prefix = re.sub(patternString,'',timeString)
                startTPstr = prefix + template['start']
                endTPstr = prefix + template['end']
                startTP = self.__parseTimePoint(startTPstr, self.__tp)

                endTP = self.__parseTimePoint(endTPstr, startTP)
                endTP = self.__checckBefore(startTP,endTP)
                af = TimeResult(tp1=startTP, tp2=endTP)

                return af
        return TimeResult()


    def __checckBefore(self,tp1,tp2):
        if(tp1.year <tp2.year):
            return tp2
        if(tp1.year> tp2.year):
            tp2.setUnitValue('year',tp1.year)
        if(tp1.isAccurateTo is 0):
            tp2.setUnitValue('year',tp2.year+1)
            return tp2
        if(tp1.month<tp2.month):
            return tp2
        if(tp1.month>tp2.month):
            tp2.setUnitValue('year',tp2.year+1)
            return tp2
        if(tp1.isAccurateTo is 1):
            tp2.setUnitValue('month',tp2.month+1)
            if (tp2.month > 12):
                tp2.setUnitValue('year', tp2.year + 1)
                tp2.setUnitValue('month', 1)
            return tp2
        if(tp1.day < tp2.day):
            return tp2
        if(tp1.day > tp2.day):
            tp2.setUnitValue('month',tp2.month+1)
            if (tp2.month > 12):
                tp2.setUnitValue('year', tp2.year + 1)
                tp2.setUnitValue('month', 1)
            return tp2
        return tp2


## 带有上文信息的时间解析，通常用在时间段解析的结束时间解析，开始时间为上文信息
# @param timeString 为string类型，context 为imePointT类型
# @return TimePoint类型
#02
    def __parseTimePoint(self,timeString, context):

        ##/把上文信息设为基准时间，TimeBase
        self.__isLunarDate, self.__isWeek= False,False
        ##initialize time_temp array
        for i in range(0, len(self.__time_temp)):
            self.__time_temp[i] = -1
        ##如果context是有效的

        if(context.year is not None):
            newTimeBase = context.toTimeUnitsArray()
            for i in range(0, 6):
                self.__timeBaseArray[i] = newTimeBase[i]


        self.__rawTimeExpression = preHandling(timeString)
        ##如果当前字符串只是一个数字，则用这个值替换上文的最后一位有效时间
        if(re.search("^[\\d]+$",timeString)):
            endTP = TimePoint(tp=context)
            endTP.setUnitValue(context.isAccurateTo,int(timeString))
            return endTP

        self.__mainParseProcess()
        return self.__tp

#region normalization
#年-规范化方法
#该方法识别时间表达式单元的年字段
#03#
    def __norm_setyear(self):
        rule = self.__regexMap["year2digits"]#识别两位数字的年
        re_match = re.search(rule,self.__rawTimeExpression)
        if(re_match):
            self.__time_temp[0] = int(re_match.group())
            if(self.__time_temp[0]>=0 and self.__time_temp[0]<100):
                if(self.__time_temp[0]<30):#30以下表示2000年以后的年份
                    self.__time_temp[0] = self.__time_temp[0]+2000
                else:
                    self.__time_temp[0] = self.__time_temp[0]+1900#否则表示1900年以后的年份
        #识别三位数和四位数表示的年，如果有，覆盖之前两位结果
        rule = self.__regexMap["year4digits"]
        re_match = re.search(rule,self.__rawTimeExpression)
        if(re_match):
            self.__time_temp[0]= int( re_match.group())

#月-规范化方法
#该方法识别时间表达式单元的月字段
#04
    def __norm_setmonth(self):
        rule = self.__regexMap["month"]
        re_match = re.search(rule,self.__rawTimeExpression)
        if(re_match):
            self.__time_temp[1] = int(re_match.group())
            self.__preferFuture(1) #倾向于未来时间的情况


# 检查输入字段是否包含节日关键词，有的话解析
#05
    def __festivalday(self):
        for i in range(0,len(self.__festivalJsonArray)):
            template = self.__festivalJsonArray[i]
            patternString = template['Regex']
            if(re.search(patternString,self.__rawTimeExpression)):
                month = template['month']
                date = template['day']
                if('isLunar' in template.keys()):
                    if(template['isLunar'] == 'true'):
                        self.__isLunarDate = True

                self.__time_temp[1] =int(month)
                if(re.search("清明",patternString)):
                    if(self.__time_temp[0] is not -1):
                        self.__time_temp[2] = int(math.floor((self.__time_temp[0]-2000)*0.2422 + 4.81)-(self.__time_temp[0]-2000)//4)
                    elif((self.__timeBaseArray[1]*100+self.__timeBaseArray[2]) > 406):
                        self.__time_temp[2] = int(math.floor((self.__timeBaseArray[0]+1-2000)*0.2422 + 4.81)-(self.__timeBaseArray[0]+1-2000)//4)
                    else:
                        self.__time_temp[2] = int(math.floor((self.__timeBaseArray[0]-2000)*0.2422 + 4.81)-(self.__timeBaseArray[0]-2000)//4)
                else:
                    self.__time_temp[2]=int(date)
                self.__preferFuture(1)
                break

# 年-月-日 兼容模糊写法, 诸如11月2，11-2，11.2等等
#06
    def __norm_setmonth_fuzzyday(self):
        rule = self.__regexMap["mm_dd"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            matchStr = re_match.group()
            p = "(月|\\.|\\-|/)"
            m = re.search(p,matchStr)
            if(m):
                month = matchStr[0:m.span()[0]]
                date = matchStr[m.span()[1]:len(matchStr)]
                self.__time_temp[1]=int(month)
                self.__time_temp[2] = int(date)
                self.__preferFuture(1)  # 倾向于未来时间的情况
    #第二种情况进行处理
        rule = self.__regexMap["yy_mm"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            matchStr = re_match.group()
            p = "(年|\\.|\\-)"
            m = re.search(p, matchStr)
            if (m):
                year = matchStr[0:m.span()[0]]
                month = matchStr[m.span()[1]:len(matchStr)]
                yearVal = int(year)
                if(yearVal<100):
                    yearVal = yearVal+2000
                self.__time_temp[0] = yearVal
                self.__time_temp[1] = int(month)
                self.__preferFuture(1)  # 倾向于未来时间的情况

#该方法识别时间表达式单元的日字段，x/xx 号/日
#07
    def __norm_setday(self):
        rule = self.__regexMap["day"]
        re_match = re.search(rule,self.__rawTimeExpression)
        if(re_match):
            self.__time_temp[2] = int(re_match.group())
            self.__preferFuture(2) #倾向于未来时间的情况


#时-规范化方法
#该方法识别时间表达式单元的时字段
#08
    def __norm_sethour(self):
        rule = self.__regexMap["hour"]
        temp = '?'+self.__rawTimeExpression
        re_match = re.search(rule, temp)
        if (re_match):
            self.__time_temp[3] = int(re_match.group())

        rule = self.__regexMap["hour_pureNumber"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            self.__time_temp[3] = int(re_match.group())
#
         # 对关键字：早（包含早上/早晨/早间），上午，中午,午间,下午,午后,晚上,傍晚,晚间,晚,pm,PM的正确时间计算
         # 规约：
         # 1.中午/午间0-10点视为12-22点
         # 2.下午/午后0-11点视为12-23点
         # 3.晚上/傍晚/晚间/晚1-11点视为13-23点，12点视为0点
         # 4.0-11点pm/PM视为12-23点

        rule = self.__regexMap["mid_day"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            if (self.__time_temp[3] >= 0 and  self.__time_temp[3] <= 10):
                self.__time_temp[3] = self.__time_temp[3]+12

        rule = self.__regexMap["afternoon"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            if (self.__time_temp[3] >= 0 and self.__time_temp[3] <= 11):
                self.__time_temp[3] = self.__time_temp[3] + 12

        rule = self.__regexMap["evening"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            if (self.__time_temp[3] >= 1 and self.__time_temp[3] <= 11):
                self.__time_temp[3] = self.__time_temp[3] + 12
            elif(self.__time_temp[3] is 12):
                self.__time_temp[3] = 0

        self.__preferFuture(3) # 倾向于未来时间的情况


#分-规范化方法
#该方法识别时间表达式单元的分字段
#09
    def __norm_setminute(self):
        rule = self.__regexMap["minute_number"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            if(re_match.group() is not ""):
                self.__time_temp[4]=int(re_match.group())
                self.__preferFuture(4)#处理倾向于未来时间的情况

        #加对一刻，半，3刻的正确识别（1刻为15分，半为30分，3刻为45分）
        rule = self.__regexMap["minute_quarter"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            self.__time_temp[4] = 15
            self.__preferFuture(4)

        rule = self.__regexMap["minute_half"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            self.__time_temp[4] = 30
            self.__preferFuture(4)  # 处理倾向于未来时间的情况

        rule = self.__regexMap["minute_3quarters"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            self.__time_temp[4] = 45
            self.__preferFuture(4)  # 处理倾向于未来时间的情况


#秒-规范化方法
#该方法识别时间表达式单元的秒字段
#010
    def __norm_setsecond(self):
        #添加了省略“分”说法的时间
        #如17点15分32
        rule = self.__regexMap["second"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            self.__time_temp[5]=int(re_match.group())


#特殊形式的规范化方法
#该方法识别特殊形式的时间表达式单元的各个字段
#011#
    def __norm_setTotal(self):
        rule = self.__regexMap["yy_mm_dd"]
        temp = '?' + self.__rawTimeExpression
        re_match = re.search(rule,temp)
        if (re_match):
            tmp_target = re_match.group()
            tmp_parser = tmp_target.split(":")
            self.__time_temp[3],self.__time_temp[4],self.__time_temp[5]=int(tmp_parser[0]),int(tmp_parser[1]),int(tmp_parser[2])
            self.__preferFuture(3) #处理倾向于未来时间的情况

        rule = self.__regexMap["hh_mm"]
        temp = '?' + self.__rawTimeExpression
        re_match = re.search(rule, temp)
        if (re_match):
            tmp_target = re_match.group()
            tmp_parser = tmp_target.split(":")
            self.__time_temp[3], self.__time_temp[4]= int(tmp_parser[0]), int(tmp_parser[1])
            self.__preferFuture(3)  # 处理倾向于未来时间的情况

        rule = self.__regexMap["yyyy_mm_dd"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            tmp_target = re_match.group()
            tmp_parser = tmp_target.split("-")
            self.__time_temp[0], self.__time_temp[1], self.__time_temp[2] = int(tmp_parser[0]), int(tmp_parser[1]), int(tmp_parser[2])

        #mm/dd/yyyy
        rule = self.__regexMap["mmddyyyy"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            tmp_target = re_match.group()
            tmp_parser = tmp_target.split("/")
            self.__time_temp[1], self.__time_temp[2], self.__time_temp[0] = int(tmp_parser[0]), int(tmp_parser[1]), int(tmp_parser[2])  # mm/dd/yyyy
        ##yyyy.mm.dd
        rule = self.__regexMap["yyyymmdd"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            tmp_target = re_match.group()
            tmp_parser = tmp_target.split(".")
            self.__time_temp[0], self.__time_temp[1], self.__time_temp[2] = int(tmp_parser[0]), int(tmp_parser[1]), int(tmp_parser[2])

        ##yyyymmdd, pure number
        rule = self.__regexMap["yyyymmdd_8digits"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            tmp_target = re_match.group()
            leng = len(tmp_target)
            self.__time_temp[0]=int(tmp_target[0:leng-4])
            if(self.__time_temp[0]<100):
                self.__time_temp[0] = self.__time_temp[0]+2000
            self.__time_temp[1] = int(tmp_target[leng-4:leng-2])
            self.__time_temp[2] = int(tmp_target[leng - 2:leng])


#设置以上文时间为基准的时间偏移计算
#时间基准一律以当前时间算
#012
    def __norm_setBaseRelated(self):
        time_now = datetime.now()
        flag = [False,False,False]
        #在“天之前”的数字
        rule = self.__regexMap["days_before"]
        re_match = re.search(rule,self.__rawTimeExpression)
        if(re_match):
            flag[2]=True
            day_decrease = int(re_match.group())
            time_now = time_now - relativedelta(days=day_decrease)
        #在“天之后”的数字
        rule = self.__regexMap["days_after"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            day_increase = int(re_match.group())
            time_now = time_now + relativedelta(days=day_increase)
        #在“周之前”的数字
        rule = self.__regexMap["weeks_before"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            week_decrease = int(re_match.group())
            time_now = time_now - relativedelta(weeks=week_decrease)
        #在“周之后”的数字
        rule = self.__regexMap["weeks_after"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            week_increase = int(re_match.group())
            time_now = time_now + relativedelta(weeks=week_increase)
        #在“月之前”的数字
        rule = self.__regexMap["months_before"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[1] = True
            month_decrease = int(re_match.group())
            time_now = time_now - relativedelta(months=month_decrease)
        #在“月之后”的数字
        rule = self.__regexMap["months_after"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[1] = True
            month_increase = int(re_match.group())
            time_now = time_now + relativedelta(months=month_increase)
        # 在“年之前”的数字
        rule = self.__regexMap["years_before"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[0] = True
            year_decrease = int(re_match.group())
            time_now = time_now - relativedelta(years=year_decrease)
        # 在“年之后”的数字
        rule = self.__regexMap["years_after"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[0] = True
            year_increase = int(re_match.group())
            time_now = time_now + relativedelta(years=year_increase)
        #保存已经处理过的基准时间
        time_fin= time_now.strftime('%Y-%m-%d-%H-%M-%S').split('-')
        if(flag[0] or flag[1] or flag[2]):
            self.__time_temp[0] = int(time_fin[0])
        if(flag[1] or flag[2]):
            self.__time_temp[1] = int(time_fin[1])
        if(flag[2]):
            self.__time_temp[2] = int(time_fin[2])


# 设置当前时间相关的时间表达式
# 时间基准一律以当前时间算
#013
    def __norm_setCurRelated(self):
        time_now = datetime.now()
        flag = [False,False,False]
        # 在“年之后”的数字
        rule = self.__regexMap["theYearBeforeLast"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[0] = True
            num_increase = re_match.span()[1]-re_match.span()[0]
            time_now = time_now - relativedelta(years=num_increase)

        rule = self.__regexMap["lastYear"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[0] = True
            time_now = time_now - relativedelta(years=1)

        rule = self.__regexMap["thisYear"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[0] = True
            time_now = time_now + relativedelta(years=0)

        rule = self.__regexMap["nextYear"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[0] = True
            time_now = time_now + relativedelta(years=1)

        rule = self.__regexMap["theYearAfterNext"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[0] = True
            num_increase_days = re_match.span()[1]-re_match.span()[0]
            time_now = time_now + relativedelta(years=num_increase_days)

        rule = self.__regexMap["lastMonth"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[1] = True
            subMatch = re.search("上+",re_match.group())
            if(subMatch):
                num_increase_days = subMatch.span()[1]-subMatch.span()[0]
                time_now = time_now - relativedelta(months=num_increase_days)

        rule = self.__regexMap["thisMonth"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[1] = True
            time_now = time_now + relativedelta(months=0)

        rule = self.__regexMap["nextMonth"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[1] = True
            subMatch = re.search("下+",re_match.group())
            if(subMatch):
                num_increase_days = subMatch.span()[1]-subMatch.span()[0]
                time_now = time_now + relativedelta(months=num_increase_days)

        rule = self.__regexMap["theDayBeforeYesterday"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            num_decrease_days = re_match.span()[1] - re_match.span()[0]
            time_now = time_now - relativedelta(days=num_decrease_days)

        rule = self.__regexMap["yesterday"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            time_now = time_now - relativedelta(days=1)

        rule = self.__regexMap["today"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            time_now = time_now - relativedelta(days=0)

        rule = self.__regexMap["tomorrow"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            time_now = time_now + relativedelta(days=1)

        rule = self.__regexMap["theDayAfterTomorrow"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            num_increase_days = re_match.span()[1] - re_match.span()[0]
            time_now = time_now + relativedelta(days=num_increase_days)

        rule = self.__regexMap["lastWeek"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            try:
                weekday = int(re_match.group()[-1])
            except:
                weekday = -1
            if(weekday is not -1):
                if(weekday == 7):
                    time_now = time_now - timedelta(days=time_now.isoweekday())+ relativedelta(days=7)
                else:
                    time_now = time_now - timedelta(days=time_now.isoweekday()) + relativedelta(days=weekday)
            else:
                self.__isWeek = True
            subMatch = re.search("上+", re_match.group())
            if (subMatch):
                num_decrease = subMatch.span()[1] - subMatch.span()[0]
                time_now = time_now - relativedelta(weeks= num_decrease)

        rule = self.__regexMap["nextWeek"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            flag[2] = True
            try:
                weekday = int(re_match.group()[-1])
            except:
                weekday = -1
            if (weekday is not -1):
                if (weekday == 7):
                    time_now = time_now - timedelta(days=time_now.isoweekday()) + relativedelta(days=7)
                else:
                    time_now = time_now - timedelta(days=time_now.isoweekday()) + relativedelta(days=weekday)
            else:
                self.__isWeek = True
            subMatch = re.search("下+", re_match.group())
            if (subMatch):
                num_decrease = subMatch.span()[1] - subMatch.span()[0]
                time_now = time_now + relativedelta(weeks=num_decrease)

        rule = self.__regexMap["weekDay_cod1"]
        rule2 = self.__regexMap["weekDay_cod2"]
        re_match = re.search(rule, self.__rawTimeExpression)
        re_match2 = re.search(rule2,self.__rawTimeExpression)
        if (re_match and re_match2):
            flag[2] = True
            try:
                weekday = int(re_match.group()[-1])
            except:
                weekday =1
            if (weekday == 7):
                time_now = time_now - timedelta(days=time_now.isoweekday()) + relativedelta(days=7)
            else:
                time_now = time_now - timedelta(days=time_now.isoweekday()) + relativedelta(days=weekday)
            time_now= self.__preferFutureWeek(weekday, time_now)

        time_fin = time_now.strftime('%Y-%m-%d-%H-%M-%S').split('-')
        if(flag[0] or flag[1] or flag[2]):
            self.__time_temp[0] = int(time_fin[0])
        if(flag[1] or flag[2]):
            self.__time_temp[1] = int(time_fin[1])
        if(flag[2]):
            self.__time_temp[2] = int(time_fin[2])


#014
    def __norm_setLastDayOfSomething(self):
        rule = self.__regexMap['lastDayOfSomething']
        re_match = re.search(rule,self.__rawTimeExpression)
        if(re_match):
            if(self.__timeBaseArray[1] is not -1 or self.__time_temp[1] is not -1):
                context_year,context_month = self.__timeBaseArray[0],self.__timeBaseArray[1]
                if(self.__time_temp[1] is not -1): #某月最后一天，优先用time_temp赋值
                    context_year,context_month = self.__time_temp[0],self.__time_temp[1]
                if(context_year is -1):
                    context_year = self.__timeBaseArray[0]
                new_date = datetime(context_year,context_month,1)
                new_date = new_date + relativedelta(months=1)
                new_date = new_date - relativedelta(days=1)
                time_fin = new_date.strftime('%Y-%m-%d').split('-')
                time_fin = [int(i) for i in time_fin]
                self.__time_temp[0],self.__time_temp[1],self.__time_temp[2] = time_fin[0],time_fin[1],time_fin[2]

#识别农历日期#
#015
    def __norm_lunarCalendar(self):
        month_lunar = -1
        day_lunar = -1
        rule = self.__regexMap["lunar_mmdd"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            strArr = re_match.group().split("月初")
            month_lunar = int(strArr[0])
            day_lunar = int(strArr[1])
            self.__isLunarDate = True
        #正月各种
        rule = self.__regexMap["lunar_1mdd"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            strArr = re.split("(月初?)|(大年初?)",re_match.group())
            if(strArr[0] is "腊" or ('大年'in re_match.group() and '大年初' not in re_match.group())):
                month_lunar = 12
            else:
                month_lunar = 1

            day_lunar = int(strArr[-1])
            self.__isLunarDate = True
            #几月廿几，农历特有
        rule = self.__regexMap["lunar_mm2d"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match):
            strArr = re_match.group().split("月廿")
            month_lunar = int(strArr[0])
            day_lunar = int(strArr[1])
            if(day_lunar is 10):
                day_lunar = 20
            else:
                day_lunar = day_lunar + 20
            self.__isLunarDate = True
        #注明农历
        rule = self.__regexMap["lunar"]
        re_match = re.search(rule, self.__rawTimeExpression)
        if (re_match or (self.__isLunarDate and  month_lunar is -1 and day_lunar is -1)):
            self.__isLunarDate = True
            month_lunar = self.__time_temp[1]
            day_lunar = self.__time_temp[2]
        if(self.__isLunarDate is not True):
            return
        #convert lunar date, and consider preferring future time
        time_fin = datetime.now().strftime('%Y-%m-%d').split('-')
        time_fin = [int(i) for i in time_fin]
        solar_today = Solar(time_fin[0],time_fin[1],time_fin[2])
        tf = LunarSolarConverter()
        lunar_today = tf.SolarToLunar(solar_today)

        try:
            if ((month_lunar > lunar_today.lunarMonth) or (month_lunar is lunar_today.lunarMonth and day_lunar >= lunar_today.lunarDay)):
                lunar_toConvt = Lunar(lunar_today.lunarYear, month_lunar, day_lunar)
            else:
                lunar_toConvt = Lunar(lunar_today.lunarYear+1, month_lunar, day_lunar)
        except:
            self.__time_temp[0],self.__time_temp[-1],self.__time_temp[2] = -1,-1,-1
            return
        solar_res = tf.LunarToSolar(lunar_toConvt)
        self.__time_temp[0] = solar_res.solarYear
        self.__time_temp[1] = solar_res.solarMonth
        self.__time_temp[2] = solar_res.solarDay

    def __norm_qinming(self):
        rule = '清明'
        if(re.search(rule,self.__rawTimeExpression)):
            if(self.__time_temp[0] is not -1):
                year = self.__time_temp[0]
                if (year > 1700 and year <= 3100):
                    if (year == 2232):
                        qingming_day = 4
                    else:
                        coefficient = [5.15, 5.37, 5.59, 4.82, 5.02, 5.26, 5.48, 4.70, 4.92, 5.135, 5.36, 4.60, 4.81,
                                       5.04, 5.26]
                        mod = year % 100
                        qingming_day = int(mod * 0.2422 + coefficient[year // 100 - 17] - mod // 4)
                    self.__time_temp[2]=qingming_day



#
#时间表达式规范化的入口
#时间表达式识别后，通过此入口进入规范化阶段，
#具体识别每个字段的值
#016
    def __mainParseProcess(self):
        self.__festivalday()
        self.__norm_setyear()
        self.__norm_setmonth()
        self.__norm_setday()
        self.__norm_setmonth_fuzzyday()
        self.__norm_setBaseRelated()
        self.__norm_setCurRelated()
        self.__norm_setLastDayOfSomething()
        self.__norm_sethour()
        self.__norm_setminute()
        self.__norm_setsecond()
        self.__norm_setTotal()
        self.__norm_lunarCalendar()
        self.__norm_qinming()
        tunitpointer=5
        while tunitpointer>=0 and self.__time_temp[tunitpointer]<0:
            tunitpointer = tunitpointer - 1

        for i in range(0,tunitpointer):
            if(self.__time_temp[i]<0):
                self.__time_temp[i] = self.__timeBaseArray[i]

        self.__tp = TimePoint(tu=self.__time_temp,isWeek=self.__isWeek)
        self.__time_parsing_result_str = self.__tp.toString()

# 如果用户选项是倾向于未来时间，检查int的checkTimeIndex所指的时间是否是过去的时间，如果是的话，将大一级的时间设为当前时间的+1。
# 只检查指定时间单位，操作完全在tunit上进行
#017
    def __preferFuture(self, checkTimeIndex):
        for i in range(0,checkTimeIndex):
            if(self.__time_temp[i]is not -1):
                return
        if(not self.__isPreferFuture):
            return
        curTime = self.__timeBaseArray[checkTimeIndex]
        if(curTime <= self.__time_temp[checkTimeIndex] or self.__time_temp[checkTimeIndex] == -1):
            return
####确认一下timeBaseArray是不是当前时间的存储数组####
        if(checkTimeIndex == 1):
            now_time = datetime(self.__timeBaseArray[0], 1, 1)
            now_time = now_time + relativedelta(years=1)
        elif(checkTimeIndex == 2):
            now_time = datetime(self.__timeBaseArray[0], self.__timeBaseArray[1], 1)
            now_time = now_time + relativedelta(months=1)
        elif(checkTimeIndex == 3):
            now_time = datetime(self.__timeBaseArray[0], self.__timeBaseArray[1], self.__timeBaseArray[2])
            now_time = now_time + relativedelta(days=1)
        elif(checkTimeIndex == 4):
            now_time = datetime(self.__timeBaseArray[0], self.__timeBaseArray[1], self.__timeBaseArray[2]
                                , self.__timeBaseArray[3])
            now_time = now_time + relativedelta(hours=1)
        elif(checkTimeIndex == 5):
            now_time = datetime(self.__timeBaseArray[0], self.__timeBaseArray[1], self.__timeBaseArray[2]
                                , self.__timeBaseArray[3], self.__timeBaseArray[4])
            now_time = now_time+relativedelta(minutes=1)
        time_add= now_time.strftime('%Y-%m-%d-%H-%M-%S').split('-')
        time_add = [int(i) for i in time_add]
        for i in range(0,checkTimeIndex):
            self.__time_temp[i] = time_add[i]

# 如果用户选项是倾向于未来时间，检查所指的day_of_week是否是过去的时间，如果是的话，设为下周。
# 如在周五说：周一开会，识别为下周一开会
# @param weekday 识别出是周几（范围1-7）
#**Calendar 类型的c需要注意
#018
    def __preferFutureWeek(self, weekday, c):
        if(not self.__isPreferFuture):
            return c
        checkTimeIndex = 2
        for i in range(0, checkTimeIndex):
            if (self.__time_temp[i] is not -1):
                return c
        now_time = datetime(self.__timeBaseArray[0], self.__timeBaseArray[1], self.__timeBaseArray[2])
        cod = c-now_time
        if(cod.days>0):
            return c
        else:
            c = c + relativedelta(weeks=1)
            return c

#test

# af = TimeParser()
# print(af.parseTimeMain('2020年清明').toString())
# print(af.parseTimeMain('下午六点到晚上八点').toString())
# print(af.parseTimeMain('两个礼拜前').toString())
# print(af.parseTimeMain('今年到后年').toString())
# print(af.parseTimeMain('月底').toString())
# print(af.parseTimeMain('年底').toString())
# print(af.parseTimeMain('4-7月').toString())
# print(af.parseTimeMain('19年6-10月').toString())
# print(af.parseTimeMain('二月2-4').toString())
# print(af.parseTimeMain('周末').toString())
# print(af.parseTimeMain('上周末').toString())
# print(af.parseTimeMain('下周到下下周').toString())
# print(af.parseTimeMain('今天晚上到后天').toString())
# print(af.parseTimeMain('明晚到明年').toString())
# print(af.parseTimeMain('下午六点').toString())
# print(af.parseTimeMain('下月底').toString())
# print(af.parseTimeMain('周末').toString())
# print(af.parseTimeMain('明年三月').toString())
# print(af.parseTimeMain('大年二十九').toString())
# print(af.parseTimeMain('三月初三').toString())
# print(af.parseTimeMain('二月廿四').toString())
# print(af.parseTimeMain('正月15').toString())
# print(af.parseTimeMain('八月十五').toString())
# print(af.parseTimeMain('农历八月十五').toString())
# print(af.parseTimeMain('周9').toString())
# print(af.parseTimeMain('2月39').toString())
# print(af.parseTimeMain('下个月').toString())
# print(af.parseTimeMain('本月末').toString())
# print(af.parseTimeMain('上上周九').toString())
# print(af.parseTimeMain('大大后天').toString())
# print(af.parseTimeMain('前天').toString())
# print(af.parseTimeMain('明天下午三点').toString())
# print(af.parseTimeMain('五月最后一天').toString())
# print(af.parseTimeMain('十号').toString())
# print(af.parseTimeMain('明年').toString())
# print(af.parseTimeMain('今晚').toString())
# print(af.parseTimeMain('去年冬季').toString())
# print(af.parseTimeMain('下下个星期').toString())






