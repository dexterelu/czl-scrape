# -*- coding: utf-8 -*-
import scrapy
import scrapy_proj.items

class SanatateSpider(scrapy.Spider):
    name = "sanatate"

    def start_requests(self):
        urls = [
            'http://www.ms.ro/acte-normative-in-transparenta/?vpage=1',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for item in response.css('.panel'):
            heading = item.css('div.panel-heading')
            body = item.css('div.panel-body')

            title = item.css('a.panel-title::text').extract_first()
            contact = {
                'name': body.xpath('//p[contains(text(), "Contact")]/text()').re_first(r'Contact:\s*(.*)')
            }

            yield scrapy_proj.items.ActItem(
                title = title,
                contact = contact
            )

        next_pages = response.css('.pt-cv-pagination a::attr(href)').extract()
        next_pages.reverse()
        for next_page in next_pages:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
