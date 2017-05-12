#!/usr/local/var/pyenv/shims/python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from datetime import time

weekday = os.environ.get('SWEETSHOP_WEEKDAY', '7').split(',')
debug = os.environ.get('SWEETSHOP_DEBUG', False)

duty = {}

# 参考假日表 http://www.gov.cn/zhengce/content/2015-12/10/content_10394.htm
#           http://www.gov.cn/zhengce/content/2016-12/01/content_5141603.htm
# 所有假日均不按两倍工资计算

holiday_list = [
    '2016-01-01',
    '2016-02-07',
    '2016-02-08',
    '2016-02-09',
    '2016-02-10',
    '2016-02-11',
    '2016-02-12',
    '2016-02-13',
    '2016-04-04',
    '2016-05-01',
    '2016-05-02',
    '2016-06-09',
    '2016-06-10',
    '2016-06-11',
    '2016-09-15',
    '2016-09-16',
    '2016-09-17',
    '2016-10-01',
    '2016-10-02',
    '2016-10-03',
    '2016-10-04',
    '2016-10-05',
    '2016-10-06',
    '2016-10-07',
    '2017-01-01',
    '2017-01-02',
    '2017-01-27',
    '2017-01-28',
    '2017-01-29',
    '2017-01-30',
    '2017-01-31',
    '2017-02-01',
    '2017-02-02',
    '2017-04-02',
    '2017-04-03',
    '2017-04-04',
    '2017-05-01',
]

duty_day_list = [
    '2016-02-06',
    '2016-02-14',
    '2016-06-12',
    '2016-09-18',
    '2016-10-8',
    '2016-10-9',
    '2017-01-22',
    '2017-02-04',
    '2017-04-01',
]

begin_time = time(hour=10)
half_end_time = time(hour=12)
end_time = time(hour=19)
zero_time = time(hour=0)

prev = None


def calc_morning(prev):
    """
    计算早于上班时间
    :param prev: 
    :return: 
    """
    if prev['time_obj'] < begin_time:
        # 早于上班时间
        # duty[prev['date_str']] += begin_time.hour - prev['time_obj'].hour
        return begin_time.hour - prev['time_obj'].hour
    return 0


def calc_am(prev):
    """
    计算上午工作时间
    
    有一次提交默认为上午工作
    :return: 
    """
    if begin_time <= prev['time_obj'] <= half_end_time:
        return 4
    return 0


def calc_pm(prev):
    """
    计算下午工作时间
    
    有一次提交默认为下午工作
    :return: 
    """
    if half_end_time < prev['time_obj'] <= end_time:
        # 下午时间
        return 4
    return 0


def calc_night(prev):
    """
    计算晚上
    :param prev: 
    :return: 
    """
    if end_time < prev['time_obj']:
        # 下午下班之后的时间
        return prev['time_obj'].hour - end_time.hour
    return 0


def calc_dark(prev):
    """
    计算凌晨
    :param prev: 
    :return: 
    """
    if zero_time < time_obj < begin_time:
        # 跨夜凌晨
        # duty[prev['date_str']] += time_obj.hour - zero_time.hour
        return time_obj.hour - zero_time.hour
    return 0


for line in sys.stdin:
    user, date_time = line.strip().split("^")

    # 只处理自己的 commit
    date_str, time_str = date_time.split(" ")
    date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    date_obj = date_time_obj.date()
    time_obj = date_time_obj.time()

    if not prev:
        prev = {
            'date_obj': date_obj,
            'time_obj': time_obj,
            'date_str': date_str,
            'time_str': time_str,
            'datetime_obj': date_time_obj,
        }
        continue

    # 同一天，忽略
    if date_str == prev['date_str']:
        continue

    duty[prev['date_str']] = 0

    if prev['date_str'] in holiday_list:
        # 假日
        duty[prev['date_str']] += calc_morning(prev)
        duty[prev['date_str']] += calc_am(prev)
        duty[prev['date_str']] += calc_pm(prev)
        duty[prev['date_str']] += calc_night(prev)
        duty[prev['date_str']] += calc_dark(prev)

        duty[prev['date_str']] *= 2
        pass
    elif str(prev['date_obj'].isoweekday()) in weekday:
        # 普通休息日
        duty[prev['date_str']] += calc_morning(prev)
        duty[prev['date_str']] += calc_am(prev)
        duty[prev['date_str']] += calc_pm(prev)
        duty[prev['date_str']] += calc_night(prev)
        duty[prev['date_str']] += calc_dark(prev)

        duty[prev['date_str']] *= 2
        pass
    else:
        # 工作日
        duty[prev['date_str']] += calc_morning(prev)
        duty[prev['date_str']] += calc_night(prev)
        duty[prev['date_str']] += calc_dark(prev)
        pass

    prev = {
        'date_obj': date_obj,
        'time_obj': time_obj,
        'date_str': date_str,
        'time_str': time_str,
        'datetime_obj': date_time_obj,
    }

    pass

total = 0
for k, v in duty.items():
    if v and debug:
        print(k, v)
    total += v
    pass

print('累计加班时长:%d' % total)

