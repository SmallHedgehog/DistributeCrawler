# coding: utf-8

"""
新闻类网页正文提取模块
"""

import re

class regular(object):
    re_body = re.compile(r'<body.*?>([\s\S]*?)<\/body>', re.I)
    re_comm = r'<!--.*?-->'
    re_trim = r'<{0}.*?>([\s\S]*?)<\/{0}>'
    re_tags = r'<[\s\S]*?>|[ \t\r\f\v]'
    re_imgs = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')

class textExtractor(object):
    """新闻类网页正文提取"""
    def __init__(self, page=None, blockSize=3, image=False):
        super(textExtractor, self).__init__()

        self.page = page
        self.blockSize = blockSize
        self.saveImage = image
        self.ctexts = []
        self.cblocks = []

    def getContext(self):
        """Get text"""
        self.body = re.findall(regular.re_body, self.page)[0]
        if self.saveImage:
            self.processImages()
        self.processTags()
        return self.processBlocks()

    def processImages(self):
        """Process images"""
        self.body = regular.re_imgs.sub(r'{{\1}}', self.body)

    def processTags(self):
        """Process tags"""
        self.body = re.sub(regular.re_comm, "", self.body)
        self.body = re.sub(regular.re_trim.format("script"), "" ,re.sub(regular.re_trim.format("style"), "", self.body))
        self.body = re.sub(regular.re_tags, "", self.body)

    def processBlocks(self):
        self.ctexts   = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]

        self.cblocks  = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x,y: x+y, self.textLens[i : lines-1-self.blockSize+i], self.cblocks))

        maxTextLen = max(self.cblocks)

        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1

        return "".join(self.ctexts[self.start:self.end])

