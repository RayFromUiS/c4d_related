# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class C4DWebPipeline:
    def process_item(self, item, spider):
        if not spider.db[spider.collection].find_one({'url': item.get('url')}):
            spider.db[spider.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
