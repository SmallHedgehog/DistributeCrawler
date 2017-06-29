# coding: utf-8

"""
解析配置文件
"""

import os
import yaml

# 配置文件路径
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

with open(config_path) as f:
    cont = f.read()

class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        self.attris = yaml.load(cont)

    def getAttris(self):
        """Return self.attris"""
        return self.attris

    @property
    def get_max_tasks(self):
        return self.attris.get('max_tasks', None)

    @property
    def get_max_redirect(self):
        return self.attris.get('max_redirect', None)

    @property
    def get_headers(self):
        return self.attris.get('headers', None)

    @property
    def get_sleep_time(self):
        return self.attris.get('sleep_time', None)

    @property
    def get_cookies(self):
        return self.attris.get('cookies', None)

    @property
    def get_proxies(self):
        return self.attris.get('proxies', None)

    @property
    def get_timeout(self):
        return self.attris.get('time_out', None)

    @property
    def get_redis(self):
        return self.attris.get('redis', None)

if __name__ == '__main__':
    Con = Config()
    print(Con.get_max_tasks)
