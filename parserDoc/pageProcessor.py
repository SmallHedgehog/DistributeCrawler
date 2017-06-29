# coding:utf-8

"""
将HTML文档解析成document
document规则：
    （1）HTML文档的pUrl信息
    （2）将HTML文档解析成bs4.BeautifulSoup对象
    （3）存储HTML文档中的新链接
    （4）存储解析出的信息
"""

from bs4 import BeautifulSoup
from defines.pUrl import pUrl
from log.logHandler import logHandler

# 日志记录
log = logHandler(__name__)

class Document(object):
    def __init__(self, URL=None, htmlDoc=None):
        super(Document, self).__init__()
        self.pUrl = URL
        self.parserDoc = BeautifulSoup(htmlDoc, 'lxml')
        self.newUrls = []
        self.items = {}
        # 清除重复的URL
        # self.__Set = set()

    def parserLinks(self):
        links = []
        __Set = set()
        try:
            tagsOfa = self.parserDoc.select('a')
            for info in tagsOfa:
                if 'href' not in info.attrs:
                    continue
                url, sign = self.__fixUrl(info.attrs['href'])
                if sign:
                    if url not in __Set:
                        __Set.add(url)
                        links.append(pUrl(url))
        except Exception as error:
            log.error('parser htmlDoc(%r) ERROR:%r', self.pUrl.getUrl, error)

        return links, self

    def __fixUrl(self, url):
        """Prefix a schema-less URL with http://"""
        sign = True
        if 'javascript:' in url:
            sign = False
        else:
            if url.startswith('//'):
                url = url[2:]
            if '://' not in url:
                url = 'http://' + url
        return url, sign

    def setNewUrls(self, newUrls):
        self.newUrls = newUrls
        return self

    def getItems(self):
        return  self.items

if __name__ == '__main__':
    import requests

    url = "http://news.nwsuaf.edu.cn/yxxw/75964.htm"
    htmlDoc = requests.get(url).text
    for URL in Document(pUrl(url), htmlDoc).parserLinks():
        print(URL.getUrl)
