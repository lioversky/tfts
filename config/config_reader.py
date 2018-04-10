# -*- coding:utf-8 -*-

import etcd


def read_config(key):
    client = etcd.Client(host='127.0.0.1', port=4003)
    config_result = client.read(key)
    print(config_result.value)
