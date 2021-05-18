# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import json
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline

class C4DWebPipeline:
    def process_item(self, item, spider):
        if not spider.db[spider.collection].find_one({'url': item.get('url')}):
            spider.db[spider.collection].insert_one(ItemAdapter(item).asdict())
        return item

class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)


# class MyFilesPipeline(FilesPipeline):
#
#     def get_media_requests(self, item, info):
#         adapter = ItemAdapter(item)
#         formdata = item.get('formdata')
#         for file_url in adapter['file_urls']:
#             if formdata:
#                 yield scrapy.FormRequest(file_url,method='POST',formdata=json.dumps(formdata))

