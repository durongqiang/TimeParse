# -*- coding: utf-8 -*-
import re

'''
    * 方法numberTranslator的辅助方法，可将[零-九]正确翻译为[0-9]
     *
     * @param s 大写数字
     * @return 对应的整形数，如果不是大写数字返回-1
'''


def wordToNumber(s):
    if (s == ("零") or s == ("0")):
        return 0
    elif (s == ("一") or s == ("1")):
        return 1
    elif (s == ("二") or s == ("两") or s == ("2")):
        return 2
    elif (s == ("三") or s == ("3")):
        return 3
    elif (s == ("四") or s == ("4")):
        return 4
    elif (s == ("五") or s == ("5")):
        return 5
    elif (s == ("六") or s == ("6")):
        return 6
    elif (s == ("七") or s == ("天") or s == ("日") or s == ("末") or s == ("7")):
        return 7
    elif (s == ("八") or s == ("8")):
        return 8
    elif (s == ("九") or s == ("9")):
        return 9
    else:
        return -1


'''
     * 该方法可以将字符串中所有的用汉字表示的数字转化为用阿拉伯数字表示的数字
     * 如"这里有一千两百个人，六百零五个来自中国"可以转化为
     * "这里有1200个人，605个来自中国"
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
    cond = re.search('[一二两三四五六七八九123456789]万[一二两三四五六七八九123456789](?!(千|百|十))', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("万")
        if (tem_str.__len__() == 2):
            num = num + wordToNumber(tem_str[0]) * 10000 + wordToNumber(tem_str[1]) * 1000
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('[一二两三四五六七八九123456789]万[一二两三四五六七八九123456789](?!(千|百|十))', target)

    # 处理仅有千位结果
    cond = re.search('[一二两三四五六七八九123456789]千[一二两三四五六七八九123456789](?!(百|十))', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("千")
        if (tem_str.__len__() == 2):
            num = num + wordToNumber(tem_str[0]) * 1000 + wordToNumber(tem_str[1]) * 100
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('[一二两三四五六七八九123456789]千[一二两三四五六七八九123456789](?!(百|十))', target)

    # 处理仅有百位结果
    cond = re.search('[一二两三四五六七八九123456789]百[一二两三四五六七八九123456789](?!十)', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("百")
        if (tem_str.__len__() == 2):
            num = num + wordToNumber(tem_str[0]) * 100 + wordToNumber(tem_str[1]) * 10
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('[一二两三四五六七八九123456789]百[一二两三四五六七八九123456789](?!十)', target)

    # 处理大写转化为小写
    for each in re.finditer("[零一二两三四五六七八九]", target):
        temp = str(wordToNumber(each.group()))
        target = target[0:each.span()[0]] + str(temp) + target[each.span()[1]:len(target)]

    # 处理周天，星期天替换为周7，星期7的情况
    for each in re.finditer("(?<=(周))[天日]|(?<=(星期))[天日]", target):
        temp = str(wordToNumber(each.group()))
        target = target[0:each.span()[0]] + str(temp) + target[each.span()[1]:len(target)]

    # 处理正常的数据，从十位开处理
    target = '*' + target
    cond = re.search('(?<!(.周|星期))0?[0-9]?十[0-9]?', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("十")
        # print(tem_str)
        if (tem_str.__len__() == 0):
            num = num + 10
        elif (tem_str.__len__() == 1):
            if (int(tem_str[0]) == 0):
                num = num + 10
            else:
                num = num + int(tem_str[0]) * 10
        elif (tem_str.__len__() == 2):
            if (tem_str[0] == ''):
                num = num + 10
            else:
                if (int(tem_str[0]) == 0):
                    num = num + 10
                else:
                    num = num + int(tem_str[0]) * 10
            if (len(tem_str[1]) != 0):
                num = num + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('(?<!(.周|星期))0?[0-9]?十[0-9]?', target)
    target = target[1:len(target)]

    # 处理百位结果
    cond = re.search('0?[1-9]百[0-9]?[0-9]?', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("百")
        if (tem_str.__len__() == 1):
            num = num + int(tem_str[0]) * 100
        elif (tem_str.__len__() == 2):
            if (len(tem_str[1]) == 0):
                num = num + int(tem_str[0]) * 100
            else:
                num = num + int(tem_str[0]) * 100 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('0?[1-9]百[0-9]?[0-9]?', target)

    # 处理千位结果
    cond = re.search('0?[1-9]百[0-9]?[0-9]?', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("百")
        if (tem_str.__len__() == 1):
            num = num + int(tem_str[0]) * 100
        elif (tem_str.__len__() == 2):
            if (len(tem_str[1]) == 0):
                num = num + int(tem_str[0]) * 100
            else:
                num = num + int(tem_str[0]) * 100 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('0?[1-9]百[0-9]?[0-9]?', target)

    # 处理千位结果
    cond = re.search('0?[1-9]千[0-9]?[0-9]?[0-9]?', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("千")
        if (tem_str.__len__() == 1):
            num = num + int(tem_str[0]) * 1000
        elif (tem_str.__len__() == 2):
            if (len(tem_str[1]) == 0):
                num = num + int(tem_str[0]) * 1000
            else:
                num = num + int(tem_str[0]) * 1000 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('0?[1-9]千[0-9]?[0-9]?[0-9]?', target)

    # 处理万位结果
    cond = re.search('[0-9]+万[0-9]?[0-9]?[0-9]?[0-9]?', target)
    while (cond is not None):
        tem_str = cond.group()
        num = 0
        tem_str = tem_str.split("万")
        if (tem_str.__len__() == 1):
            num = num + int(tem_str[0]) * 10000
        elif (tem_str.__len__() == 2):
            num = num + int(tem_str[0]) * 10000 + int(tem_str[1])
        target = target[0:cond.span()[0]] + str(num) + target[cond.span()[1]:len(target)]
        cond = re.search('[0-9]+万[0-9]?[0-9]?[0-9]?[0-9]?', target)

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
    while (cond is not None):
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
    rules = "\\s+"
    target = delKeyword(target, rules)
    rules = "[的]+"
    target = delKeyword(target, rules)

    target = numberTranslator(target)

    # 替换掉,.这类符号
    p = re.compile(".*(，|,)\.*")
    if (p.search(target)):
        target = re.sub("(，|,|\.)", '', target)
    # print(target)
    # 替换掉上1个和下1个,替换为上个和下个
    target = target.replace('下1个', '下个')
    target = target.replace('上1个', '上个')
    return target
