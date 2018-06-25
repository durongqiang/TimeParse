# -*- coding: utf-8 -*-

import json
import os
from io import open

current_abs_path = os.path.split(os.path.realpath(__file__))[0]

TimeFilePath = '/Regex/times'
DatefilePath = '/Regex/date'
FestivalFilePath = '/Regex/festival.json'
IntervalTermFilePath = '/Regex/intervalTerm.json'
timeRegexPath = '/Regex/timeRegex'


def read_timeRegex_dict():
    resDict = {}
    with open(current_abs_path + timeRegexPath, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            _parts = line.split('\t')
            resDict[_parts[0]] = _parts[1]
    return resDict


def read_date_regex():
    regList = []
    with open(current_abs_path + DatefilePath, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            regList.append(line)
    return '|'.join(regList)


def read_time_regex():
    regList = []
    with open(current_abs_path + TimeFilePath, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            regList.append(line)
    return '|'.join(regList)


def read_festival_regex():
    with open(current_abs_path + FestivalFilePath, encoding='utf-8') as f:
        res = json.load(f)
    return res


def read_interval_regex():
    with open(current_abs_path + IntervalTermFilePath, encoding='utf-8') as f:
        res = json.load(f)
    return res
