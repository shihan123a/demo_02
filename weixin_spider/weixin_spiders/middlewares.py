# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import requests
from scrapy import signals


class WeixinSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeixinSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HttpProxyMiddleware(object):

    def __init__(self, test_url):
        self.test_url = test_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            test_url=crawler.settings.get('TEST_URL'),
        )
    # proxys_ip.txt为我存放IP的文件。
    with open('F:\project\spider_study\weixin_spider\weixin_spider\proxys_ip.txt', 'r', encoding='utf-8') as f:
        ips = f.readlines()

    def test_proxy(self, proxy):
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:
            response = requests.get(url=self.test_url, proxies=proxies, verify=False, timeout=20)
            if response.status_code == 200:
                print('Successfully', proxy)
                return True
            else:
                print('Useless', proxy)
                return False
        except Exception:
            print('Useless', proxy)
            return False

    def process_request(self, request, spider):
        spider.logger.debug('Using Proxy')
        random_ip = ''
        for proxy in self.ips:
            if proxy and self.test_proxy(proxy):
                random_ip = proxy
            else:
                self.ips.remove(proxy)
        # 刷新获取的ip，剔除掉那些不能用的
        with open('proxys_ip.txt', 'w+', encoding='utf-8') as f:
            f.write('\n'.join(self.ips))
        if random_ip:
            request.meta['proxy'] = 'http://{proxy}'.format(proxy=random_ip)
            request.meta['proxy'] = 'https://{proxy}'.format(proxy=random_ip)
            # request.meta['download_timeout'] = 20
            spider.logger.debug('Using Proxy:' + random_ip)
        else:
            spider.logger.debug('NO Voide IP')