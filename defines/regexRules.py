# coding:utf-8

"""
定义正则规则（url提取规则）
"""

__author__ = 'hedgehog'

import re

class regexRules(object):
    """rules全部匹配，nRules全不匹配"""
    def __init__(self, rules, nRules):
        super(regexRules).__init__()
        # URL正则规则
        self.rules = rules
        self.nRules = nRules

    def addRules(self, rules, nRules):
        """增加URL正则规则"""
        if self.rules is not None:
            self.rules.append(rules)
        if self.nRules is not None:
            self.nRules.append(nRules)

    def setRules(self, rule_list, nRules_list):
        """设置URL正则规则"""
        self.rules = rule_list
        self.nRules = nRules_list

    def __empty(self):
        """判断self.rules是否为空"""
        if len(self.rules)==0 and len(self.nRules)==0:
            return True
        return False

    def isMatched(self, url):
        """判断url是否匹配成功"""
        if self.__empty():
            return True
        if self.rules is not None:
            for pattern in self.rules:
                if re.match(pattern, url) is None:
                    return False
        if self.nRules is not None:
            for pattern in self.nRules:
                if re.match(pattern, url) is not None:
                    return False
        return True

if __name__ == '__main__':
    urlRules = regexRules([
        'http://'
    ], 'http://')

    if urlRules.isMatched('http://www.baidu.com/'):
        print('True')
    else:
        print('False')
