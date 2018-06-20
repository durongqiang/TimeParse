# -*- coding: utf-8 -*-
import re

'''
    * 方法numberTranslator的辅助方法，可将[零-九]正确翻译为[0-9]
     *
     * @param s 大写数字
     * @return 对应的整形数，如果不是大写数字返回-1
'''


def wordToNumber(s):
    if s == u'零' or s == u'0':
        return 0
    elif s == u'一' or s == u'1':
        return 1
    elif s == u'二' or s == u'两' or s == u'2':
        return 2
    elif s == u'三' or s == u'3':
        return 3
    elif s == u'四' or s == u'4':
        return 4
    elif s == u'五' or s == u'5':
        return 5
    elif s == u'六' or s == u'6':
        return 6
    elif s == u'七' or s == u'天' or s == u'日' or s == u'末' or s == u'7':
        return 7
    elif s == u'八' or s == u'8':
        return 8
    elif s == u'九' or s == u'9':
        return 9
    else:
        return -1


'''
     * 该方法可以将字符串中所有的用汉字表示的数字转化为用阿拉伯数字表示的数字
     * 如'这里有一千两百个人，六百零五个来自中国'可以转化为
     * '这里有1200个人，605个来自中国'
     * 此外添加支持了部分不规则表达方法
     * 如两万零六百五可转化为20650
     * 两百一十四和两百十四都可以转化为214
     * 一六零加一五八可以转化为160+158
     * 该方法目前支持的正确转化范围是0-99999999
     * 该功能模块具有良好的复用性
     *
     * @param target 待转化的字符串
     * @return 转化完毕后的字符串
'''


