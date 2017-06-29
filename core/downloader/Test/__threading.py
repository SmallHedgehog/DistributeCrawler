# coding:utf-8

"""
多线程示例
"""

import requests
import time
import Queue
import threading

urls = [
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
]

Q = Queue.Queue()

class threadUrl(threading.Thread):
    def __init__(self, Q):
        threading.Thread.__init__(self)
        self.Q = Q

    def run(self):
        while True:
            url = self.Q.get()  # 默认情况下阻塞调用
            response = requests.get(url)
            print(response.url)

            self.Q.task_done()

# 多线程
def main():
    for i in range(10):
        t = threadUrl(Q)
        t.setDaemon(True)
        t.start()

    for url in urls:
        Q.put(url)
    Q.join()

# 单线程
def singleMain():
    for url in urls:
        response = requests.get(url)
        print(response.url)

if __name__ == '__main__':
    # 多线程
    startTime = time.time()
    main()
    print("多线程(s):", time.time() - startTime)

    # 单线程
    startTime = time.time()
    # singleMain()
    print("单线程(s):", time.time() - startTime)
