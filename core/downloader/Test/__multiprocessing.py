# coding:utf-8

"""
多进程示例
"""

import requests
import time
from multiprocessing.dummy import Pool
import multiprocessing

urls = [
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm',
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=1",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=2",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=3",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=4",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=5",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=6",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=7",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=8",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=9",
        "http://tieba.baidu.com/f/index/forumpark?pcn=%E5%A8%B1%E4%B9%90%E6%98%8E%E6%98%9F&pci=0&ct=1&rn=20&pn=10"
]

def Request(url):
    response = requests.get(url)
    print(response.url)

def main():
    pool = Pool(multiprocessing.cpu_count())
    for url in urls:
        pool.apply(Request, (url, ))
    # pool.map(Request, urls)
    pool.close()
    pool.join()

if __name__ == '__main__':
    startTime = time.time()
    main()
    print(time.time() - startTime)
