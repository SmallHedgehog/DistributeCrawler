# coding: utf-8

"""
封装异常模块
"""

class DependencyNotInstalledError(Exception):
    """依赖模块未安装异常"""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return 'Error because lacking of dependency: %s' % self.msg
