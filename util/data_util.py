import numpy as np

import datetime
import pandas as pd
from pandas import Series, DataFrame


def fill_np_none(origin_data):
    return np.where(origin_data, origin_data, 0).astype(np.float32)


def fill_array_none(arr):
    pass


def diff_smooth(data):
    """
    数据平滑处理，首先替换0值和nan值，再替换异常值
    :param data: 原始数据
    :return: 平滑结果
    """
    ts = linspace_zero_or_none(Series(data.reshape(-1).tolist()))
    dif = ts.diff().dropna()  # 差分序列
    td = dif.describe()  # 描述性统计得到：min，25%，50%，75%，max值

    high = td['75%'] + 1.5 * (td['75%'] - td['25%'])  # 定义高点阈值，1.5倍四分位距之外
    low = td['25%'] - 1.5 * (td['75%'] - td['25%'])  # 定义低点阈值，同上

    # 变化幅度超过阈值的点的索引
    forbid_index = dif[(dif > high) | (dif < low)].index
    ts = linspace_indexs(ts, forbid_index)
    return ts.values


def linspace_indexs(data, indexs):
    """
    使用索引两侧边界值填充索引值
    :param data: 原始数据
    :param indexs: 需要填充的索引
    :return: 平滑结果
    """
    i = 0
    while i < len(indexs) - 1:
        n = 1  # 发现连续多少个点变化幅度过大，大部分只有单个点
        start = indexs[i]  # 异常点的起始索引
        while i + n < indexs.size and indexs[i + n] == start + n:
            n += 1
        i += n - 1

        end = indexs[i]  # 异常点的结束索引
        # 用前后值的中间值均匀填充
        value = np.linspace(data[start - 1], data[end + 1], n + 2)
        data[start: end + 1] = value[1:value.size - 1]
        print('{0} {1} {2} {3}'.format(i, n, start, end))
        i += 1
    return data


def linspace_zero_or_none(data):
    """
    处理0值和nan值
    :param data: 原始数据
    :return: 平滑结果
    """
    indexs = data[(data == 0) | (data.isnull())].index
    return linspace_indexs(data, indexs)



