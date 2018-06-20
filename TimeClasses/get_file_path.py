# -*- coding: utf-8 -*-

import json
import os
from io import open


# 获取当前文档的绝对路径
def get_temp_file_path():
    path_str = os.path.dirname(os.path.realpath(__file__))
    path_str = path_str.split('\\')
    tem_path = [temp + '\\' for temp in path_str if temp != path_str[-1]]
    final_path = ''
    for each in tem_path:
        final_path = final_path + each
    return final_path


# 读取配置文件当前路径绝对路径
def get_confing_file_path(temp_file_path):
    return get_temp_file_path() + 'TimeClasses\\config.properties'


# 按字符名字读取文件内路径名
def read_each_file_path(each_file_name):
    each_file_name_path = 'None'
    config_path = get_confing_file_path(get_temp_file_path())
    # 打开配置文件读取内部正则文件与json文件的路径，结果在each_line中
    with open(config_path, encoding='utf-8') as config_file:
        for each_line in config_file:
            each_line = each_line.replace('\n', '')
            each_line = each_line.split('=')
            if each_line[0] == each_file_name:
                each_file_name_path = get_temp_file_path() + 'TimeClasses\\' + each_line[-1]
                break
    # 判断得到的文件路径是否可进行读写操作,存在返回绝对路径名，不存在则输出文件不存在信息
    try:
        with open(each_file_name_path) as f:
            return each_file_name_path
    except IOError:
        print("File {0} is not accessible.".format(each_file_name))


'''
0.针对time文件内容
1.读取文件内容，并将内容存储在文件字典当中并返回；
2.当文件为空返回为空字典；
3.当文件不存在打印文件不存在并且返回空字典。
'''


def read_timeRegexPath_file(each_file_name):
    file_path = read_each_file_path(each_file_name)
    file_haspmap = {}
    if file_path != None:
        with open(file_path, encoding='utf-8') as f:
            for each_line in f:
                each_line = each_line.split()
                file_haspmap[each_line[0]] = each_line[-1]
    if file_haspmap == None:
        print("this file is empty")
    return file_haspmap


'''
0.针对Date和Time文件内容
1.读取文件内容，并将内容存储在string当中并返回；
2.当文件为空返回为空string；
3.当文件不存在打印文件不存在并且返回空string。
'''


def read_Date_or_Time_filePath_file(each_file_name):
    file_path = read_each_file_path(each_file_name)
    file_result = ''
    if file_path != None:
        with open(file_path, encoding='utf-8') as f:
            for each_line in f:
                each_line = each_line.replace('\n', '')
                file_result = file_result + each_line + '|'
    file_result = file_result[0:-1]
    return file_result


'''
0.针对Festival或者Interval文件内容
1.读取文件内容，并将内容存储在list当中并返回；
2.当文件为空返回为空list；
3.当文件不存在打印文件不存在并且返回空list。
'''


def read_Festival_or_Interval_file(each_file_name):
    file_path = read_each_file_path(each_file_name)
    file_result = []
    if file_path != None:
        with open(file_path, encoding='utf-8') as f:
            file_result = json.load(f)
    return file_result


'''
0.根据不同的string读取相应的文件
1.time文件内容调用read_timeRegexPath_file
2.Date和Time文件内容调用read_Date_or_Time_filePath_file
3.Festival或者Interval内的json文件调用read_Festival_or_Interval_file
4.若都不是这些文件名，返回None，并打印信息
5.若要进行功能扩展，再后面加条件分支即可
'''


def read_Regex_file(each_file_name):
    read_Regex_result = None
    if each_file_name == 'timeRegexPath':
        read_Regex_result = read_timeRegexPath_file(each_file_name)
        return read_Regex_result
    elif each_file_name == 'DatefilePath' or each_file_name == 'TimeFilePath':
        read_Regex_result = read_Date_or_Time_filePath_file(each_file_name)
        return read_Regex_result
    elif each_file_name == 'FestivalFilePath' or each_file_name == 'IntervalTermFilePath':
        read_Regex_result = read_Festival_or_Interval_file(each_file_name)
        return read_Regex_result
    else:
        print("This file not exit!")
        return read_Regex_result
