# -*- coding: utf-8 -*-

# Define your item pipelines here在此定义项目管道
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
#不要忘记将管道添加到项管道设置中
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class WeixinSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, 27017)
        self.db = self.client[self.mongo_db]
        # self.db.authenticate(name='admin', password="*****") #开启身份验证时要启用这句

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = spider.name
        self.db[collection_name].update({'article_url': item['article_url']}, {'$set': dict(item)}, upsert=True, multi=True)
        return item