def numberTranslator(target):
    # 处理仅有万位结果
    cond = re.search(u'[一二两三四五六七八九123456789]万[一二两三四五六七八九123456789](?!(千|百|十))', target)
    while cond is not None:
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split(u'万')
        if tem_str.__len__() == 2:
            num = num + wordToNumber(tem_str[0]) * 10000 + wordToNumber(tem_str[1]) * 1000
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search(u'[一二两三四五六七八九123456789]万[一二两三四五六七八九123456789](?!(千|百|十))', target)

    # 处理仅有千位结果
    cond = re.search(u'[一二两三四五六七八九123456789]千[一二两三四五六七八九123456789](?!(百|十))', target)
    while cond is not None:
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split(u'千')
        if tem_str.__len__() == 2:
            num = num + wordToNumber(tem_str[0]) * 1000 + wordToNumber(tem_str[1]) * 100
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search(u'[一二两三四五六七八九123456789]千[一二两三四五六七八九123456789](?!(百|十))', target)

    # 处理仅有百位结果
    cond = re.search(u'[一二两三四五六七八九123456789]百[一二两三四五六七八九123456789](?!十)', target)
    while cond is not None:
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split(u'百')
        if tem_str.__len__() == 2:
            num = num + wordToNumber(tem_str[0]) * 100 + wordToNumber(tem_str[1]) * 10
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search(u'[一二两三四五六七八九123456789]百[一二两三四五六七八九123456789](?!十)', target)

    # 处理大写转化为小写
    rule = u'[零一二两三四五六七八九]'

    for each in re.finditer(rule, target):
        temp = str(wordToNumber(each.group()))
        target = target[0:each.span()[0]] + str(temp) + target[each.span()[1]:len(target)]

    # 处理周天，星期天替换为周7，星期7的情况
    for each in re.finditer(u'(?<=(周))[天日]|(?<=(星期))[天日]', target):
        temp = str(wordToNumber(each.group()))
        target = target[0:each.span()[0]] + str(temp) + target[each.span()[1]:len(target)]

    # 处理正常的数据，从十位开处理
    target = '*' + target
    cond1 = re.search(u'(?<!(星期))0?[0-9]?十[0-9]?', target)
    cond2 = re.search(u'(?<!(.周))0?[0-9]?十[0-9]?', target)
    cond = cond1 and cond2
    while cond is not None:
        tem_str = cond1.group()
        num = 0
        tem_str = tem_str.split(u'十')
        if tem_str.__len__() == 0:
            num = num + 10
        elif tem_str.__len__() == 1:
            if int(tem_str[0]) == 0:
                num = num + 10
            else:
                num = num + int(tem_str[0]) * 10
        elif tem_str.__len__() == 2:
            if tem_str[0] == '':
                num = num + 10
            else:
                if int(tem_str[0]) == 0:
                    num = num + 10
                else:
                    num = num + int(tem_str[0]) * 10
            if len(tem_str[1]) != 0:
                num = num + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond1 = re.search(u'(?<!(星期))0?[0-9]?十[0-9]?', target)
        cond2 = re.search(u'(?<!(.周))0?[0-9]?十[0-9]?', target)
        cond = cond1 and cond2
    target = target[1:len(target)]

    # 处理百位结果
    cond = re.search(u'0?[1-9]百[0-9]?[0-9]?', target)
    while cond is not None:
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split(u'百')
        if tem_str.__len__() == 1:
            num = num + int(tem_str[0]) * 100
        elif tem_str.__len__() == 2:
            if len(tem_str[1]) == 0:
                num = num + int(tem_str[0]) * 100
            else:
                num = num + int(tem_str[0]) * 100 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search(u'0?[1-9]百[0-9]?[0-9]?', target)

    # 处理千位结果
    cond = re.search(u'0?[1-9]百[0-9]?[0-9]?', target)
    while cond is not None:
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split(u'百')
        if tem_str.__len__() == 1:
            num = num + int(tem_str[0]) * 100
        elif tem_str.__len__() == 2:
            if len(tem_str[1]) == 0:
                num = num + int(tem_str[0]) * 100
            else:
                num = num + int(tem_str[0]) * 100 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search(u'0?[1-9]百[0-9]?[0-9]?', target)

    # 处理千位结果
    cond = re.search(u'0?[1-9]千[0-9]?[0-9]?[0-9]?', target)
    while cond is not None:
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split(u'千')
        if tem_str.__len__() == 1:
            num = num + int(tem_str[0]) * 1000
        elif tem_str.__len__() == 2:
            if len(tem_str[1]) == 0:
                num = num + int(tem_str[0]) * 1000
            else:
                num = num + int(tem_str[0]) * 1000 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search(u'0?[1-9]千[0-9]?[0-9]?[0-9]?', target)

    # 处理万位结果
    cond = re.search(u'[0-9]+万[0-9]?[0-9]?[0-9]?[0-9]?', target)
    while cond is not None:
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split(u'万')
        if tem_str.__len__() == 1:
            num = num + int(tem_str[0]) * 10000
        elif tem_str.__len__() == 2:
            num = num + int(tem_str[0]) * 10000 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search(u'[0-9]+万[0-9]?[0-9]?[0-9]?[0-9]?', target)

    return target


'''
     * 该方法删除一字符串中所有匹配某一规则字串
     * 可用于清理一个字符串中的空白符和语气助词
     *
     * @param target 待处理字符串
     * @param rules 删除规则
     * @return 清理工作完成后的字符串
'''


def delKeyword(target, rules):
    cond = re.search(rules, target)
    while cond is not None:
        target = target[0:cond.span()[0]] + target[cond.span()[1]:len(target)]
        cond = re.search(rules, target)

    return target


'''
0.清理空白符
1.清理语气助词
2.大写数字转化
3.去掉两种符号 .，
4.下一个月和上一个月转化
'''


def preHandling(target):
    rules = u'\\s+'
    target = delKeyword(target, rules)
    rules = u'[的]+'
    target = delKeyword(target, rules)

    target = numberTranslator(target)

    # 替换掉,.这类符号
    p = re.compile(u'.*(，|,)\.*')
    if p.search(target):
        target = re.sub(u'(，|,|\.)', '', target)
    # 替换掉上1个和下1个,替换为上个和下个
    p = re.compile(u'下1个')
    if p.search(target):
        target = re.sub(u'下1个', u'下个', target)

    p = re.compile(u'上1个')
    if p.search(target):
        target = re.sub(u'上1个', u'下个', target)
    return target
