# -*- coding: utf-8 -*-

from urllib.parse import urlencode
from ..items import WeixinSpiderItem
from scrapy import Request, Spider


class WxSpiderSpider(Spider):
    name = 'wx_spider'
    # allowed_domains = ['http://weixin.sogou.com/']
    # 如需启用代理ip请不要注释以下代码，这里使用的是custom_settings,它的好处是后面当同一个项目
    # 中有多个spider时，并不是每个都需要启用代理IP或其他一些中间件，custom_settings的设置只对
    # 本spider有用，对其他spider不起作用
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {

            # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
            # 'weixin_spiders.middlewares.HttpProxyMiddleware': 543,
        },
    }
    keyword = '李敖'
    def start_requests(self):
        page = 1
        data = {
            'query': self.keyword,
            'type': 2,
            'page': page,
        }
        # 生成URL的参数部分
        params = urlencode(data)
        base = 'http://weixin.sogou.com/weixin?'
        url = base + params
        # Cookie的值请用你自己的cookie代替，现在这个我删除了一部分内容所以不能用
        yield Request(url, callback=self.parse_list, cookies={
            'Cookie':'''SUID=AC200DC65F20940A000000005A82D238; SUV=003C177D2AE863765A82D23BA7F92361; CXID=DB6B9A02141A4B19FF8FA874796DC7E9; wuid=AAHm0LONHgAAAAqLE2MmvwAAIAY=; IPLOC=CN3201; ld=plllllllll2z$XnslllllV$$tfDlllllHDczxyllll9lllllRZlll5@@@@@@@@@@; LSTMV=275%2C284; LCLKINT=11834; ABTEST=3|1521210607|v1; weixinIndexVisited=1; JSESSIONID=aaaFGYBCztQ0x--EwPOiw; ad=OZllllllll2zO5galllllV$spnGlllllTOfiLlllll9lllll9Zlll5@@@@@@@@@@; SNUID=4F43D1674446248703FE2CA0440BA81E;'''},
                      meta= {'dont_redirect': False})
    # 这里传入cookies,在搜狗微信，实现登陆微信账号，这样就可以爬取多篇文章
        # print(start_urls)

    def parse_list(self, response):
        # print('redirect_urls', response.request.meta['redirect_urls'])
        if response.status == 302:
            print(response.url)
        if response.status == 200:
            # print(response.text)
            news_urls = response.xpath("//li[contains(@id,'sogou_vr_')]/div[2]/h3/a/@href").extract()
            print('news_urls', news_urls)
            for new_url in news_urls:
                yield Request(new_url, callback=self.parse_detail, dont_filter=False, meta= {'dont_redirect': False})

            # 获取所有下一页的内容//*[@id="sogou_next"]
            if response.xpath('//a[@id="sogou_next"]/text()').extract_first() == '下一页':
                next_page_url = response.xpath('//a[@id="sogou_next"]/@href').extract_first()
                next_page_url = response.urljoin(next_page_url)
                print('next_page_url:',next_page_url)
                yield Request(next_page_url, callback=self.parse_list)#meta= {'dont_redirect': False}

    def parse_detail(self, response):
        item = WeixinSpiderItem()
        if response.status == 200:
            item['article_title'] = response.xpath('//*[@id="activity-name"]/text()').extract_first(default='').strip()
            item['article_content'] = response.xpath('string(//*[@id="js_content"])').extract_first(default='').strip()
            item['article_pubtime'] = response.xpath('//*[@id="post-date"]/text()').extract_first(default='').strip()
            item['article_savetime'] = response.xpath('//*[@id="post-date"]/text()').extract_first(default='').strip()
            item['article_source'] = response.xpath('//*[@id="post-user"]/text()').extract_first(default='').strip()
            item['article_editor'] = response.xpath('//*[@id="meta_content"]/em[2]/text()').extract_first(default='').strip()
            item['article_picture_url'] = '\n'.join(
                    [url for url in response.xpath('//*[@id="js_content"]/p//img/@data-src').extract()])
            if not item['article_picture_url']:
                item['article_picture_url'] = '\n'.join(
                    [url for url in response.xpath('//*[@id="js_content"]//p//img/@data-src').extract()])
            item['article_url'] = response.url
            item['article_platform'] = '微信搜狗'
            item['spider_keyword'] = self.keyword
            yield item
