# coding:utf-8

"""
核心引擎（调度downloader、scheduler、saver相关操作来爬取网页）
规则：
    （1）设置start_urls初始URL集合，regexRules解析URL正则规则，domains域名集合
    （2）核心模块downloader下载器、scheduler调度器、saver存储器、pageProcessor等
    （3）downloader：提供SyncDownloader
            可以编写自定义的downloader，只需继承Downloader类并实现接口方法
        scheduler：提供PriorityScheduler、QueueScheduler、RedisScheduler（分布式调度器）
            可以编写自定义的scheduler，需继承baseScheduler类实现其接口方法
        pageProcessor：提供Processor
            可自定义，需继承Processor并实现其方法
        saver：提供ConsoleSaver
            可以编写自定义的saver，只需继承baseSaver类并实现接口方法
额外功能：
    可以监听线程状态，切换线程状态
"""

__author__ = 'hedgehog'

import time
import os
import threading

from config import Config
from log.logHandler import logHandler
from defines.pUrl import pUrl
from defines.regexRules import regexRules
from core.downloader.SyncDownloader import SyncDownloader
from core.scheduler.QueueScheduler import QueueScheduler
from core.scheduler.redisScheduler.RedisScheduler import redisScheduler
from saver.ConsoleSaver import ConsoleSaver
from parserDoc.pageProcessor import Processor

# record log message
log = logHandler(__name__)

