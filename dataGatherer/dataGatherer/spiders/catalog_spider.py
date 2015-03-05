import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from dataGatherer.items import CatalogItem
import articleUtils

class CatalogSpider(CrawlSpider):
    name = 'Catalog.emich.edu spider'
    allowed_domains = ["catalog.emich.edu","emich.com"]
    start_urls = ['http://catalog.emich.edu/content.php?catoid=14&navoid=2857'] # urls from which the spider will start crawling
    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('preview_program\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        item = scrapy.Item()
        return item        