from __future__ import print_function
import numpy as np
import matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.contrib.timeseries.python.timeseries import NumpyReader
from tensorflow.contrib.timeseries.python.timeseries import model_utils
from tensorflow.contrib.timeseries.python.timeseries import feature_keys


def main(_):
    x = np.array(range(1008))
    y = np.array(range(1008))
    labels = np.array(range(1008))
    f = open('../kafka_time_series.txt', 'r')
    i = 0
    for line in f.readlines():
        y[i] = int(line.split(",")[1].strip())
        labels[i] = int(line.split(",")[0].strip())
        i += 1
    f.close()
    data = {
        tf.contrib.timeseries.TrainEvalFeatures.TIMES: x,
        tf.contrib.timeseries.TrainEvalFeatures.VALUES: y,
    }

    reader = NumpyReader(data)

    train_input_fn = tf.contrib.timeseries.RandomWindowInputFn(
        reader, batch_size=16, window_size=60)

    ar = tf.contrib.timeseries.ARRegressor(
        periodicities=144, input_window_size=40, output_window_size=20,
        num_features=1,
        loss=tf.contrib.timeseries.ARModel.NORMAL_LIKELIHOOD_LOSS)

    ar.train(input_fn=train_input_fn, steps=6000)

    evaluation_input_fn = tf.contrib.timeseries.WholeDatasetInputFn(reader)
    # keys of evaluation: ['covariance', 'loss', 'mean', 'observed', 'start_tuple', 'times', 'global_step']
    evaluation = ar.evaluate(input_fn=evaluation_input_fn, steps=1)
    evaluation1 = {'start_tuple': (np.array([range(60, 100, 1)]), np.array([np.ones((40, 1), dtype=np.float32)])),
                  'times': np.array([range(60, 100, 1)])}

    (predictions1,) = tuple(ar.predict(
        input_fn=tf.contrib.timeseries.predict_continuation_input_fn(
            evaluation1, steps=300)))

    evaluation2 = {'start_tuple': (np.array([range(400, 440, 1)]), np.array([np.ones((40, 1), dtype=np.float32)])),
                   'times': np.array([range(400, 440, 1)])}

    (predictions2,) = tuple(ar.predict(
        input_fn=tf.contrib.timeseries.predict_continuation_input_fn(
            evaluation2, steps=300)))

    plt.figure(figsize=(15, 5))
    plt.plot(data['times'].reshape(-1), data['values'].reshape(-1), label='origin')
    plt.plot(evaluation['times'].reshape(-1), evaluation['mean'].reshape(-1), label='evaluation')
    plt.plot(predictions1['times'].reshape(-1), predictions1['mean'].reshape(-1), label='prediction1')
    plt.plot(predictions2['times'].reshape(-1), predictions2['mean'].reshape(-1), label='prediction2')
    plt.xlabel('time_step')
    plt.ylabel('values')
    plt.legend(loc=4)
    plt.savefig('predict_result_csv.png')


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
