# -*- coding:utf-8 -*-

from __future__ import print_function
import tensorflow as tf
from model import LSTMModel
from tensorflow.contrib.timeseries.python.timeseries import estimators as ts_estimators
from config import config_model
from tensorflow.contrib.timeseries.python.timeseries import NumpyReader


def train(data, config):
    """
    训练并验证模型
    :param data: 训练数据
    :param config: 配置
    :return: 验证值
    """
    reader = NumpyReader(data)
    train_config = config.train_config
    estimator = create_estimator(train_config)

    train_input_fn = tf.contrib.timeseries.RandomWindowInputFn(
        reader, batch_size=train_config.batch_size, window_size=train_config.window_size)
    estimator.train(input_fn=train_input_fn, steps=train_config.training_steps)

    return estimator


def evaluate(data, config, estimator=None):
    """
    评估模型，生成评估结果
    :param data:
    :param config:
    :param estimator:
    :return:
    """
    reader = NumpyReader(data)
    train_config = config.train_config
    eval_config = config.eval_config
    if estimator is None:
        estimator = create_estimator(train_config)

    evaluation_input_fn = tf.contrib.timeseries.WholeDatasetInputFn(reader)
    evaluation = estimator.evaluate(input_fn=evaluation_input_fn, steps=eval_config.steps)

    return evaluation


def predict(data, config):
    """
    预测
    :param data: evaluation后的数据
    :param config: 配置
    :return: 预测结果
    """
    # 加载模型
    train_config = config.train_config
    estimator = create_estimator(train_config)

    # 获取评估结果
    evaluation = evaluate(data, config)
    # 预测
    predict_config = config.predict_config
    input_fn = tf.contrib.timeseries.predict_continuation_input_fn(
        evaluation, steps=predict_config.steps)
    (predictions,) = tuple(estimator.predict(input_fn))

    return predictions


def create_estimator(train_config):
    if train_config.model_type == config_model.TrainConfig.ALGR_TYPE_AR:
        ar_config = train_config.ar_config
        estimator = tf.contrib.timeseries.ARRegressor(
            periodicities=train_config.periodicities, input_window_size=ar_config.input_window_size,
            output_window_size=ar_config.output_window_size, num_features=train_config.num_features,
            loss=ar_config.loss, model_dir=train_config.model_dir)
        estimator.evaluate
    elif train_config.model_type == config_model.TrainConfig.ALGR_TYPE_SE:
        se_config = train_config.se_config
        estimator = tf.contrib.timeseries.StructuralEnsembleRegressor(
            periodicities=train_config.periodicities, num_features=train_config.num_features,
            model_dir=train_config.model_dir,
            cycle_num_latent_values=se_config.cycle_num_latent_values)
    elif train_config.model_type == config_model.TrainConfig.ALGR_TYPE_LSTM:
        lstm_config = train_config.lstm_config
        estimator = ts_estimators.TimeSeriesRegressor(
            model=LSTMModel.LSTMModel(num_features=train_config.num_features, num_units=lstm_config.num_units),
            model_dir=train_config.model_dir,
            optimizer=tf.train.AdamOptimizer(lstm_config.adam_optimizer))
    return estimator
