# -*- coding:utf-8 -*-

"""
数据读取模块，从各数据源读取数据


"""
from influxdb import InfluxDBClient
import numpy as np
import tensorflow as tf


def read_data_from_influxdb(influxdb_config, start_time, end_time, train_period_interval):
    """
    从influxdb中读取数据
    训练数据按照训练周期读取
    :param influxdb_config:数据库配置
    :param predict_start_time:
    :param predict_end_time:
    :param train_period_interval: 样本周期间隔
    :return:
    """

    client = InfluxDBClient(influxdb_config.ip, influxdb_config.port,
                            influxdb_config.username, influxdb_config.password,
                            influxdb_config.dbname)
    try:
        metrics = []
        for i in range(0, len(influxdb_config.metrics)):
            metrics.append("sum({0})".format(influxdb_config.metrics[i]))
        metrics_str = ",".join(metrics)
        dimensions_str = ''
        for key in influxdb_config.dimensions:
            dimensions_str = "{0} and {1}='{2}'".format(
                dimensions_str, key, influxdb_config.dimensions[key])
        # if len(influxdb_config.dimensions) > 0:
        #     dimensions_str = "and " + " and ".join(influxdb_config.dimensions)
        sql = """select {0} from {1}  where time < '{2}' and time >='{3}' {4} group by time({5}) """.format(
            metrics_str,
            influxdb_config.measurement,
            end_time,
            start_time,
            dimensions_str,
            train_period_interval
        )
        result = client.query(sql)
        result_dict = result.raw['series'][0]
        colums_list = result_dict['columns']
        values_list = result_dict['values']
        times = np.array(values_list)[:, 0].reshape(-1)
        x = np.array(range(len(values_list)))
        y = np.array(values_list)[:, 1].astype(np.int32)
        train_data = {
            tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
            tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
        }
    finally:
        client.close()

    return times, train_data


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
