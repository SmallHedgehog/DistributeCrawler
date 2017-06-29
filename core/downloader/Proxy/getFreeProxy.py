# coding:utf-8

"""
获取免费的IP代理（url: http://www.66ip.cn/）
"""

__author__ = 'hedgehog'

import random
import re
import requests
from log.logHandler import logHandler
from lxml import etree

userAgents = [
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

class getFreeProxy(object):
    def __init__(self):
        self.headers = {
            "User-Agent": random.choice(userAgents)
        }
        self.log = logHandler(__name__)

    # 检查IP代理格式
    def __verifyProxy(self, proxy):
        verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
        return True if re.findall(verify_regex, proxy) else False

    # 获取一个可用的免费IP代理
    def validProxy(self):
        """
         url: http://www.66ip.cn/
        """
        url = 'http://www.66ip.cn/areaindex_1/1.html'

        response = requests.get(url=url, headers=self.headers)
        htmlDoc = response.content.decode('gbk')

        htmlTree = etree.HTML(htmlDoc)
        proxy_list = htmlTree.xpath('.//table//tr')
        for proxy in proxy_list:
            proxies = ':'.join(proxy.xpath('./td/text()')[0:2])
            if self.__verifyProxy(proxies):
                if self.__isVaildProxy(proxies):
                    return {
                        "https": "https://{proxy}".format(proxy = proxies)
                    }
        return None

    # 检查IP代理是否可用
    def __isVaildProxy(self, proxy):
        proxies = {
            "https": "https://{proxy}".format(proxy = proxy)
        }
        try:
            # 有效代理IP地址（请求在2秒内）
            response = requests.get('http://www.baidu.com/', proxies = proxies, timeout = 2, verify = False)
            if response.status_code == 200:
                return True
        except Exception as e:
            self.log.error(proxy + "\tinvalid")
            return False

if __name__ == '__main__':
    print(getFreeProxy().validProxy())