class Spider(object):
    """"""
    current_threadCounts = 0
    def __init__(self, start_urls, domains=None, regexRules=None,
                 downloader=None, scheduler=None, saver=None, pageProcessor=None):
        super(Spider, self).__init__()

        self.start_urls = start_urls
        self.domains = domains
        self.regexRules = regexRules

        self.downloader = downloader or SyncDownloader()
        self.scheduler = scheduler or redisScheduler()
        # 默认将结果输出到控制台
        self.saver = saver or ConsoleSaver()
        self.pageProcessor = pageProcessor or Processor()

        # Prefix start_urls
        for url_idex in range(len(self.start_urls)):
            self.start_urls[url_idex] = self.__fix_urls(self.start_urls[url_idex])

        # Valid URL
        for url in self.start_urls:
            if self.__judge_urls(url):
                # Add init URL collection
                self.scheduler.pushUrl(pUrl(url), 0)

        self.config = Config()
        # Store thread of this Spider
        self.threads = {}

    def __judge_urls(self, url):
        """Judge url whether valid and start_urls' domain whether in domains
        """
        if self.domains is None:
            return True
        items = url.split('.')
        for item in items:
            if item in self.domains:
                return True
        return False

    def __fix_urls(self, url):
        """Fix the url(prefix a schema-less URL with http://)"""
        if '://' not in url:
            url = 'http://' + url
        return url

    def set_attris(self, downloader=None, scheduler=None, saver=None, pageProcessor=None):
        """提供设置downloader、scheduler、saver、pageProcessor的接口"""
        if downloader is not None:
            self.downloader = downloader
        if scheduler is not None:
            self.scheduler = scheduler
        if saver is not None:
            self.saver = saver
        if pageProcessor is not None:
            self.pageProcessor = pageProcessor

    def Run(self):
        """Start launch the Crawler"""
        def __run():
            while True:
                # Check the current thread's status
                thread = self.threads[threading.currentThread().getName()]
                if thread['status'] == 'Stopping':
                    # Finish current thread
                    break
                elif thread['status'] == 'Suspending':
                    # Suspend current thread
                    continue

                URL, _ = self.scheduler.popUrl()
                if URL is None and threading.activeCount() == 2:
                    # Main-thread、Monitor-thread
                    break
                elif URL is None:
                    # Sleep one second
                    time.sleep(1)
                else:
                    print URL.getUrl
                    # step1: download URL
                    document = self.downloader.download(URL)
                    if document:
                        # step2: Get URLs in document
                        urls, document = document.parserLinks()
                        # step3: handle URLs from step2
                        for url in urls:
                            if self.regexRules is None:
                                if self.__judge_urls(url.getUrl):
                                    self.scheduler.pushUrl(pUrl(self.__fix_urls(url.getUrl)), 0)
                            else:
                                if self.regexRules.isMatched(url.getUrl) and self.__judge_urls(url.getUrl):
                                    self.scheduler.pushUrl(pUrl(self.__fix_urls(url.getUrl)), 0)
                        # step4: handle document
                        document = self.pageProcessor.pageParser(document)
                        # step5: save the result from document
                        self.saver.save(document.getItems())
                self.scheduler.done()

                # Exit
                # print "Queue size: ", self.scheduler.getSize()
                # print "threading activeCount: ", threading.activeCount()
                # if self.scheduler.getSize() == 0 and threading.activeCount() == 1:
                #    break

        # Manager threads' status
        def __manager():
            while True:
                command = raw_input('Command> ')
                if command == '-h' or command == '--help':
                    self.__help()
                elif command == '-p' or command == '--print':
                    self.__print()
                elif '-k' in command:
                    try:
                        com, id = command.split(' ')
                        if com == '-k' or com == '--kill':
                            self.__kill(int(id.strip()))
                    except ValueError:
                        pass
                elif '-s' in command:
                    try:
                        com, id = command.split(' ')
                        if com == '-s' or com == '--suspend':
                            self.__suspend(int(id.strip()))
                    except ValueError:
                        pass
                elif '-r' in command:
                    try:
                        com, id = command.split(' ')
                        if com == '-r' or com == '--run':
                            self.__start(int(id.strip()))
                    except ValueError:
                        pass
                elif command == '-a' or command == '--add':
                    t = threading.Thread(target=__run)
                    self.__init_thread(t)
                elif command == 'exit':
                    # Exit process
                    os._exit(-1)

        # Get max tasks from config.yaml file
        tasks = self.config.get_max_tasks
        if tasks is None:
            tasks = 10
        for task in range(tasks):
            self.t = threading.Thread(target=__run)
            self.__init_thread(self.t)

        # Using a thread to monitor and manager thread
        self.monitor = threading.Thread(target=__manager)
        # self.monitor.setDaemon(True)
        self.monitor.start()
        # Join the QUEUE
        self.scheduler.join()
        if isinstance(self.scheduler, redisScheduler):
            self.monitor.join()

    # Manager threads' status
    # -h or --help  Print help info
    # -k or --kill  Kill a thread by its id
    # -r or --run   restart a thread from suspending status
    # -s or --suspend   Suspend a thread by its id
    # -a or --add   Add a new thread
    # -p or --print Print current threads info
    # exit          Exit process
    def __help(self):
        print 'Usage: '
        print '-h or --help\tPrint help info'
        print '-k or --kill\tKill a thread by its id'
        print '-r or --run\t\trestart a thread from suspending status'
        print '-s or --suspend\tSuspend a thread by its id'
        print '-a or --add\t\tAdd a new thread'
        print '-p or --print\tPrint current threads info'
        print 'exit\t\t\tExit process\n'

    def __print(self):
        """Print all threads' information"""
        for key in self.threads.keys():
            print 'name: {name}\tid: {id}\tobject: {object}\tstatus: ' \
                  '{status}'.format(name=key, id=self.threads[key]['id'], object=self.threads[key]['object'], status=
            self.threads[key]['status'])

    def __kill(self, id=None):
        """To kill a thread by its id"""
        if id is not None:
            for key in self.threads.keys():
                if self.threads[key]['id'] == id:
                    if self.threads[key]['status'] != 'Stopping':
                        self.threads[key]['status'] = 'Stopping'

    def __suspend(self, id=None):
        """To Suspend a thread by its id"""
        if id is not None:
            for key in self.threads.keys():
                if self.threads[key]['id'] == id:
                    if self.threads[key]['status'] == 'Running':
                        self.threads[key]['status'] = 'Suspending'

    def __start(self, id=None):
        """To start a thread from suspending status"""
        if id is not None:
            for key in self.threads.keys():
                if self.threads[key]['id'] == id:
                    if self.threads[key]['status'] == 'Suspending':
                        self.threads[key]['status'] = 'Running'

    # def __add(self):
    #    """Add a new thread"""
    #    pass

    def __init_thread(self, thread):
        thread.setName('Spider_thread-{current_num}'.format(current_num=Spider.current_threadCounts))
        self.threads[thread.getName()] = {
            'id': Spider.current_threadCounts,
            'object': thread,
            'status': 'Running'
        }
        Spider.current_threadCounts += 1
        thread.setDaemon(True)
        thread.start()

if __name__ == '__main__':
    urls = [
        'http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm'
    ]

    domains = [
        'xinhuanet'
    ]

    rules = regexRules([
        '(.*?)\d\.htm*'
    ], [
        '(.*?)vedio(.*?)'
    ])

    spider = Spider(start_urls=urls, domains=domains, regexRules=rules)
    spider.Run()

    # print threading.activeCount()
