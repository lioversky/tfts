# -*- coding:utf-8 -*-
"""
json文件，解析数据和模型配置，全部如下：
{
  "data_config": {

    "source_type": "",
    "metrics": [],
    "dimensions": {},
    "params": {
      "measurement": "",
      "ip": "",
      "port": ,
      "dbname": ""
    }
  },
  "train_config": {
    "train_start_time": "2018-01-03",
    "model_type": "AR",
    "period_type": "day",
    "period_num": 6,
    "periodicities": ,
    "batch_size": ,
    "window_size": ,
    "model_dir": "",
    "training_steps": ,
    "num_features": 1,
    "params": {
      "input_window_size": ,
      "output_window_size":
    }
  },
  "eval_config": {
    "steps":
  },
  "predict_config": {
    "predict_start_time": "",
    "steps":
  }
}
"""

from config import config_model
from util import time_util
import json
import yaml


def parse_json_config(file):
    with open(file, 'r') as f:
        json_dict = json.load(f)
        f.close()
    return parse_config(json_dict)


def parse_yaml_config(file):
    with open(file, 'r') as f:
        yaml_dict = yaml.load(f)
        f.close()
    return parse_config(yaml_dict)


def parse_config(dict):
    config = config_model.Config()
    if dict['data_config'] is not None:
        config.data_config = parse_data_config(dict['data_config'])
    if dict['train_config'] is not None:
        config.train_config = parse_train_config(dict['train_config'])
    if dict['predict_config'] is not None:
        config.predict_config = parse_predict_config(dict['predict_config'])
    if dict['eval_config'] is not None:
        config.eval_config = parse_evaluation_config(dict['eval_config'])

    return config


def parse_train_config(train_dict):
    """
    解析训练配置
    :param train_dict:
    :return:
    """
    train_config = config_model.TrainConfig()
    train_config.model_type = train_dict['model_type']
    train_config.batch_size = train_dict['batch_size']
    train_config.window_size = train_dict['window_size']
    train_config.num_features = train_dict['num_features']
    train_config.train_start_time = train_dict['train_start_time']

    train_config.period_num = train_dict['period_num']
    train_config.period_type = train_dict['period_type']
    train_config.period_interval = train_dict['period_interval']
    # 计算每个样本间隔周期秒数和单周期样本数
    train_config.period_time_unit = time_util.get_config_time_seconds(train_config.period_interval)

    if train_config.period_type == config_model.PERIOD_TYPE_HOUR:
        train_config.periodicities = 3600 / train_config.period_time_unit
    elif train_config.period_type == config_model.PERIOD_TYPE_DAY:
        train_config.periodicities = 3600 * 24 / train_config.period_time_unit
    elif train_config.period_type == config_model.PERIOD_TYPE_WEEK:
        train_config.periodicities = 3600 * 24 * 7 / train_config.period_time_unit

    params_dict = train_dict['params']
    # 各模型参数
    if train_config.model_type == config_model.TrainConfig.ALGR_TYPE_AR:
        ar_config = config_model.ARConfig()
        ar_config.input_window_size = params_dict['input_window_size']
        ar_config.output_window_size = params_dict['output_window_size']
        train_config.ar_config = ar_config
    elif train_config.model_type == config_model.TrainConfig.ALGR_TYPE_SE:
        se_config = config_model.SEConfig()
        se_config.cycle_num_latent_values = params_dict['cycle_num_latent_values']
        train_config.se_config = se_config
    elif train_config.model_type == config_model.TrainConfig.ALGR_TYPE_LSTM:
        lstm_config = config_model.LSTMConfig()
        lstm_config.num_units = params_dict['num_units']
        train_config.lstm_config = lstm_config
    train_config.training_steps = train_dict['training_steps']
    train_config.model_dir = train_dict['model_dir']

    return train_config


def parse_evaluation_config(eval_dict):
    eval_config = config_model.EvalConfig()
    eval_config.steps = eval_dict['steps']
    return eval_config


def parse_predict_config(predict_dict):
    predict_config = config_model.PredictConfig()
    predict_config.steps = predict_dict['steps']
    predict_config.predict_interval = predict_dict['predict_interval']
    predict_config.predict_delay = predict_dict['predict_delay']
    # 预测结果输出类型和参数
    # predict_config.output_type = predict_dict['output_type']
    if predict_config.output_type == config_model.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_dict = predict_dict['params']
        predict_config.output_config = parse_influxdb_config(influxdb_dict)

    return predict_config


def parse_data_config(data_dict):
    """
    解析数据配置
    :param data_dict:
    :return:
    """
    data_config = config_model.DataConfig()
    data_config.source_type = data_dict['source_type']

    if data_config.source_type == config_model.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_dict = data_dict['params']
        data_config.source_config = parse_influxdb_config(influxdb_dict)
    # todo:解析es config
    elif data_config.source_type == config_model.DataConfig.SOURCE_TYPE_ES:
        pass
    return data_config


def parse_influxdb_config(influxdb_dict):
    influxdb_config = config_model.InfluxdbConfig()
    influxdb_config.dbname = influxdb_dict['dbname']
    influxdb_config.ip = influxdb_dict['ip']
    influxdb_config.port = influxdb_dict['port']
    influxdb_config.measurement = influxdb_dict['measurement']

    influxdb_config.metrics = influxdb_dict['metrics']
    influxdb_config.dimensions = influxdb_dict['dimensions']
    if influxdb_dict.__contains__('retention_policy'):
        influxdb_config.retention_policy = influxdb_dict['retention_policy']
    return influxdb_config
