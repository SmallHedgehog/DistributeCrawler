# coding: utf-8

"""
Using qr(https://github.com/tnm/qr) to operate redis
分布式：
    （1）在Redis中初始化两条key-value数据，对应的key分别为spider.wait和spider.all
    （2）spider.wait的value是一个list队列，存放我们待抓取的URL，该数据类型方便我们实现
消息队列，我们使用lpush操作添加URL数据，同时使用brpop监听并获取URL数据。
    （3）spider.all的value是一个集合，存放我们所有待抓取和已抓取的URL，该数据类型方便
我们实现排重操作，使用sadd操作添加数据。
"""

import qr
import redis

class RedisQueue(object):
    def __init__(self, name, namsapce=''):
        self.__db = redis.Redis(host='120.95.132.153', port=6379, db=0)
        self.key = '%s%s' % (namsapce, name)

    def push(self, item):
        self.__db.lpush(self.key, item)

    def get(self, block=True, timeout=None):
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)
        return item

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

class qr_redisQueue(object):
    def __init__(self, key):
        self.queue = qr.Queue(key, host='120.95.132.153', port=6379)
        self.key = key

    def push(self, item):
        self.queue.push(item)

    def get(self):
        return self.queue.pop()

    def elements(self):
        return self.queue.elements()

    def qsize(self):
        return len(self.queue)

if __name__ == '__main__':
    # Q = RedisQueue('hedgehog')
    # Q.push('1')
    # Q.push('2')
    # Q.push('3')
    # print Q.qsize()

    q = qr_redisQueue('key')
    q.push('1')
    q.push('2')

    print q.elements()
    print q.qsize()
    print q.get()
    print q.get()
    print q.get()
