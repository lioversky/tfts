# -*- coding:utf-8 -*-

"""
对外方法返回的类型都为：TFTSData


"""

from util.time_util import *
from config import config_model
from data import data_model, data_reader
import tensorflow as tf
import numpy as np
import datetime


def parse_train_data(config):
    """
    生成训练数据
    :param config:
    :return:
    """
    data_config = config.data_config
    tfts = data_model.TFTSData()
    train_start_time = date_to_str(data_config.train_start_time, DATETIME_FORMAT_1)

    timedelta = None
    if data_config.period_type == config_model.PERIOD_TYPE_HOUR:
        timedelta = datetime.timedelta(hours=data_config.period_num)
    elif data_config.period_type == config_model.PERIOD_TYPE_DAY:
        timedelta = datetime.timedelta(days=data_config.period_num)
    elif data_config.period_type == config_model.PERIOD_TYPE_WEEK:
        timedelta = datetime.timedelta(weeks=data_config.period_num)

    end_time = str_to_datetime(train_start_time, DATETIME_FORMAT_1) + timedelta
    train_end_time = datetime_to_str(end_time, DATETIME_FORMAT_1)

    if data_config.source_type == config_model.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_config = data_config.source_config
        # 训练样本的起止时间
        times, load_data = data_reader.read_data_from_influxdb(influxdb_config, train_start_time, train_end_time,
                                                               data_config.period_interval, smooth=True)
        tfts.train_times = times
        x = np.array(range(len(times)))
        tfts.train_data = {
            tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
            tf.contrib.timeseries.TrainEvalFeatures.VALUES: load_data
        }
    # TODO:
    # elif data_config.source_type == Config.DataConfig.SOURCE_TYPE_ES:
    #     train_data = load_data_from_influxdb(data_config)
    # elif data_config.source_type == Config.DataConfig.SOURCE_TYPE_FILE:
    #     train_data = load_data_from_file(data_config)
    return tfts


def parse_predict_data(config):
    """
    根据配置生成预测数据，按照预测周期和延迟生成预测时间序列
    预测总时长=验证周期+预测周期
    predict_start_time=
        predict_end_time - predict_interval - period_interval * output_window_size
    predict_end_time=current_time - predict_delays
    :param config:
    :return:
    """
    data_config = config.data_config

    predict_config = config.predict_config
    train_config = config.train_config
    # 计算数据查询起止时间
    cur_timestamp = get_cur_timestamp()
    cur_timestamp = str_to_timestamp('2018-05-05T22:00:00Z', DATETIME_FORMAT_1)
    # end_time = datetime.datetime.strptime('2018-05-05T22:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    # end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
    #     cur_timestamp - time_util.get_config_time_seconds(predict_config.predict_delay)))
    end_time = timestamp_to_datetime(
        int((cur_timestamp - get_config_time_seconds(
            predict_config.predict_delay)) / data_config.period_time_unit) * data_config.period_time_unit)

    predict_end_time_str = datetime_to_str(end_time, DATETIME_FORMAT_1)
    evaluation_data_size = train_config.window_size
    second_size = get_config_time_seconds(
        predict_config.predict_interval) + data_config.period_time_unit * evaluation_data_size
    start_time = datetime_add_seconds(end_time, -second_size)

    predict_start_time_str = datetime_to_str(start_time, DATETIME_FORMAT_1)
    # 使用训练开始时间计算周期
    train_start_datetime = date_to_datetime(data_config.train_start_time)
    base_index = int((start_time - train_start_datetime).total_seconds() / data_config.period_time_unit)
    # 封装数据
    tfts = data_model.TFTSData()
    if data_config.source_type == config_model.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_config = data_config.source_config
        ts_times, ts_data = data_reader.read_data_from_influxdb(influxdb_config, predict_start_time_str,
                                                                predict_end_time_str,
                                                                data_config.period_interval)
    # 只保留window_size数作为evaluation
    x = np.array(range(base_index, base_index + evaluation_data_size))
    tfts.evaluation_data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: ts_data[0:evaluation_data_size, :],
    }
    tfts.evaluation_times = ts_times[0:evaluation_data_size]

    tfts.predict_times = ts_times[evaluation_data_size:]
    tfts.real_data = ts_data[evaluation_data_size:, :]
    return tfts
