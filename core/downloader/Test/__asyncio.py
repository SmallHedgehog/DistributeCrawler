# coding:utf-8

"""
asyncio + aiohttp测试
"""

import asyncio
import aiohttp
import time
from collections import namedtuple

urls = [
    "http://baidu.com/",
    "https://jd.com/",
    "https://taobao.com",
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

asyncQueue = asyncio.Queue()
loop = asyncio.get_event_loop()
url_node = namedtuple("url_node", ["url"])

for url in urls:
    asyncQueue.put_nowait(url_node(url))

session = aiohttp.ClientSession(loop=loop)
async def fetch(url):
    return await session.get(url)

async def Start():
    gevent_workers = [asyncio.Task(gevent_work(), loop=loop)
                      for _ in range(100)]
    startTime = time.time()
    await asyncQueue.join()
    print(time.time() - startTime)
    for worker in gevent_workers:
        worker.cancel()

async def gevent_work():
    try:
        while True:
            urlNode = await asyncQueue.get()
            print(urlNode.url)

            try:
                response = await fetch(urlNode.url)
                print(response.status)
            finally:
                await response.release()

            asyncQueue.task_done()
    except asyncio.CancelledError:
        pass

if __name__ == '__main__':
    loop.run_until_complete(Start())
    loop.close()
    session.close()
