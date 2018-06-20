# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from datetime import datetime

from dateutil.relativedelta import relativedelta

from TimeClasses.LunarSolarConverter import Lunar, LunarSolarConverter
from TimeClasses.parser_time import TimeParser


# get_qingming_day方法得到每一年清明的阳历日
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


testCases = [
    # 表达式，标准答案，精确至，是否节日
    ('2018/05/02', '2018年5月2日', 'day', None),
    ('20一8年五月二十号', '2018年5月20日', 'day', None),
    ('19年6-10月', '2019年6月 ->>>>- 2019年10月', 'month', None),
    ('下个月的7号', '-', 'day', None),
    ('下个月7号', '-', 'day', None),
    ('明天', '-', 'day', None),
    ('两个礼拜前', '-', 'day', None),
    ('今天下午六点到晚上八点', '-', 'hour', None),
    ('今年到后年', '-', 'year', None),
    ('月底', '-', 'day', None),
    ('年底', '-', 'day', None),
    ('4-7月', '-', 'month', None),
    ('二月2-4', '-', 'day', None),
    ('周末', '-', 'day', None),
    ('上周末', '-', 'day', None),
    ('下周到下下周', '-', 'day', None),
    ('今天晚上到后天', '-', 'day', None),
    ('明晚到明年', '-', 'day', None),
    ('下午六点', '-', 'day', None),
    ('下月底', '-', 'day', None),
    ('明年三月', '-', 'month', None),
    ('大年二十九', '-', 'day', None),
    ('三月初三', '-', 'day', None),
    ('二月廿四', '-', 'day', None),
    ('正月15', '-', 'day', True),
    ('八月十五', '-', 'day', None),
    ('农历八月十五', '-', 'day', True),
    ('周9', '-', 'day', None),
    ('2月39', '-', 'day', None),
    ('下个月', '-', 'month', None),
    ('本月末', '-', 'day', None),
    ('上上周九', '-', 'day', None),
    ('大大后天', '-', 'day', None),
    ('前天', '-', 'day', None),
    ('明天下午三点', '-', 'day', None),
    ('五月最后一天', '-', 'day', None),
    ('十号', '-', 'day', None),
    ('今晚', '-', 'hour', None),
    ('去年冬季', '-', 'month', None),
    ('国庆', '-', 'day', True),
    ('中秋', '-', 'day', True),
    ('圣诞', '-', 'day', True),
    ('1月1号', '-', 'day', True),
    ('今年清明', '-', 'day', None)
]
# 前处理得到答案
for idx, each in enumerate(testCases):
    temp = each[1]
    if idx == 3 or idx == 4:
        temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
        time_now = datetime(temp[0], temp[1], 7) + relativedelta(months=1)
        temp = [int(each) for each in time_now.strftime('%Y-%m-%d').split('-')]
        temp = '{0}年{1}月{2}日'.format(temp[0], temp[1], temp[2])
    elif idx == 5:
        time_now = datetime.now() + relativedelta(days=1)
        temp = '{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
    elif idx == 6:
        time_now = datetime.now() - relativedelta(days=14)
        temp = '{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
    elif idx == 7:
        temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
        time_now = datetime.now() - datetime(temp[0], temp[1], temp[2], 18)
        if time_now.days > 0:
            temp[2] = temp[2] + 1
        temp = '{0}年{1}月{2}日18时 ->>>>- {0}年{1}月{2}日20时'.format(temp[0], temp[1], temp[2])
    elif idx == 8:
        temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
        temp = '{0}年 ->>>>- {1}年'.format(temp[0], temp[0] + 2)
    elif idx == 9:
        temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
        time_now = datetime(temp[0], temp[1], 1) + relativedelta(months=1)
        time_now = time_now - relativedelta(days=1)
        temp = '{0}年{1}月25日 ->>>>- {0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
    elif idx == 10:
        time_now = datetime.now()
        temp = '{0}年12月1日 ->>>>- {0}年12月31日'.format(time_now.year)
    elif idx == 11:
        time_now = datetime.now()
        if time_now.month > 4:
            time_now = time_now + relativedelta(years=1)
        temp = '{0}年4月 ->>>>- {0}年7月'.format(time_now.year)
    elif idx == 12:
        time_now = datetime.now()
        t1 = time_now - datetime(time_now.year, 2, 4)
        if t1.days > 0:
            temp = '{0}年2月2日 ->>>>- {0}年2月4日'.format(time_now.year + 1)
        else:
            temp = '{0}年2月2日 ->>>>- {0}年2月4日'.format(time_now.year)
    elif idx == 13:
        time_now = datetime.now()
        time_now = time_now - relativedelta(days=time_now.isoweekday())
        time_now = time_now + relativedelta(days=7)
        t2 = time_now - relativedelta(days=1)
        if (t2 - datetime.now()).days < 0:
            time_now = time_now + relativedelta(days=7)
            t2 = t2 + relativedelta(days=7)
        temp = '{0}年{1}月{2}日 ->>>>- {3}年{4}月{5}日'. \
            format(t2.year, t2.month, t2.day, time_now.year, time_now.month, time_now.day)
    elif idx == 14:
        time_now = datetime.now()
        time_now = time_now - relativedelta(days=time_now.isoweekday())
        t2 = time_now - relativedelta(days=1)
        temp = '{0}年{1}月{2}日 ->>>>- {3}年{4}月{5}日'. \
            format(t2.year, t2.month, t2.day, time_now.year, time_now.month, time_now.day)
    elif idx == 15:
        time_now = datetime.now()
        time_now = time_now - relativedelta(days=time_now.isoweekday())
        time_now = time_now + relativedelta(weeks=1) + relativedelta(days=1)
        t2 = time_now + relativedelta(days=7)
        time_now = t2 + relativedelta(days=6)
        temp = '{3}年{4}月{5}日 ->>>>- {0}年{1}月{2}日'. \
            format(time_now.year, time_now.month, time_now.day, t2.year, t2.month, t2.day)
    elif idx == 16:
        time_now = datetime.now()
        t2 = time_now + relativedelta(days=2)
        temp = '{0}年{1}月{2}日 ->>>>- {3}年{4}月{5}日'. \
            format(time_now.year, time_now.month, time_now.day, t2.year, t2.month, t2.day)
    elif idx == 17:
        time_now = datetime.now() + relativedelta(days=1)
        temp = '{0}年{1}月{2}日 ->>>>- {3}年'. \
            format(time_now.year, time_now.month, time_now.day, time_now.year + 1)
    elif idx == 18:
        time_now = datetime.now()
        if time_now.hour > 18:
            time_now = time_now + relativedelta(days=1)
        temp = '{0}年{1}月{2}日18时'.format(time_now.year, time_now.month, time_now.day)
    elif idx == 19:
        temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
        time_now = datetime(temp[0], temp[1], 1) + relativedelta(months=2) - relativedelta(days=1)
        t2 = time_now - relativedelta(days=time_now.isoweekday()) + relativedelta(days=1)
        temp = '{3}年{4}月25日 ->>>>- {0}年{1}月{2}日'. \
            format(time_now.year, time_now.month, time_now.day, t2.year, t2.month)
    elif idx == 20:
        time_now = datetime.now()
        temp = '{0}年3月'.format(time_now.year + 1)
    elif idx == 21:
        time_now = datetime.now()
        L_time = Lunar(time_now.year, 12, 29)
        tf_class = LunarSolarConverter()
        result_time = tf_class.LunarToSolar(L_time)
        temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
    elif idx == 22:
        time_now = datetime.now()
        L_time = Lunar(time_now.year, 3, 3)
        tf_class = LunarSolarConverter()
        result_time = tf_class.LunarToSolar(L_time)
        cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
        if cond.days < 0:
            result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 3, 3))
        temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
    elif idx == 23:
        time_now = datetime.now()
        L_time = Lunar(time_now.year, 2, 24)
        tf_class = LunarSolarConverter()
        result_time = tf_class.LunarToSolar(L_time)
        cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
        if cond.days < 0:
            result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 2, 24))
        temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
    elif idx == 24:
        time_now = datetime.now()
        L_time = Lunar(time_now.year, 1, 15)
        tf_class = LunarSolarConverter()
        result_time = tf_class.LunarToSolar(L_time)
        cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
        if cond.days < 0:
            result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 1, 15))
        temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
    elif idx == 25:
        time_now = datetime.now()
        cond = datetime(time_now.year, 8, 15) - time_now
        if cond.days < 0:
            time_now = time_now + relativedelta(years=1)
        temp = '{0}年8月15日'.format(time_now.year)
    elif idx == 26:
        time_now = datetime.now()
        L_time = Lunar(time_now.year, 8, 15)
        tf_class = LunarSolarConverter()
        result_time = tf_class.LunarToSolar(L_time)
        cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
        if cond.days < 0:
            result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 8, 15))
        temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
    elif idx == 27:
        temp = u''
    elif idx == 28:
        temp = u''
    elif idx == 29:
        time_now = datetime.now() + relativedelta(months=1)
        temp = '{0}年{1}月'.format(time_now.year, time_now.month)
    elif idx == 30:
        temp = [int(each) for each in datetime.now().strftime('%Y-%m-%d').split('-')]
        time_now = datetime(temp[0], temp[1], 1) + relativedelta(months=1) - relativedelta(days=1)
        t2 = time_now - relativedelta(days=time_now.isoweekday()) + relativedelta(days=1)
        temp = '{3}年{4}月25日 ->>>>- {0}年{1}月{2}日'. \
            format(time_now.year, time_now.month, time_now.day, t2.year, t2.month)
    elif idx == 31:
        temp = u''
    elif idx == 32:
        time_now = datetime.now() + relativedelta(days=4)
        temp = '{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
    elif idx == 33:
        time_now = datetime.now() - relativedelta(days=2)
        temp = '{0}年{1}月{2}日'.format(time_now.year, time_now.month, time_now.day)
    elif idx == 34:
        time_now = datetime.now() + relativedelta(days=1)
        temp = '{0}年{1}月{2}日15时'.format(time_now.year, time_now.month, time_now.day)
    elif idx == 35:
        time_now = datetime.now()
        cond = datetime(time_now.year, 5, 31) - time_now
        if cond.days < 0:
            time_now = time_now + relativedelta(years=1)
        temp = '{0}年5月31日'.format(time_now.year)
    elif idx == 36:
        time_now = datetime.now()
        cond = datetime(time_now.year, time_now.month, 10) - time_now
        if cond.days < 0:
            time_now = time_now + relativedelta(months=1)
        temp = '{0}年{1}月10日'.format(time_now.year, time_now.month)
    elif idx == 37:
        time_now = datetime.now()
        temp = '{0}年{1}月{2}日18时 ->>>>- {0}年{1}月{2}日23时59分'. \
            format(time_now.year, time_now.month, time_now.day)
    elif idx == 38:
        time_now = datetime.now()
        if time_now.month < 3:
            temp = '{0}年12月 ->>>>- {0}年2月'.format(time_now.year - 2, time_now.year - 1)
        else:
            temp = '{0}年12月 ->>>>- {1}年2月'.format(time_now.year - 1, time_now.year)
    elif idx == 39:
        time_now = datetime.now()
        cond = datetime(time_now.year, 10, 1) - time_now
        if cond.days < 0:
            time_now = time_now + relativedelta(years=1)
        temp = '{0}年10月1日'.format(time_now.year)
    elif idx == 40:
        time_now = datetime.now()
        L_time = Lunar(time_now.year, 8, 15)
        tf_class = LunarSolarConverter()
        result_time = tf_class.LunarToSolar(L_time)
        cond = datetime(result_time.solarYear, result_time.solarMonth, result_time.solarDay) - time_now
        if cond.days < 0:
            result_time = tf_class.LunarToSolar(Lunar(time_now.year + 1, 8, 15))
        temp = '{0}年{1}月{2}日'.format(result_time.solarYear, result_time.solarMonth, result_time.solarDay)
    elif idx == 41:
        time_now = datetime.now()
        cond = datetime(time_now.year, 12, 25) - time_now
        if cond.days < 0:
            time_now = time_now + relativedelta(years=1)
        temp = '{0}年12月25日'.format(time_now.year)
    elif idx == 42:
        time_now = datetime.now()
        cond = datetime(time_now.year, 1, 1) - time_now
        if cond.days < 0:
            time_now = time_now + relativedelta(years=1)
        temp = '{0}年1月1日'.format(time_now.year)
    elif idx == 43:
        time_now = datetime.now()
        qingming_day = get_qingming_day(time_now.year)
        temp = '{0}年4月{1}日'.format(time_now.year, qingming_day)

    testCases[idx] = (testCases[idx][0].encode('utf-8'), temp.encode('utf-8'), testCases[idx][2], testCases[idx][3])

# 进行测试
af = TimeParser()

for (timeExpression, answer, _, _) in testCases:
    result = af.parseTimeMain(timeExpression.decode('utf-8')).toString()
    version_type = sys.version_info.major
    if version_type == 3:
        answer = answer.decode('utf-8')
    if answer is u'':
        if u'年' in result:
            print(u'测试情况：', timeExpression, u'\n结果：', result)
            raise ValueError(u'测试没有通过')
    else:
        if answer not in result:
            print(u'测试情况：', answer, u'\n结果：', result)
            raise ValueError(u'测试没有通过')

print(u'测试通过\n')
