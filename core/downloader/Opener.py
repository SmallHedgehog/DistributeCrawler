# coding: utf-8

"""
网络请求模块
"""

import socket
import gzip
import urllib2
import cookielib

from core.errors import DependencyNotInstalledError

class Opener(object):
    def open(self, url):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def ungzip(self, fileobj):
        gz = gzip.GzipFile(fileobj=fileobj, mode='rb')
        try:
            return gz.read()
        finally:
            gz.close()

class builtinOpener(Opener):
    def __init__(self, cookie_filename=None, timeout=None, **kwargs):
        self.cj = cookielib.LWPCookieJar()
        if cookie_filename is not None:
            self.cj.load(cookie_filename)
        self.cookie_processor = urllib2.HTTPCookieProcessor(self.cj)
        self.__build_opener()
        urllib2.install_opener(self.opener)

        if timeout is None:
            # self._default_timeout = socket._GLOBAL_DEFAULT_TIMEOUT
            # Set default timeout
            self._default_timeout = 5
        else:
            self._default_timeout = timeout

    def __build_opener(self):
        """Build opener"""
        self.opener = urllib2.build_opener(self.cookie_processor, urllib2.HTTPHandler)

    def open(self, url, data=None, timeout=None):
        if timeout is None:
            timeout = self._default_timeout

        resp = urllib2.urlopen(url, data=data, timeout=timeout)
        # print resp.getcode()
        is_gzip = resp.headers.get('content-encoding') == 'gzip'
        if is_gzip:
            return self.ungzip(resp)
        self.content = resp.read()
        return self.content

    def read(self):
        """Return content"""
        return self.content if hasattr(self, 'content') else None

    def add_header(self, headers):
        """Add headers"""
        self.opener.addheaders = [(key, headers[key]) for key in headers.keys()]
        urllib2.install_opener(self.opener)

    def add_proxy(self, addr, proxy_type='all',
                  user=None, password=None):
        """Add proxy"""
        if proxy_type == 'all':
            self.proxies = {
                'http': addr,
                'https': addr,
                'ftp': addr
            }
        else:
            self.proxies[proxy_type] = addr
        proxy_handler = urllib2.ProxyHandler(self.proxies)
        self.__build_opener()
        self.opener.add_handler(proxy_handler)

        if user and password:
            pwd_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
            pwd_manager.add_password(None, addr, user, password)
            proxy_auth_handler = urllib2.ProxyBasicAuthHandler(pwd_manager)
            self.opener.add_handler(proxy_auth_handler)

        urllib2.install_opener(self.opener)

    def remove_proxy(self):
        """Remove proxies from opener"""
        self.__build_opener()
        urllib2.install_opener(self.opener)

class mechanizeOpener(Opener):
    def __init__(self, cookie_filename=None, user_agent=None, timeout=None, **kwargs):
        try:
            import mechanize
        except ImportError:
            raise DependencyNotInstalledError('mechanize')

        if user_agent is None:
            user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'

        self.browser = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()
        if cookie_filename is not None:
            self.cj.load(cookie_filename)
        self.browser.set_cookiejar(self.cj)
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_gzip(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [
            ('User-agnet', user_agent)
        ]

        if timeout is None:
            # self._default_timout = mechanize._sockettimeout._GLOBAL_DEFAULT_TIMEOUT
            self._default_timout = 5
        else:
            self._default_timout = timeout

    def set_default_timeout(self, timeout):
        self._default_timout = timeout

    def open(self, url, data=None, timeout=None):
        """Request the url"""
        self._clear_content()
        if timeout is None:
            timeout = self._default_timout
        self.content = self.browser.open(url, data=data, timeout=timeout).read()

        return self.content

    def add_proxy(self, addr, proxy_type='all',
                  user=None, password=None):
        """Add proxies"""
        if proxy_type == 'all':
            self.proxies = {
                'http': addr,
                'https': addr,
                'ftp': addr
            }
        else:
            self.proxies[proxy_type] = addr
        self.browser.set_proxies(proxies=self.proxies)
        if user and password:
            self.browser.add_proxy_password(user, password)

    def remove_proxy(self):
        """Remove proxies"""
        self.browser.set_proxies({})
        self.proxies = {}

    def read(self):
        if hasattr(self, 'content'):
            return self.content
        elif self.browser.response() is not None:
            self.content = self.browser.response().read()
            return self.content
        else:
            return None

    def _clear_content(self):
        """Clear the self.content"""
        if hasattr(self, 'content'):
            del self.content

    def close(self):
        self._clear_content()
        resp = self.browser.response()
        if resp is not None:
            resp.close()
        self.browser.clear_history()

if __name__ == '__main__':
    opener = mechanizeOpener()
    print(opener.open('http://www.nwsuaf.edu.cn/'))
