# -*- coding:utf-8 -*-
import tensorflow as tf

from config import config_parser, config_reader
from data import data_parser
from model import model_tools
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from util import time_util

scheduler = BlockingScheduler()


def evaluate(tfts_data, conf):
    tfts_data.predict_data = model_tools.evaluate(data=tfts_data.train_data, config=conf)
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
    print_result(tfts_data)
    return tfts_data


def print_result(tfts):
    predicts = tfts.predict_result['mean'].reshape(-1)
    reals = tfts.real_data.reshape(-1)
    print()


def main(argv):
    key_name = argv[0]
    etcd_ip = argv[1] if len(argv) > 1 else '127.0.0.1'
    # 读取配置
    config_str = config_reader.read_config(key_name, host=etcd_ip)
    config = config_parser.parse_yaml_str(config_str)
    # 按预测间隔生成定时任务
    interval = time_util.get_config_time_seconds(config.predict_config.predict_interval)
    scheduler.add_job(predict, args=[config], trigger='cron', second='*/10')
    scheduler.start()


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    main(sys.argv[1:])