import pymongo
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from c4d_web.items import C4DWebItem
from selenium.webdriver.firefox.options import Options


class C4dMatSpider(scrapy.Spider):
    name = 'c4d_mat'
    # allowed_domains = ['c4d.com']
    start_urls = ['https://c4dcenter.com/material-library']

    def __init__(self):

        self.mongo_uri = get_project_settings().get('MONGO_URI')
        self.mongo_db = get_project_settings().get('MONGO_DATABASE_WECHAT')

        self.collection = 'c4d_material'
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url,
                                  callback=self.parse_pages,
                                  wait_time=30,
                                  wait_until=EC.presence_of_element_located(
                                      (By.ID, 'jupiterx-primary'))
                                  )

    def parse_pages(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        base_url = "https://c4dcenter.com/material-library/page/"
        # print(self.mongo_uri)
        results = []
        articles = response.css('ul.products li')
        for article in articles:
            url = article.css('a::attr(href)').get()
            title = article.css('h2::text').get().strip()
            preview_img_url = article.css('img').attrib.get('src')
            result = self.db[self.collection].find_one({'url': url})
            if not result:
                yield SeleniumRequest(url=url,
                                      callback=self.parse,
                                      cb_kwargs={
                                          'preview_img_url': preview_img_url,
                                          'title': title
                                      },
                                      wait_until=EC.presence_of_element_located(
                                          (By.ID, 'somdn-form-submit-button')),
                                      wait_time=30,
                                      )
            results.append(result)

        # if [result for result in results if not result] == len(results):
        next_page = response.css('a.next').attrib.get('href')
        if next_page:
            yield SeleniumRequest(url=next_page,
                                  callback=self.parse_pages,
                                  wait_time=30,
                                  wait_until=EC.presence_of_element_located(
                                      (By.ID, 'jupiterx-primary'))
                                  )

    def parse(self, response,title,preview_img_url):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = C4DWebItem()
        # item['image_urls'] = []
        # item['image_urls'].append(preview_img_url)
        item['image_urls'] = response.xpath("//img[@role='presentation::attr(src)']").getall()
        # item['image_urls'] = preview_img_url
        item['image_urls'].append(preview_img_url)
        summary = response.css('div.summary')
        item['url'] = response.url
        item['title'] = summary.css('h1.product_title::text').get()
        item['categories'] = summary.css('span.product-categories a::text').getall()
        item['image_plx'] = summary.css('p.p1::text').get()
        item['map_files'] = summary.css('ul.ul1 li::text').getall()
        # item['image_preview'] = preview_img_url

        download_wrap = response.css('div.somdn-download-wrap')
        item['file_url'] = download_wrap.css('form.somdn-download-form::attr(action)').get()
        formdata = {}
        for input in download_wrap.css('input'):
            formdata[input.attrib.get('name')] = input.attrib.get('value')

        item['formdata'] = formdata

        yield item




        iamge_file_dir = get_project_settings().get('IMAGES_STORE')
        # try:
        #     driver = response.meta.get('driver')
        #     driver.find_element_by_id('somdn-form-submit-button').click()
        #     item['image_downloaded_status'] = True
        # except:
        #     item['image_downloaded_status'] = False
        #     pass
        # yield item
