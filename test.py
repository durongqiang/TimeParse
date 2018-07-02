# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from datetime import datetime
import sys
from dateutil.relativedelta import relativedelta
from timeParser.LunarSolarConverter import Lunar, Solar, LunarSolarConverter
from timeParser.parser_time import TimeParser
from timeParser.TimePoint import TimePoint


# get_qingming_day方法得到每一年清明的阳历日
def get_qingming_day(year):
    if year > 1700 and year <= 3100:
        if year == 2232:
            qingming_day = 4
        else:
            coefficient = [5.15, 5.37, 5.59, 4.82, 5.02, 5.26, 5.48, 4.70, 4.92, 5.135, 5.36, 4.60, 4.81, 5.04, 5.26]
            mod = year % 100
            qingming_day = int(mod * 0.2422 + coefficient[year // 100 - 17] - mod // 4)
        return qingming_day
    else:
        raise ValueError("Year out of conversion range")


# 改写textCases得到测试样例
testCases = []
# 1
testCases.append((u'2018/05/02', u'2018年5月2日', 'day', None))
# 2
testCases.append((u'20一8年五月二十号', u'2018年5月20日', 'day', None))
# 3
testCases.append((u'19年6-10月', u'2019年6月 ->>>>- 2019年10月', 'month', None))
# 4
temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
time_now = datetime(temp[0], temp[1], 7) + relativedelta(months=1)
temp = [int(each) for each in time_now.strftime('%Y-%m-%d').split('-')]
temp = u'{0}年{1}月{2}日'.format(temp[0], temp[1], temp[2])
testCases.append((u'下个月的7号', temp, 'day', None))
# 5
testCases.append((u'下个月7号', temp, 'day', None))
# 6
time_now = datetime.now() + relativedelta(days=1)
temp = u'{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
testCases.append((u'明天', temp, 'day', None))
# 7
time_now = datetime.now() - relativedelta(days=14)
temp = '{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
testCases.append((u'两个礼拜前', temp, 'day', None))
# 8
temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
time_now = datetime.now() - datetime(temp[0], temp[1], temp[2], 18)
if time_now.days >= 0:
    temp[2] = temp[2] + 1
temp = '{0}年{1}月{2}日18时 ->>>>- {0}年{1}月{2}日20时'.format(temp[0], temp[1], temp[2])
testCases.append((u'下午六点到晚上八点', temp, 'day', None))
# 9
temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
temp = '{0}年 ->>>>- {1}年'.format(temp[0], temp[0] + 2)
testCases.append((u'今年到后年', temp, 'day', None))
# 10
temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
time_now = datetime(temp[0], temp[1], 1) + relativedelta(months=1)
time_now = time_now - relativedelta(days=1)
temp = '{0}年{1}月25日 ->>>>- {0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
testCases.append((u'月底', temp, 'day', None))
# 11
time_now = datetime.now()
temp = '{0}年12月1日 ->>>>- {0}年12月31日'.format(time_now.year)
testCases.append((u'年底', temp, 'day', None))
# 12
time_now = datetime.now()
if time_now.month > 4:
    time_now = time_now + relativedelta(years=1)
temp = '{0}年4月 ->>>>- {0}年7月'.format(time_now.year)
testCases.append((u'4-7月', temp, 'month', None))
# 13
time_now = datetime.now()
t1 = time_now - datetime(time_now.year, 2, 4)
if t1.days > 0:
    temp = '{0}年2月2日 ->>>>- {0}年2月4日'.format(time_now.year + 1)
else:
    temp = '{0}年2月2日 ->>>>- {0}年2月4日'.format(time_now.year)
testCases.append((u'二月2-4', temp, 'month', None))
# 14
time_now = datetime.now()
time_now = time_now - relativedelta(days=time_now.isoweekday())
time_now = time_now + relativedelta(days=7)
t2 = time_now - relativedelta(days=1)
if (t2 - datetime.now()).days < 0:
    time_now = time_now + relativedelta(days=7)
    t2 = t2 + relativedelta(days=7)
temp = '{0}年{1}月{2}日 ->>>>- {3}年{4}月{5}日'. \
    format(t2.year, t2.month, t2.day, time_now.year, time_now.month, time_now.day)
testCases.append((u'周末', temp, 'day', None))
# 15
time_now = datetime.now()
time_now = time_now - relativedelta(days=time_now.isoweekday())
t2 = time_now - relativedelta(days=1)
temp = '{0}年{1}月{2}日 ->>>>- {3}年{4}月{5}日'. \
    format(t2.year, t2.month, t2.day, time_now.year, time_now.month, time_now.day)
testCases.append((u'上周末', temp, 'day', None))
# 16
time_now = datetime.now()
time_now = time_now - relativedelta(days=time_now.isoweekday())
time_now = time_now + relativedelta(weeks=1) + relativedelta(days=1)
t2 = time_now + relativedelta(days=7)
time_now = t2 + relativedelta(days=6)
temp = '{3}年{4}月{5}日 ->>>>- {0}年{1}月{2}日'. \
    format(time_now.year, time_now.month, time_now.day, t2.year, t2.month, t2.day)
testCases.append((u'下周到下下周', temp, 'day', None))
# 17
time_now = datetime.now()
t2 = time_now + relativedelta(days=2)
temp = '{0}年{1}月{2}日 ->>>>- {3}年{4}月{5}日'. \
    format(time_now.year, time_now.month, time_now.day, t2.year, t2.month, t2.day)
testCases.append((u'今天晚上到后天', temp, 'day', None))
# 18
time_now = datetime.now() + relativedelta(days=1)
temp = '{0}年{1}月{2}日 ->>>>- {3}年'. \
    format(time_now.year, time_now.month, time_now.day, time_now.year + 1)
testCases.append((u'明晚到明年', temp, 'day', None))
# 19
time_now = datetime.now()
if time_now.hour > 18:
    time_now = time_now + relativedelta(days=1)
temp = '{0}年{1}月{2}日18时'.format(time_now.year, time_now.month, time_now.day)
testCases.append((u'下午六点', temp, 'day', None))
# 20
temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
time_now = datetime(temp[0], temp[1], 1) + relativedelta(months=2) - relativedelta(days=1)
t2 = time_now - relativedelta(days=time_now.isoweekday()) + relativedelta(days=1)
temp = '{3}年{4}月25日 ->>>>- {0}年{1}月{2}日'. \
    format(time_now.year, time_now.month, time_now.day, t2.year, t2.month)
testCases.append((u'下月底', temp, 'day', None))
# 21
time_now = datetime.now()
temp = '{0}年3月'.format(time_now.year + 1)
testCases.append((u'明年三月', temp, 'day', None))
# 22
time_now = datetime.now()
L_time = Lunar(time_now.year, 12, 29)
tf_class = LunarSolarConverter()
result_time = tf_class.LunarToSolar(L_time)
temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
testCases.append((u'大年二十九', temp, 'day', '大年二十九'))
# 23
time_now = datetime.now()
L_time = Lunar(time_now.year, 3, 3)
tf_class = LunarSolarConverter()
result_time = tf_class.LunarToSolar(L_time)
cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
if cond.days < 0:
    result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 3, 3))
    temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
