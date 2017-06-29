# coding:utf-8

"""
优先级调度器
"""

import threading
import Queue
from core.scheduler import baseScheduler

class PriorityShceduler(baseScheduler):
    def __init__(self):
        # 使用queue.PriorityQueuue()实现优先级调度器
        self.__priorityQueue = Queue.PriorityQueue()
        super(baseScheduler, self).__init__()
        # 去除重复URL
        self.__Set = set()
        self.lock = threading.RLock()

    def pushUrl(self, pUrl, max_redirect):
        if pUrl.vaildUrl():
            if pUrl.getUrl not in self.__Set:
                self.__priorityQueue.put_nowait((pUrl, max_redirect))
                self.lock.acquire()
                self.__Set.add(pUrl.getUrl)
                self.lock.release()

    def popUrl(self):
        pUrl = (None, None)
        try:
            pUrl = self.__priorityQueue.get_nowait()
        except Queue.Empty:
            pass
        return pUrl

    def done(self):
        self.__priorityQueue.task_done()

    def isEmtpy(self):
        return self.__priorityQueue.empty()

    def getSize(self):
        return self.__priorityQueue.qsize()

    def join(self):
        self.__priorityQueue.join()

if __name__ == '__main__':
   pass