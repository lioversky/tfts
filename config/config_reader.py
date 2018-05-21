# -*- coding:utf-8 -*-

import etcd


def read_config(key, host):
    try:
        client = etcd.Client(host=host, port=2379)
        config_result = client.read(key)
        return config_result.value
    finally:
        pass
