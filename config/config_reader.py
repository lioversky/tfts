# -*- coding:utf-8 -*-

import etcd


def read_config(key):
    client = etcd.Client(host='127.0.0.1', port=2379)
    config_result = client.read(key)
    print(config_result.value)


if __name__ == '__main__':
    read_config('message')
