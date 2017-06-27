# coding: utf-8

"""
下载器公共接口
规则：
    接口：download(pUrl)
    返回值：parserDoc.parserDoc对象
"""

class Downloader(object):
    def __init__(self):
        super(Downloader, self).__init__()

    def download(self, pUrl):
        """"""
        raise NotImplementedError
    
