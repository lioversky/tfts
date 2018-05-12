# -*- coding:utf-8 -*-
"""
时间工具类
"""

import datetime
from config import config_model


def get_config_time_seconds(config_str):
    unit = config_str[-1]
    value = int(config_str[0:len(config_str) - 1])

    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 60 * 60


def get_timedelta(train_config):
    if train_config.period_type == config_model.PERIOD_TYPE_HOUR:
        return datetime.timedelta(hours=train_config.period_num)
    elif train_config.period_type == config_model.PERIOD_TYPE_DAY:
        return datetime.timedelta(days=train_config.period_num)
    elif train_config.period_type == config_model.PERIOD_TYPE_WEEK:
        return datetime.timedelta(weeks=train_config.period_num)
