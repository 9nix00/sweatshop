#!/usr/local/var/pyenv/shims/python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime
from datetime import time

weekday = os.environ.get('SWEATSHOP_WEEKDAY', '7').split(',')
working_time = os.environ.get('SWEATSHOP_WORKING_TIME', '10-19').split('-')

debug = os.environ.get('SWEATSHOP_DEBUG', False)
only_hours = os.environ.get('SWEATSHOP_HOURS', False)

duty = {}

prevs = {
    'yesterday': None,
    'early': None,
    'am': None,
    'pm': None,
    'late': None,
}

# 参考假日表 http://www.gov.cn/zhengce/content/2015-12/10/content_10394.htm
#           http://www.gov.cn/zhengce/content/2016-12/01/content_5141603.htm

#  所有假日均按两倍计算，3倍还要再细化
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

begin_time = time(hour=int(working_time[0]))
half_end_time = time(hour=12)
end_time = time(hour=int(working_time[1]))
zero_time = time(hour=0)
morning_time = time(hour=4)

prev = None
prev_obj = None


def calc_morning(c, t):
    """
    计算早于上班时间
    :param prev: 
    :return: 
    """

    if not t or c != t['date_str']:
        return 0

    if morning_time <= t['time_obj'] < begin_time:
        return begin_time.hour - t['time_obj'].hour

    return 0


def calc_am(c, t):
    """
    计算上午工作时间
    
    有一次提交默认为上午工作
    :return: 
    """
    if not t or c != t['date_str']:
        return 0

    if begin_time <= t['time_obj'] <= half_end_time:
        return 4
    return 0


def calc_pm(c, t):
    """
    计算下午工作时间
    
    有一次提交默认为下午工作
    :return: 
    """
    if not t or c != t['date_str']:
        return 0

    if half_end_time < t['time_obj'] <= end_time:
        # 下午时间
        return 4
    return 0


def calc_night(c, t):
    """
    计算晚上
    :param prev: 
    :return:
    """

    if not t or c != t['date_str']:
        return 0
    if end_time < t['time_obj']:
        return t['time_obj'].hour - end_time.hour
    return 0


def calc_dark(c, t):
    """
    计算凌晨
    
    目前归结到当天，存在误差
    
    ..todo::
        一种解决策略：
            精确的算法应为根据当前日期，获取上一日期，
            并根据上一日期的假期和工作日状态，进行赋值
    
    :param prev: 
    :return: 
    """
    if not t or c != t['date_str']:
        return 0

    if zero_time < time_obj < morning_time:
        return time_obj.hour - zero_time.hour
    return 0


def set_prev(temp):
    if zero_time <= temp['time_obj'] < morning_time:
        prevs['yesterday'] = temp
    elif morning_time <= temp['time_obj'] < begin_time:
        prevs['early'] = temp
    elif begin_time <= temp['time_obj'] < half_end_time:
        prevs['am'] = temp
    elif half_end_time <= temp['time_obj'] <= end_time:
        prevs['pm'] = temp
    elif end_time < temp['time_obj']:
        prevs['late'] = temp
        pass
    pass


for line in sys.stdin:
    user, date_time = line.strip().split("^")

    # 只处理自己的 commit
    date_str, time_str = date_time.split(" ")
    date_time_obj = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    date_obj = date_time_obj.date()
    time_obj = date_time_obj.time()

    if not prev:
        prev = date_str
        prev_obj = date_obj
        set_prev({
            'date_obj': date_obj,
            'time_obj': time_obj,
            'date_str': date_str,
            'time_str': time_str,
            'datetime_obj': date_time_obj,
        })
        continue

    # 同一天，参与单天存储
    if date_str == prev:
        set_prev({
            'date_obj': date_obj,
            'time_obj': time_obj,
            'date_str': date_str,
            'time_str': time_str,
            'datetime_obj': date_time_obj,
        })
        continue

    duty[prev] = 0

    if prev in holiday_list:
        # 假日
        duty[prev] += calc_morning(prev, prevs['early'])
        duty[prev] += calc_am(prev, prevs['am'])
        duty[prev] += calc_pm(prev, prevs['pm'])
        duty[prev] += calc_night(prev, prevs['late'])
        duty[prev] += calc_dark(prev, prevs['yesterday'])

        duty[prev] *= 2 if not only_hours else 1

        pass
    elif str(prev_obj.isoweekday()) in weekday:
        # 普通休息日
        duty[prev] += calc_morning(prev, prevs['early'])
        duty[prev] += calc_am(prev, prevs['am'])
        duty[prev] += calc_pm(prev, prevs['pm'])
        duty[prev] += calc_night(prev, prevs['late'])
        duty[prev] += calc_dark(prev, prevs['yesterday'])

        duty[prev] *= 2 if not only_hours else 1
        pass
    else:
        # 工作日
        duty[prev] += calc_morning(prev, prevs['early'])
        duty[prev] += calc_night(prev, prevs['late'])
        duty[prev] += calc_dark(prev, prevs['yesterday'])

        duty[prev] *= 1.5 if not only_hours else 1
        pass

    prev = date_str
    prev_obj = date_obj
    pass

total = 0
for k, v in duty.items():
    if v and debug:
        print(k, v)
    total += v
    pass

print('累计加班%s:%d' % (
    '时长' if only_hours else '工时', total))
