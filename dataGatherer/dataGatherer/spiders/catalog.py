# -*- coding: utf-8 -*-
import time
import re
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from dataGatherer.items import CatalogItem


class CatalogSpider(CrawlSpider):
    name = 'catalog'
    allowed_domains = ['catalog.emich.edu']
    start_urls = ['http://catalog.emich.edu/content.php?catoid=18&navoid=3608']

    rules = (
        Rule(LinkExtractor(allow=r'preview_program\.php\?catoid=18&poid=\d{4}&returnto=3608'), callback='parse_item', follow=True),
    )
    def parse_item(self, response):
        item = CatalogItem()

        #get sections
        unimportant_sections = ["<a name=\"DepartmentInformation\"", "<a name=\"AdvisorInformation\"", "<a name=\"Note\"", "<a name=\"CriticalGraduationInformation\""]
        sections = {}
        for field in response.selector.css('.acalog-core'):
            field_text = field.extract()
            if not any(section in field_text for section in unimportant_sections):
                if "<h2" in field_text:
                    section_head = re.sub('<.*?>', '', field_text[field_text.index("<h2"):field_text.index("</h2")])
                elif "<h3" in field_text:
                    section_head = re.sub('<.*?>', '', field_text[field_text.index("<h3"):field_text.index("</h3")])
                else:
                    section_head = "UNKNOWN SECTION HEAD "+str(time.time())
                print section_head
                sections[section_head] = field_text
        #find "Total credits" section, and extract that number
        for sectionName in sections:
            if "Total" in sectionName:
                total_credits = re.findall(r'\d+', sectionName)[0]

        #extract name
        name = response.xpath('//h1/text()').extract()

        #attempt to extract catalog IDs for associated classes
        class_ids = []
        for section in sections.values():
            ids = re.findall(r'onclick=\"showCourse\(\'18\', \'\d{6}', section)
            for thisId in ids:
                class_ids.append(thisId[27:])

        #prep the item for return
        item['name'] = response.xpath('//h1/text()').extract()
        item['total_credits'] = total_credits
        item['url'] = response.url
        item['associated_classes'] = class_ids
        return item
