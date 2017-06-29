# coding:utf-8

"""
实现队列调度器
"""

import threading
import Queue
from core.scheduler import baseScheduler

class QueueScheduler(baseScheduler):
    def __init__(self):
        # 使用queue.Queue实现队列
        self.__Queue = Queue.Queue()
        super(QueueScheduler, self).__init__()
        # 去除重复URL
        self.__Set = set()
        self.lock = threading.RLock()

    def pushUrl(self, pUrl, max_redirect):
        if pUrl.vaildUrl():
            if pUrl.getUrl not in self.__Set:
                self.__Queue.put_nowait((pUrl, max_redirect))
                self.lock.acquire()
                self.__Set.add(pUrl.getUrl)
                self.lock.release()

    def popUrl(self):
        pUrl = (None, None)
        try:
            pUrl = self.__Queue.get_nowait()
        except Queue.Empty:
            pass
        return pUrl

    def done(self):
        self.__Queue.task_done()

    def isEmpty(self):
        return self.__Queue.empty()

    def getSize(self):
        return self.__Queue.qsize()

    def join(self):
        self.__Queue.join()