testCases.append((u'三月初三', temp, 'day', None))
# 24
time_now = datetime.now()
L_time = Lunar(time_now.year, 2, 24)
tf_class = LunarSolarConverter()
result_time = tf_class.LunarToSolar(L_time)
cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
if cond.days < 0:
    result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 2, 24))
temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
testCases.append((u'二月廿四', temp, 'day', None))
# 25
time_now = datetime.now()
L_time = Lunar(time_now.year, 1, 15)
tf_class = LunarSolarConverter()
result_time = tf_class.LunarToSolar(L_time)
cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
if cond.days < 0:
    result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 1, 15))
temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
testCases.append((u'正月15', temp, 'day', '元宵节'))
# 26
time_now = datetime.now()
cond = datetime(time_now.year, 8, 15) - time_now
if cond.days < 0:
    time_now = time_now + relativedelta(years=1)
temp = '{0}年8月15日'.format(time_now.year)
testCases.append((u'八月十五', temp, 'day', None))
# 27
time_now = datetime.now()
L_time = Lunar(time_now.year, 8, 15)
tf_class = LunarSolarConverter()
result_time = tf_class.LunarToSolar(L_time)
cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
if cond.days < 0:
    result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 8, 15))
temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
testCases.append((u'农历八月十五', temp, 'day', '中秋节'))
# 28
testCases.append((u'周9', '', 'day', None))
# 29
testCases.append((u'2月39', '', 'day', None))
# 30
time_now = datetime.now() + relativedelta(months=1)
temp = '{0}年{1}月'.format(time_now.year, time_now.month)
testCases.append((u'下个月', temp, 'month', None))
# 31
temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
time_now = datetime(temp[0], temp[1], 1) + relativedelta(months=1) - relativedelta(days=1)
t2 = time_now - relativedelta(days=time_now.isoweekday()) + relativedelta(days=1)
temp = '{3}年{4}月25日 ->>>>- {0}年{1}月{2}日'. \
    format(time_now.year, time_now.month, time_now.day, t2.year, t2.month)
