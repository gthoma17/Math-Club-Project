from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from dataGatherer.items import LppsItem

class NullSpider(CrawlSpider):
    name = 'lpps'
    allowed_domains = ["lincolnparkpublicschools.com"]
    start_urls = ['http://lincolnparkpublicschools.com/'] # urls from which the spider will start crawling
    rules = [Rule(SgmlLinkExtractor(allow=[r'\?idpage=.*']), follow=True, callback='parse_page'), 
        # r'page/\d+' : regular expression for http://isbullsh.it/page/X URLs
        ]
        # r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs


    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        item = LppsItem()
        # Extract title
        #item['title'] = hxs.select('//header/h1/text()').extract() # XPath selector for title
        # Extract author
        #item['tag'] = hxs.select("//header/div[@class='post-data']/p/a/text()").extract() # Xpath selector for tag(s)
        return item        