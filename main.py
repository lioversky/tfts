# -*- coding:utf-8 -*-
import tensorflow as tf

from config import config_parser, config_reader
from data import data_parser
from model import model_tools
import sys


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
    tfts_data.evaluation_result = model_tools.evaluate(data=tfts_data.train_data, config=conf)
    return tfts_data


def predict(conf):
    """
    预测
    :return:
    """
    tfts_data = data_parser.parse_predict_data(conf)
    evaluation_result, predictions = model_tools.predict(data=tfts_data.evaluation_data, config=conf)
    tfts_data.evaluation_result = evaluation_result
    tfts_data.predict_result = predictions
    return tfts_data


def main(argv):
    key_name = argv[0]
    etcd_ip = argv[1] if len(argv) > 1 else '127.0.0.1'
    # 读取配置
    config_str = config_reader.read_config(key_name, host=etcd_ip)
    config = config_parser.parse_yaml_str(config_str)


    result = data_parser.parse_train_data(config)
    # result = evaluate(data_parser.parse_train_data(config), config)
    # result = predict(config)


    import matplotlib.pyplot as plot

    plot.figure(figsize=(15, 5))
    plot.plot(result.train_data['times'].reshape(-1), result.train_data['values'].reshape(-1), label='origin')
    # plot.plot(result.evaluation_data['times'].reshape(-1), result.evaluation_data['values'].reshape(-1), label='origin')

    # plot.plot(result.evaluation_result['times'].reshape(-1), result.evaluation_result['mean'].reshape(-1),
    #           label='evaluation')
    # plot.plot(result.predict_result['times'].reshape(-1), result.predict_result['mean'].reshape(-1),
    #           label='prediction')
    # plot.plot(result.predict_result['times'].reshape(-1), result.real_data.reshape(-1),
    #           label='real')
    plot.xlabel('time_step')
    plot.ylabel('values')
    plot.legend(loc=4)
    plot.savefig("mobile-origin1.png")


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    main(sys.argv[1:])

    # train(config)

    # all_data = data_parser.parse_train_data(config)

    # evaluation_data = evaluate(all_data, config)
    # plot_tools.make_plot(all_data.train_data['times'].reshape(-1),
    #                      all_data.train_data['values'].reshape(-1),
    #                      evaluation_data.predict_data['times'].reshape(-1),
    #                      evaluation_data.predict_data['mean'].reshape(-1),
    #                      "eval.png"
    #                      )

    # predictions = predict(config)
    # plot_tools.make_plot(all_data.train_data['times'].reshape(-1),
    #                      all_data.train_data['values'].reshape(-1),
    #                      predictions.predict_result['times'].reshape(-1),
    #                      predictions.predict_result['mean'].reshape(-1),
    #                      "predict.png"
    #                      )
    # output_tools.data_output(config, predictions)
