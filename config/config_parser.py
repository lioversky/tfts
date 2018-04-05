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

from config import Config
import json


def parse_config(file):
    with open(file, 'r') as f:
        json_dict = json.load(f)
    config = Config.Config()
    if json_dict['data_config'] is not None:
        config.data_config = parse_data_config(json_dict['data_config'])
    if json_dict['train_config'] is not None:
        config.train_config = parse_train_config(json_dict['train_config'])
    if json_dict['predict_config'] is not None:
        config.predict_config = parse_predict_config(json_dict['predict_config'])
    if json_dict['eval_config'] is not None:
        config.eval_config = parse_evaluation_config(json_dict['eval_config'])

    return config


def parse_train_config(train_dict):
    """
    解析训练配置
    :param train_dict:
    :return:
    """
    train_config = Config.TrainConfig()
    train_config.model_type = train_dict['model_type']
    train_config.periodicities = train_dict['periodicities']
    train_config.batch_size = train_dict['batch_size']
    train_config.window_size = train_dict['window_size']
    train_config.num_features = train_dict['num_features']
    train_config.train_start_time = train_dict['train_start_time']

    train_config.period_num = train_dict['period_num']
    train_config.period_type = train_dict['period_type']
    if train_config.period_type == Config.PERIOD_TYPE_DAY:
        train_config.period_time_unit = 3600 * 24 / train_config.periodicities
    elif train_config.period_type == Config.PERIOD_TYPE_HOUR:
        train_config.period_time_unit = 3600 / train_config.periodicities
    elif train_config.period_type == Config.PERIOD_TYPE_WEEK:
        train_config.period_time_unit = 3600 * 24 * 7 / train_config.periodicities

    params_dict = train_dict['params']
    # 各模型参数
    if train_config.model_type == Config.TrainConfig.ALGR_TYPE_AR:
        ar_config = Config.ARConfig()
        ar_config.input_window_size = params_dict['input_window_size']
        ar_config.output_window_size = params_dict['output_window_size']
        train_config.ar_config = ar_config
    elif train_config.model_type == Config.TrainConfig.ALGR_TYPE_SE:
        se_config = Config.SEConfig()
        se_config.cycle_num_latent_values = params_dict['cycle_num_latent_values']
        train_config.se_config = se_config
    elif train_config.model_type == Config.TrainConfig.ALGR_TYPE_LSTM:
        lstm_config = Config.LSTMConfig()
        lstm_config.num_units = params_dict['num_units']
        train_config.lstm_config = lstm_config
    train_config.training_steps = train_dict['training_steps']
    train_config.model_dir = train_dict['model_dir']

    return train_config


def parse_evaluation_config(eval_dict):
    eval_config = Config.EvalConfig()
    eval_config.steps = eval_dict['steps']
    return eval_config


def parse_predict_config(predict_dict):
    precidt_config = Config.PredictConfig()
    precidt_config.steps = predict_dict['steps']
    precidt_config.predict_start_time = predict_dict['predict_start_time']
    return precidt_config


def parse_data_config(data_dict):
    """
    解析数据配置
    :param data_dict:
    :return:
    """
    data_config = Config.DataConfig()
    data_config.source_type = data_dict['source_type']

    data_config.metrics = data_dict['metrics']
    data_config.dimensions = data_dict['dimensions']

    if data_config.source_type == Config.DataConfig.SOURCE_TYPE_INFLUXDB:
        influxdb_dict = data_dict['params']
        source_config = Config.InfluxdbConfig()
        source_config.dbname = influxdb_dict['dbname']
        source_config.ip = influxdb_dict['ip']
        source_config.port = influxdb_dict['port']
        source_config.measurement = influxdb_dict['measurement']
        data_config.source_config = source_config
    # todo:解析es config
    elif data_config.source_type == Config.DataConfig.SOURCE_TYPE_ES:
        pass
    return data_config
