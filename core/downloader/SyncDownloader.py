#coding: utf-8

"""
同步下载器
"""

from core.downloader import Downloader
from core.downloader.Net import net
from parserDoc.parserDoc import Document
from defines.pUrl import pUrl

class SyncDownloader(Downloader):
    def __init__(self):
        super(SyncDownloader, self).__init__()

    def download(self, pUrl):
        htmlDoc = net.getInstance().get(pUrl.getUrl)
        document = None
        if htmlDoc is not None:
            document = Document(pUrl, htmlDoc)

        return document


if __name__ == '__main__':
    print SyncDownloader().download(pUrl('http://www.baidu.com'))
