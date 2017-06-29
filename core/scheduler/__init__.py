# coding:utf-8

"""
基类调度器，提供两种方法（push url和pop url），
基类可以重新这两种方法以提供具体的（push url 和pop url）操作
"""

__author__ = 'hedgehog'


class baseScheduler(object):
    def __init__(self):
        pass

    # push方法
    def pushUrl(self, pUrl, max_redirect):
        raise NotImplementedError

    # pop 方法
    def popUrl(self):
        raise NotImplementedError

    # task done func
    def done(self):
        raise NotImplementedError

    # join func
    def join(self):
        raise NotImplementedError
