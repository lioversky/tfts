# -*- coding:utf-8 -*-

"""
对外方法返回的类型都为：TFTSData


"""

from util import time_util
from config import config_model
import datetime, time
from data import data_model, data_reader


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
        tfts.train_data = load_data
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
    end_time = datetime.datetime.now() - datetime.timedelta(
        seconds=time_util.get_config_time_seconds(predict_config.predict_delay))
    predict_end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    data_size = time_util.get_config_time_seconds(
        predict_config.predict_interval) + train_config.period_time_unit * train_config.ar_config.input_window_size
    predict_start_time = (end_time - datetime.timedelta(seconds=data_size)).strftime('%Y-%m-%dT%H:%M:%SZ')
    # 封装数据
    tfts = data_model.TFTSData()
    if data_config.source_type == config.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_config = data_config.source_config
        times, load_data = data_reader.read_data_from_influxdb(influxdb_config, predict_start_time, predict_end_time,
                                                               train_config.period_interval)

    tfts.evaluation_data = load_data
    tfts.evaluation_times = times
    predict_times = []

    predict_start_time = datetime.datetime.strptime(str(predict_config.predict_start_time), '%Y-%m-%d')
    for i in range(predict_config.steps):
        predict_time = predict_start_time + \
                       datetime.timedelta(seconds=i * train_config.period_time_unit)
        predict_times.append(predict_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    tfts.predict_times = predict_times
    return tfts
