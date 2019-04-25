# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#在这里定义scrape的模型
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeixinSpiderItem(Item):
    # define the fields for your item here like:
    # 在此处定义项目的字段，如下所示：
    #name = scrapy.Field()
    article_title = Field() #文章标题
    article_content = Field() #文章内容
    article_pubtime = Field() #文章发送时间
    article_savetime = Field() #保存该文章时间
    article_source = Field() #文章出处
    article_picture_url = Field() #文章内图片链接
    article_editor = Field() #编辑
    article_url = Field() #文章链接
    article_platform = Field() #何处获取该文章
    spider_keyword = Field() #查询关键字

