import scrapy
from scrapy import Request

from scrapy_project.items import PeopleItem


class WorkuaSpider(scrapy.Spider):

    name = 'workua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/resumes-kharkiv/']

    site_url = 'https://www.work.ua'

    def parse(self, response):

        for person in response.css('div.card.resume-link'):
            name = person.css('div>b::text').get()
            age = person.css('div>span:nth-child(3)::text').get()
            position = person.css('h2>a::text').get()

            people_item = PeopleItem()
            people_item['name'] = name.strip()
            people_item['age'] = age.split()[0].strip() if age.isdigit() else None # noqa
            people_item['position'] = position.strip()

            detail_page = person.css('div.row div a::attr(href)').get()
            detail_page_url = self.site_url + detail_page

            yield Request(detail_page_url, self.parse_detail, meta={
                'people_item': people_item
            })

        next_page = response.css('ul.pagination-small li a::attr(href)').getall() # noqa
        next_page_url = self.site_url + next_page[-1]
        yield Request(next_page_url)

    def parse_detail(self, response):

        detail = response.css('p#addInfo::text').get()
        people_item = response.meta['people_item']
        people_item['detail'] = detail
        yield people_item
