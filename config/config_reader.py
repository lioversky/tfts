# -*- coding:utf-8 -*-

import etcd


def read_config(key, host):
    try:
        client = etcd.Client(host=host, port=2379)
        config_result = client.read(key)
        return config_result.value
    finally:
        pass


def write(value):
    client = etcd.Client(host='127.0.0.1', port=2379)
    client.write(key='tfts/streaming_rcv_hot', value=value)


if __name__ == '__main__':
    lines = []
    f = open('../conf/streaming_rcv_hot.yaml', 'r')

    for line in f.readlines():
        lines.append(line)
    f.close()
    write(value="".join(lines))
    print(read_config("tfts/streaming_rcv_hot", host='127.0.0.1'))
