# coding:utf-8

"""
优先级url（赋予每个url一个优先级，以实现调度策略）
"""

class pUrl(object):
    def __init__(self, url):
        # url priority
        self.priority = 0
        self.url = url

    def setUrl(self, url):
        self.url = url

    def setPriority(self, priority):
        self.priority = priority

    @property
    def getUrl(self):
        return self.url

    @property
    def getPriority(self):
        return self.priority

    def vaildUrl(self):
        if self.url == "" or self.url.strip() == "#"\
                or 'javascript:' in self.url.strip():
            return False
        else:
            return True

    # 实现__cmp__方法（实现优先级调度器时，需要提供__cmp__方法）
    def __cmp__(self, other):
        return self.__lt__(other)

    def __lt__(self, other):
        return self.priority > other.priority
