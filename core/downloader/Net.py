# coding: utf-8

"""
网络请求模块
"""

import random
import time
import urllib2
import socket

from config import Config
from Opener import builtinOpener
from log.logHandler import logHandler

log = logHandler(__name__)

__user_agent = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

def getHeaders():
    return {
        'User-agent': random.choice(__user_agent),
        'Accept': '*/*',
        'Connection': 'keep-alive',
        # 'Accept-Encoding': 'gzip, deflate'
    }

class net(object):
    def __init__(self):
        super(net, self).__init__()
        # 存储配置参数
        self.config = Config()
        self.opener = builtinOpener(cookie_filename=self.config.get_cookies, timeout=self.config.get_timeout)
        # Add proxies
        if self.config.get_proxies is not None:
            self.opener.add_proxy(random.choice(self.config.get_proxies))
        # Add headers
        if self.config.get_headers is not None:
            self.opener.add_header(self.config.get_headers)
        else:
            self.opener.add_header(getHeaders())

    @staticmethod
    def getInstance():
        """Get instance of net"""
        return net()

    def get(self, url):
        """Fetch url to get html document by self.opener"""
        htmlDoc = None
        if url == None:
            return htmlDoc
        url = url.strip()
        if url == '' or not url.startswith('http'):
            return htmlDoc

        try:
            # sleep time
            if self.config.get_sleep_time is not None:
                time.sleep(self.config.get_sleep_time)
            htmlDoc = self.opener.open(url)
        except urllib2.HTTPError as error:
            code = error.code
            try:
                error_reason = error.read()
            except Exception as error:
                error_reason = error
            if code == 400:
                log.info("400 Error(请求参数出错!) reason: %r url: %r", error_reason, url)
            elif code == 403:
                log.info("403 Error(资源不可使用!) reason: %r url: %r", error_reason, url)
            elif code == 404:
                log.info("404 Error(无法找到指定资源地址!) reason: %r url: %r", error_reason, url)
            elif code == 503:
                log.info("503 Error(服务不可使用!) reason: %r url: %r", error_reason, url)
            elif code == 504:
                log.info("504 Error(网关超时!) reason: %r url: %r", error_reason, url)
            else:
                log.info("%r Error reason: %r url: %r", code, error_reason, url)
            htmlDoc = None
        except urllib2.URLError as error:
            if isinstance(error.reason, socket.timeout):
                log.info("TimeoutError(reason: %r) url: %r", error.reason, url)
            else:
                log.info("URLError(reason: %r) url: %r", error.reason, url)
            htmlDoc = None
        except Exception as error:
            log.info("Error(reason: %r) url: %r", error, url)
            htmlDoc = None

        return htmlDoc

if __name__ == '__main__':
    print net.getInstance().get("http://www.baidu.com")
