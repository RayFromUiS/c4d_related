# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class C4DWebItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()
    title = scrapy.Field()
    categories = scrapy.Field()
    tags = scrapy.Field()
    image_plx = scrapy.Field()
    map_files = scrapy.Field()
    image_preview = scrapy.Field()
    crawl_time = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_downloaded_status =scrapy.Field()

