# -*- coding:utf-8 -*-

"""
对外方法返回的类型都为：TFTSData


"""

from util import time_util
from config import config_model
import datetime, time
from data import data_model, data_reader
import tensorflow as tf
import numpy as np


def parse_train_data(config):
    """
    生成训练数据
    :param config:
    :return:
    """
    data_config = config.data_config
    train_config = config.train_config
    tfts = data_model.TFTSData()
    train_start_time = train_config.train_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.datetime.strptime(train_start_time,
                                          '%Y-%m-%dT%H:%M:%SZ') + time_util.get_timedelta(train_config)

    train_end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    if data_config.source_type == config_model.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_config = data_config.source_config
        # 训练样本的起止时间
        times, load_data = data_reader.read_data_from_influxdb(influxdb_config, train_start_time, train_end_time,
                                                               train_config.period_interval)
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

    end_time = datetime.datetime.strptime('2018-05-14T11:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    #        - datetime.timedelta(
    # seconds=time_util.get_config_time_seconds(predict_config.predict_delay))
    predict_end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    second_size = time_util.get_config_time_seconds(
        predict_config.predict_interval) + train_config.period_time_unit * train_config.periodicities
    start_time = (end_time - datetime.timedelta(seconds=second_size))
    predict_start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    train_start_datetime = datetime.datetime.strptime(train_config.train_start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                                      '%Y-%m-%dT%H:%M:%SZ')
    base_index = train_config.periodicities + int((
                                                              start_time - train_start_datetime).total_seconds() / train_config.period_time_unit) % train_config.periodicities
    # 封装数据 todo: start_time取整
    tfts = data_model.TFTSData()
    if data_config.source_type == config_model.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_config = data_config.source_config
        ts_times, ts_data = data_reader.read_data_from_influxdb(influxdb_config, predict_start_time_str,
                                                                predict_end_time_str,
                                                                train_config.period_interval)
    # 只保留window_size数作为evaluation
    x = np.array(range(base_index, base_index + train_config.periodicities))
    tfts.evaluation_data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: ts_data[0:train_config.periodicities, :],
    }
    tfts.evaluation_times = ts_times[0:train_config.periodicities]

    tfts.predict_times = ts_times[train_config.periodicities:]
    tfts.real_data = ts_data[train_config.periodicities:, :]
    return tfts
