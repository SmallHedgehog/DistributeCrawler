# coding:utf-8

"""
基于Redis实现分布式调度策略
"""

from log.logHandler import logHandler
from config import Config
from defines.pUrl import pUrl
from core.scheduler import baseScheduler
from core.scheduler.redisScheduler import Queue as redisQueue
from core.scheduler.redisScheduler import PriorityQueue

# 日志记录
log = logHandler(__name__)

class redisScheduler(baseScheduler):
    def __init__(self):
        super(redisScheduler, self).__init__()
        self.redis_attris = Config().get_redis
        self.unique_set = self.redis_attris['uniqueSet']
        self.qtype = self.redis_attris['type']
        if self.qtype == 'q':
            # Queue
            self.__Queue = redisQueue(self.redis_attris['urlQueue'],
                                      host=self.redis_attris['host'],
                                      port=self.redis_attris['port'],
                                      password=None if self.redis_attris['password'] == '' else self.redis_attris['password'])
        elif self.qtype == 'p':
            # Priority Queue
            self.__Queue = PriorityQueue(self.redis_attris['urlQueue'],
                                         host=self.redis_attris['host'],
                                         port=self.redis_attris['port'],
                                         password=None if self.redis_attris['password'] == '' else self.redis_attris['password'])
        else:
            raise ValueError

    def pushUrl(self, pUrl, max_redirect):
        """Push the pUrl into redisQueue"""
        if pUrl.vaildUrl():
            # 去重操作
            try:
                if self.__Queue.sismember(self.unique_set, pUrl.getUrl):
                    pass
                else:
                    self.__Queue.sadd(self.unique_set, pUrl.getUrl)
                    if self.qtype == 'p':
                        self.__Queue.push(pUrl.getUrl, pUrl.getPriority)
                    elif self.qtype == 'q':
                        self.__Queue.push(pUrl.getUrl)
            except Exception as error:
                log.info('redisScheduler.RedisScheduler.pushUrl ERROR(reason: %s)', error)

    def popUrl(self):
        """Pop the URL from redisQueue"""
        url = None
        score = 0
        try:
            if self.qtype == 'q':
                url = self.__Queue.pop()
            elif self.qtype == 'p':
                url, score = self.__Queue.pop(withscores=True)
        except Exception as error:
            log.info('redisScheduler.RedisScheduler.popUrl ERROR(reason: %s)', error)

        return pUrl(url, score), None

    def done(self):
        pass

    def getSize(self):
        """Get redisQueue size from redis server"""
        return self.__Queue.getSize()

    def isEmpty(self):
        """Judge redisQueue whether is empty"""
        return self.__Queue.getSize() == 0

    def join(self):
        pass

if __name__ == '__main__':
    r = redisScheduler()
    r.pushUrl(pUrl('www'), 0)
    print r.popUrl().getUrl
