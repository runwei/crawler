# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis


#from scrapy import signals


import json
import codecs
from collections import OrderedDict
from scrapy.contrib.pipeline.images import ImagesPipeline

class ImageDPipeline(ImagesPipeline):
    
    def __init__(self):
        self.file = codecs.open('data_test.json', 'w', encoding='utf-8')
    
    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        #        print '******************************************'
        return item
    
    def spider_closed(self, spider):
        self.file.close()


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('data_test.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
#        print '******************************************'
        return item

    def spider_closed(self, spider):
        self.file.close()


class RedisPipeline(object):

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379)

    def process_item(self, item, spider):
        if not item['id']:
            print 'no id item!!'

        str_recorded_item = self.r.get(item['id'])
        final_item = None
        if str_recorded_item is None:
            final_item = item
        else:
            ritem = eval(self.r.get(item['id']))
            final_item = dict(item.items() + ritem.items())
        self.r.set(item['id'], final_item)

    def spider_closed(self, spider):
        return
