# -*- coding:utf-8 -*-

"""
对外方法返回的类型都为：TFTSData


"""

from influxdb import InfluxDBClient
import numpy as np

import tensorflow as tf
from config import Config

import datetime


class TFTSData:
    """
    train_times、evaluation_times、predict_times 为时间原始数据
    train_data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
    }
    evaluation_data 是evaluation结果，包含start_tuple
    predict_result为预测结果,
    """

    def __init__(self):
        self.train_times = None
        self.evaluation_times = None
        self.predict_times = None
        self.train_data = None
        self.evaluation_data = None
        self.predict_data = None
        self.predict_result = None


def parse_train_data(config):
    """
    生成训练数据
    :param config:
    :return:
    """
    data_config = config.data_config
    tfts = TFTSData()
    if data_config.source_type == Config.DataConfig.SOURCE_TYPE_INFLUXDB:
        times, load_data = load_data_from_influxdb(config)
        tfts.train_times = times
        tfts.train_data = load_data
    # TODO:
    # elif data_config.source_type == Config.DataConfig.SOURCE_TYPE_ES:
    #     train_data = load_data_from_influxdb(data_config)
    # elif data_config.source_type == Config.DataConfig.SOURCE_TYPE_FILE:
    #     train_data = load_data_from_file(data_config)
    return tfts


def load_data_from_file(data_config):
    x = np.array(range(1008))
    y = np.array(range(1008))
    times = np.array(range(1008))
    f = open('/Users/hongxun/PycharmProjects/tfts/kafka_time_series.txt', 'r')
    i = 0
    for line in f.readlines():
        y[i] = int(line.split(",")[1].strip())
        times[i] = int(line.split(",")[0].strip()) / 1000000000.0
        i += 1
    f.close()

    size = data_config.period_num * data_config.periodicities
    x = np.array(range(size))

    data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
    }
    return times, data


def load_data_from_influxdb(config, predict=False):
    """
    从influxdb中读取数据
    训练数据按照训练周期读取
    预测数据，从预测时间向前倒序取一个周期的数据，再取反转正序
    :param config:
    :param predict:
    :return:
    """
    data_config = config.data_config
    influxdb_config = data_config.source_config
    client = InfluxDBClient(influxdb_config.ip, influxdb_config.port,
                            influxdb_config.username, influxdb_config.password,
                            influxdb_config.dbname)
    train_config = config.train_config

    if predict:
        # 从预测时间向前倒序取一个周期的数据
        predict_config = config.predict_config
        sql = "select * from {0} where time < '{1}' order by time desc limit {2}" \
            .format(influxdb_config.measurement,
                    predict_config.predict_start_time,
                    train_config.periodicities * 2)
        # （预测时间-训练时间）秒数/数据周期间隔
        # predict_time = datetime.datetime.strptime(predict_config.predict_start_time, "%Y-%m-%d")
        predict_time = predict_config.predict_start_time
        # train_time = datetime.datetime.strptime(train_config.train_start_time, "%Y-%m-%d")
        train_time = train_config.train_start_time
        end = int((predict_time - train_time).total_seconds() / train_config.period_time_unit)
        # 对x取对应周期序号
        x = np.array(range(end - train_config.periodicities * 2, end, 1))
        result = client.query(sql)
        result_dict = result.raw['series'][0]
        colums_list = result_dict['columns']
        values_list = result_dict['values']
        # 再取反转正序
        times = np.array(values_list)[:, 0][::-1].reshape(-1)
        y = np.array(values_list)[:, 2][::-1].astype(np.int32)
    else:

        sql = "select * from {0} where time >= '{1}' " \
            .format(influxdb_config.measurement,
                    train_config.train_start_time)

        result = client.query(sql)
        result_dict = result.raw['series'][0]
        colums_list = result_dict['columns']
        values_list = result_dict['values']
        times = np.array(values_list)[:, 0].reshape(-1)
        x = np.array(range(len(values_list)))
        y = np.array(values_list)[:, 2].astype(np.int32)
    train_data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
    }
    client.close()
    return times, train_data


def parse_predict_data(config):
    """
    根据配置生成预测数据，按照预测开始时间生成预测时间序列
    :param config:
    :return:
    """
    times, load_data = load_data_from_influxdb(config, predict=True)
    tfts = TFTSData()
    tfts.evaluation_data = load_data
    tfts.evaluation_times = times
    predict_times = []

    predict_config = config.predict_config
    train_config = config.train_config

    predict_start_time = datetime.datetime.strptime(str(predict_config.predict_start_time), '%Y-%m-%d')
    for i in range(predict_config.steps):
        predict_time = predict_start_time + \
                       datetime.timedelta(seconds=i * train_config.period_time_unit)
        predict_times.append(predict_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    tfts.predict_times = predict_times
    return tfts
