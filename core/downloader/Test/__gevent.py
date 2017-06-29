# coding:utf-8

"""
协程示例
python version: 3.5+
"""

# python 3.5+
# import asyncio

# async def cor(i):
#    print("cor {i} start".format(i = i))
#    await asyncio.sleep(1)
#    print("cor {i} finished".format(i = i))

# loop = asyncio.get_event_loop()
# tasks = [cor(i) for i in range(5)]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

import time
import requests
import gevent
import gevent.monkey
gevent.monkey.patch_all()

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
    "Connection": "keep-alive"
}

urls = [
    "http://baidu.com/",
    "http://jd.com/",
    "http://taobao.com",
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
    response = requests.get(url, headers = headers)
    print(response.url)

def main():
    tasks = []
    for url in urls:
        tasks.append(gevent.spawn(Request, url))
    gevent.joinall(tasks)

if __name__ == '__main__':
    startTime = time.time()
    main()
    print(time.time() - startTime)
