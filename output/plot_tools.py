

import matplotlib.pyplot as plot


def make_plot(origin_times, origin_data, evaluation_times,evaluation_data,image_name):
    """Plot a time series in a new figure."""
    plot.figure(figsize=(15, 5))
    plot.plot(origin_times, origin_data, label='origin')
    plot.plot(evaluation_times, evaluation_data, label='evaluation')
    plot.xlabel('time_step')
    plot.ylabel('values')
    plot.legend(loc=4)
    plot.savefig(image_name)
