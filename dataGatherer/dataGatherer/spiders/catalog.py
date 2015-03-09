# -*- coding: utf-8 -*-
import time
import re
import pickle
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
        Rule(
            LinkExtractor(allow=r'preview_program\.php\?catoid=18&poid=\d{4}&returnto=3608', deny=r'preview_program\.php\?catoid=18&poid=\d{4}&print=&returnto=3608'), callback='parse_item', follow=True,
            ),
    )
    def parse_item(self, response):
        item = CatalogItem()

        #extract name
        try:
            name = response.xpath('//h1/text()').extract()[0].encode('ascii','replace')
            if "Minor" not in name:
                return
        except IndexError:
            return
            name = "UNKNOWN NAME"

        #if this isn't a minor, we don't care~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
        total_credits = "UNKNOWN CREDITS"
        for sectionName in sections:
            if "Total" in sectionName:
                try:
                    total_credits = re.findall(r'\d+', sectionName)[0].encode('ascii','replace')
                except IndexError:
                    pass
            elif "Minor Requirements:"  in sectionName:
                try:
                    total_credits = re.findall(r'\d+', sectionName)[0].encode('ascii','replace')
                except IndexError:
                    pass


        #attempt to extract catalog IDs for associated classes
        class_ids = []
        for section in sections.values():
            ids = re.findall(r'onclick=\"showCourse\(\'18\', \'\d{6}', section)
            if ids:
                for thisId in ids:
                    thisId = thisId.encode('ascii','replace')
                    class_ids.append(thisId[27:])
            else:
                pass

        #prep the item for return
        item['name'] = name
        item['total_credits'] = total_credits
        item['url'] = response.url.encode('ascii','replace')
        item['associated_classes'] = pickle.dumps(class_ids)
        return item