# -*- coding:utf-8 -*-

import tensorflow as tf


class Config:
    def __init__(self):
        self.data_config = None
        self.train_config = None
        self.eval_config = None
        self.predict_config = None


PERIOD_TYPE_HOUR = "hour"
PERIOD_TYPE_DAY = "day"
PERIOD_TYPE_WEEK = "week"
PERIOD_TYPE_MONTH = "month"


class TrainConfig:
    ALGR_TYPE_AR = "AR"
    ALGR_TYPE_SE = "SE"
    ALGR_TYPE_LSTM = "LSTM"

    def __init__(self):
        self.model_type = None
        self.model_dir = None
        self.num_features = 1
        self.ar_config = None
        self.se_config = None
        self.lstm_config = None
        self.eval_config = None
        self.training_steps = 0
        # 每周期数据量
        self.periodicities = 0
        # 每两数据间隔秒数
        self.period_time_unit = 0
        # reader的batch数
        self.batch_size = 10
        # 读入batch的量
        self.window_size = 60

        self.train_start_time = 0
        self.period_type = PERIOD_TYPE_DAY
        # 周期个数
        self.period_num = 0


class ARConfig:
    def __init__(self):
        self.input_window_size = 0
        self.output_window_size = 0
        self.loss = tf.contrib.timeseries.ARModel.NORMAL_LIKELIHOOD_LOSS


class SEConfig:
    def __init__(self):
        self.cycle_num_latent_values = 0


class LSTMConfig:
    def __init__(self):
        self.num_units = 0
        self.adam_optimizer = 0.001


class EvalConfig:
    def __init__(self):
        self.steps = 1
        self.output_type = None
        self.metrics = None


class PredictConfig:
    def __init__(self):
        self.steps = 0
        self.predict_start_time = 0


"""
数据量 = period_num * periodicities
配置的基本单位是：秒(s)
按照PERIOD_TYPE_换算

"""


class DataConfig:
    SOURCE_TYPE_INFLUXDB = "influxdb"
    SOURCE_TYPE_ES = "es"
    SOURCE_TYPE_FILE = "file"

    def __init__(self):
        self.path = None

        # 数据源类型
        self.source_type = None

        self.source_config = None
        self.metrics = []
        self.dimensions = {}


class InfluxdbConfig():
    def __init__(self):
        self.ip = None
        self.port = 0
        self.username = ''
        self.password = ''
        self.dbname = None
        self.measurement = None


class ESConfig:
    def __init__(self):
        self.ip = None
