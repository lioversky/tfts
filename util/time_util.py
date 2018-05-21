# -*- coding:utf-8 -*-
"""
时间工具类
"""

import datetime, time

DATETIME_FORMAT_1 = '%Y-%m-%dT%H:%M:%SZ'
DATETIME_FORMAT_2 = '%Y-%m-%d'


def get_config_time_seconds(config_str):
    unit = config_str[-1]
    value = int(config_str[0:len(config_str) - 1])

    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 60 * 60
    elif unit == 'd':
        return value * 60 * 60 * 24


def timestamp_to_datetime(timestamp):
    """
    时间戳转datetime
    :param timestamp: 时间戳
    :return: datetime
    """
    return datetime.datetime.fromtimestamp(timestamp)


def timestamp_to_time(timestamp):
    """
    时间戳转date
    :param timestamp: 时间戳
    :return: date
    """
    return time.localtime(timestamp)


def timestamp_to_str(timestamp, fmt):
    """
    时间戳转字符
    :param timestamp: 时间戳
    :param fmt: 日期格式
    :return: 字符
    """
    return time.strftime(fmt, time.localtime(timestamp))


def datetime_to_str(dt, fmt):
    """
    datetime转字符
    :param dt: datetime
    :param fmt: 日期格式
    :return: 字符
    """
    return dt.strftime(fmt)


def datetime_to_timestamp(dt):
    """
    datetime转时间戳
    :param dt: datetime
    :return: 时间戳
    """
    return dt.timestamp()


def datetime_to_time(dt):
    """
    datetime转时间
    :return: 时间
    """
    return dt.timetuple()


def date_to_datetime(dt):
    """
    日期转datetime
    :param dt: 日期
    :return: datetime
    """
    return str_to_datetime(date_to_str(dt, DATETIME_FORMAT_1), DATETIME_FORMAT_1)


def date_to_timestamp(dt):
    pass


def date_to_str(dt, fmt):
    """
    日期转字符
    :param dt: 日期
    :param fmt: 日期格式
    :return: 字符
    """
    return dt.strftime(fmt)


def get_cur_datetime():
    return datetime.datetime.now()


def get_cur_timestamp():
    return int(time.time())


def get_cur_date():
    return datetime.date.today()


def get_cur_str(fmt):
    return datetime.datetime.now().strftime(fmt)


def str_to_timestamp(dt_str, fmt):
    """
    字符串转时间戳
    :param dt_str: 字符串
    :param fmt: 日期格式
    :return:
    """
    time_array = time.strptime(dt_str, fmt)
    return int(time.mktime(time_array))


def str_to_datetime(dt_str, fmt):
    """
    字符串转datetime
    :param dt_str:字符串
    :param fmt:日期格式
    :return:datetime
    """
    return datetime.datetime.strptime(dt_str, fmt)


def str_to_date(dt_str, fmt):
    pass


def str_to_time(dt_str, fmt):
    """
    字符串转时间
    :param dt_str: 字符串
    :param fmt: 日期格式
    :return: 时间
    """
    return time.strptime(dt_str, fmt)


def time_to_str(dt, fmt):
    return dt.strftime(fmt)


def datetime_add_seconds(dt, seconds):
    return dt + datetime.timedelta(seconds=seconds)


if __name__ == '__main__':
    dt_str = "2018-05-05T22:00:00Z"
    str_datetime = str_to_datetime(dt_str, DATETIME_FORMAT_1)
    # str_time = str_to_time(dt_str, DATETIME_FORMAT_1)
    str_timestamp = str_to_timestamp(dt_str, DATETIME_FORMAT_1)

    # print(time_to_str(str_time, DATETIME_FORMAT_1))

    datetime_timestamp = datetime_to_timestamp(str_datetime)
    timestamp_datetime = timestamp_to_datetime(str_timestamp)

    print(timestamp_to_datetime(str_timestamp))
    print(timestamp_datetime)
    print(timestamp_to_str(datetime_timestamp, DATETIME_FORMAT_1))

    print(get_cur_datetime())
    print(timestamp_to_datetime(get_cur_timestamp()))
    print(date_to_datetime(get_cur_date()))
    print(get_cur_str(DATETIME_FORMAT_1))
