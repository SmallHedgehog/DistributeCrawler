# coding:utf-8

"""
将结果输出到控制台
"""

from saver import baseSaver

class ConsoleSaver(baseSaver):
    def __init__(self):
        super(ConsoleSaver, self).__init__()

    def save(self, data):
        """Print data to console"""
        for key in data.keys():
            print(key, ':', data[key])

if __name__ == '__main__':
    data = {
        "name": "hedgehog",
        "age": 21
    }

    consoleSaver = ConsoleSaver()
    consoleSaver.save(data)
