# -*- coding:utf-8 -*-
import tensorflow as tf

from config import config_parser
from data import data_parser
from model import model_tools
from output import plot_tools, output_tools


def train(conf):
    """
    训练模型
    1.解析数据配置
    2.解析模型配置
    3.生成数据
    4.训练模型
    :return:
    """
    tfts_data = data_parser.parse_train_data(conf)
    estimator = model_tools.train(data=tfts_data.train_data, config=conf)
    return tfts_data, estimator


def evaluate(tfts_data, conf):
    tfts_data.predict_data = model_tools.evaluate(data=tfts_data.train_data, config=conf)
    return tfts_data


def predict(conf):
    """
    预测
    :return:
    """
    tfts_data = data_parser.parse_predict_data(conf)
    tfts_data.predict_result = model_tools.predict(data=tfts_data.evaluation_data, config=conf)
    return tfts_data


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    config = config_parser.parse_yaml_config("./conf/ar_sample.yaml")

    train(config)

    all_data = data_parser.parse_train_data(config)

    evaluation_data = evaluate(all_data, config)
    # plot_tools.make_plot(all_data.train_data['times'].reshape(-1),
    #                      all_data.train_data['values'].reshape(-1),
    #                      evaluation_data.predict_data['times'].reshape(-1),
    #                      evaluation_data.predict_data['mean'].reshape(-1),
    #                      "eval.png"
    #                      )

    predictions = predict(config)
    # plot_tools.make_plot(all_data.train_data['times'].reshape(-1),
    #                      all_data.train_data['values'].reshape(-1),
    #                      predictions.predict_result['times'].reshape(-1),
    #                      predictions.predict_result['mean'].reshape(-1),
    #                      "predict.png"
    #                      )
    output_tools.data_output(config, predictions)