testCases.append((u'本月末', temp, 'day', None))
# 32
testCases.append((u'上上周九', '', 'day', None))
# 33
time_now = datetime.now() + relativedelta(days=4)
temp = '{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
testCases.append((u'大大后天', temp, 'day', None))
# 34
time_now = datetime.now() - relativedelta(days=2)
temp = '{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
testCases.append((u'前天', temp, 'day', None))
# 35
time_now = datetime.now() + relativedelta(days=1)
temp = '{0}年{1}月{2}日15时'.format(time_now.year, time_now.month, time_now.day)
testCases.append((u'明天下午三点', temp, 'day', None))
# 36
time_now = datetime.now()
cond = datetime(time_now.year, 5, 31) - time_now
if cond.days < 0:
    time_now = time_now + relativedelta(years=1)
temp = '{0}年5月31日'.format(time_now.year)
testCases.append((u'五月最后一天', temp, 'day', None))
# 37
time_now = datetime.now()
cond = datetime(time_now.year, time_now.month, 10) - time_now
if cond.days < 0:
    time_now = time_now + relativedelta(months=1)
temp = '{0}年{1}月10日'.format(time_now.year, time_now.month)
testCases.append((u'十号', temp, 'day', None))
# 38
time_now = datetime.now()
temp = '{0}年{1}月{2}日18时 ->>>>- {0}年{1}月{2}日23时59分'. \
    format(time_now.year, time_now.month, time_now.day)
testCases.append((u'今晚', temp, 'hour', None))
# 39
time_now = datetime.now()
if time_now.month < 3:
    temp = '{0}年12月 ->>>>- {0}年2月'.format(time_now.year - 2, time_now.year - 1)
else:
    temp = '{0}年12月 ->>>>- {1}年2月'.format(time_now.year - 1, time_now.year)
testCases.append((u'去年冬季', temp, 'month', None))
# 40
time_now = datetime.now()
cond = datetime(time_now.year, 10, 1) - time_now
if cond.days < 0:
    time_now = time_now + relativedelta(years=1)
temp = '{0}年10月1日'.format(time_now.year)
testCases.append((u'国庆', temp, 'day', '国庆节'))
# 41
time_now = datetime.now()
L_time = Lunar(time_now.year, 8, 15)
tf_class = LunarSolarConverter()
result_time = tf_class.LunarToSolar(L_time)
cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
if cond.days < 0:
    result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 8, 15))
temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
testCases.append((u'中秋', temp, 'day', '中秋节'))
# 42
time_now = datetime.now()
cond = datetime(time_now.year, 12, 25) - time_now
if cond.days < 0:
    time_now = time_now + relativedelta(years=1)
temp = '{0}年12月25日'.format(time_now.year)
testCases.append((u'圣诞', temp, 'day', '圣诞节'))
# 43
time_now = datetime.now()
cond = datetime(time_now.year, 1, 1) - time_now
if cond.days < 0:
    time_now = time_now + relativedelta(years=1)
temp = '{0}年1月1日'.format(time_now.year)
testCases.append((u'1月1号', temp, 'day', '元旦节'))
# 44
time_now = datetime.now()
qingming_day = get_qingming_day(time_now.year)
temp = '{0}年4月{1}日'.format(time_now.year, qingming_day)
testCases.append((u'今年清明', temp, 'day', '清明节'))

# 需要的话可以增加测试例

for idx, each in enumerate(testCases):
    temp = testCases[idx][1]
    testCases[idx] = (testCases[idx][0].encode('utf-8'), temp.encode('utf-8'), testCases[idx][2], testCases[idx][3])

# 前处理得到答案完毕
# 进行测试


af = TimeParser()
for (timeExpression, answer, _, festAns) in testCases:
    result = af.parseTimeMain(timeExpression.decode('utf-8'))
    festivalRes = result.isFestival()
    if festAns != festivalRes:
        print(timeExpression)
        print(festivalRes)
        print(festAns)

    resultStr = result.toString()
    version_type = sys.version_info.major
    if version_type == 3:
        answer = answer.decode('utf-8')
    if answer is u'':
        if u'年' in resultStr:
            print(timeExpression)
            print(u'测试情况：', answer, u'\n结果：', resultStr)
            raise ValueError(u'测试没有通过')
    else:
        if answer not in resultStr:
            print(timeExpression)
            print(u'测试情况：', answer, u'\n结果：', resultStr)
            raise ValueError(u'测试没有通过')

import time
startTime = time.time()
num_iteration = 10
for i in range(num_iteration):
    for (timeExpression, answer, _, festAns) in testCases:
        res = af.parseTimeMain(timeExpression.decode('utf-8'))
endTime = time.time()
print('平均解析用时：%f'%((endTime-startTime)/(num_iteration*len(testCases))))
print(u'测试通过\n')