# -*- coding:utf-8 -*-
"""
整个过程的数据

"""


class TFTSData:
    """
    train_times、evaluation_times、predict_times 为时间原始数据
    train_data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
    }

    """

    def __init__(self):
        # 训练样本数据
        self.train_data = None
        # 训练样本数据对应时间
        self.train_times = None
        # 验证数据，在预测时获取
        self.evaluation_times = None
        self.evaluation_data = None
        self.evaluation_result = None
        # 预测时间
        self.predict_times = None
        # 预测结果
        self.predict_result = None
        # 真实结果
        self.real_data = None

