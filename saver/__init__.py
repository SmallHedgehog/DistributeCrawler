# coding:utf-8

"""
存储模块：将pageProcessor模块中处理的结果序列化
"""

class baseSaver(object):
    def __init__(self):
        super(baseSaver, self).__init__()

    def save(self, data):
        """Save"""
        raise NotImplementedError
        
