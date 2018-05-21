# -*- coding:utf-8 -*-
"""
数据输出
写出到各种配置中：influxdb,es,kfaka
"""
from influxdb import InfluxDBClient
from config import config_model


def data_output(output_list, data):
    for config in output_list:
        if config.output_type == config_model.DataConfig.SOURCE_TYPE_INFLUXDB:
            output_influxdb_data(config.output_config, data)


def output_influxdb_data(influxdb_config, data):
    """
    预测结果写到influxdb中
    :param influxdb_config: influxdb配置
    :param data: 预测结果
    :return:
    """
    series = []
    client = InfluxDBClient(influxdb_config.ip, influxdb_config.port,
                            influxdb_config.username, influxdb_config.password,
                            influxdb_config.dbname)
    predict_result = data.predict_result['mean']
    predict_time = data.predict_times

    for i, val in enumerate(predict_time):
        # 预测指标名和结果对应
        fields = {}
        for j, metric in enumerate(influxdb_config.metrics):
            fields[metric] = predict_result[i][j]
        point_values = {
            "measurement": influxdb_config.measurement,
            # "tags": influxdb_config.dimensions,
            "time": predict_time[i],
            "fields": fields
        }
        series.append(point_values)
    flag = client.write_points(series,
                               tags=influxdb_config.dimensions,
                               retention_policy=influxdb_config.retention_policy)
    client.close()

    return flag
