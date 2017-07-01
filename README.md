# DistributeCrawler
分布式爬虫（using Python2.7），自制框架

## 系统特点
* 代码结构良好，易读易用，自定义爬虫简单
* 高度可扩展性，热插拔各组件，系统提供多个组件可选，支持自定义组件
* 速度快，多线程，分布式（提供配置文件支持）
* 反爬虫，支持模拟浏览器、IP代理（更换IP代理、IP代理池）、Cookies等反爬虫策略
* 动态监控爬虫状态，支持爬虫线程能在三种状态（Running、Stopping、Suspending）之间转换，可以随时添加爬虫线程等
* 故障重爬，支持断电、宕机后继续爬取
* 可自定义爬虫，只需要实现存储器（saver）和网页内容提取（pageProcessor）即可

## 系统完善功能
* 分布式策略，系统目前使用redis做分布式调度器，redis服务器只在master主机上，worker主机从master主机上取任务，这样如果master主机故障，系统就瘫痪，不稳定
* 自动切换IP代理，系统主要维护一个免费的IP代理池，可用性不高
* 提供界面支持，监控爬虫线程、分布式中的worker主机爬虫状态等

## 系统流程图
![系统流程图](https://ooo.0o0.ooo/2017/07/01/595776538eee5.png)

## 简单例子
使用本系统爬去新华社网新闻的标题，在使用本系统定制爬虫时，只需提供一下内容：
1. 入口URLs集合、域名domains集合
2. URL提取规则
3. 网页内容提取（pageProcessor），系统默认实现是什么也不做
4. 存储器（saver），系统默认实现是输出到终端

#### 爬去新华社网新闻的标题

```python
    # coding: utf-8
    from defines.regexRules import regexRules
    from saver import baseSaver
    from parserDoc.pageProcessor import Processor
    from core.Spider import Spider
    
    # 提供自定义的saver
    class mySaver(baseSaver):
        """"""
        def __init__(self):
            super(mySaver, self).__init__()

        def save(self, data):
            """Print to console"""
            for key in data.keys():
                print key, data[key]

    # 提供自定义的网页内容提取
    class myProcessor(Processor):
        """"""
        def __init__(self):
            super(myProcessor, self).__init__()

        def pageParser(self, document):
            # htmlDoc is BeautifulSoup object
            htmlDoc = document.getParserDoc()
            try:
                title = htmlDoc.title.string
                document.setItems('title', title)
            except:
                pass
            return document

        def setUrlPriority(self, urls):
            pass

    if __name__ == '__main__':
        # 初始URLs集合
        urls = ['http://news.xinhuanet.com/politics/2017-05/16/c_1120982109.htm']
        # URL域名集合
        domains = ['xinhuanet']
        # URL提取规则
        rules = regexRules(['(.*?)\d\.htm*'], ['(.*?)vedio(.*?)'])

        # 开始
        Spider(start_urls=urls, domains=domains, regexRules=rules, pageProcessor=myProcessor(), saver=mySaver()).Run()
```
