from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from dataGatherer.items import FoxNewsItem

class FoxSpider(CrawlSpider):
    name = 'foxNews'
    allowed_domains = ["foxnews.com","www.foxnews.com"]
    start_urls = ['http://foxnews.com/'] # urls from which the spider will start crawling
    rules = [Rule(SgmlLinkExtractor(allow=[r'\d{4}/\d{2}/\w+.*']), follow=True, callback='parse_page'), 
             Rule(SgmlLinkExtractor(allow=[r'/.*/index\.html']), follow=True)
            ]
        


    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)
        item = FoxNewsItem()
        print "!!!!!!!!!!!!!!!!!!!!!!" + str(response.xpath('//title/text()').extract())
        # Extract title
        item['title'] = response.xpath('//title/text()').extract() # XPath selector for title
        # Extract author
        item['url'] = response.url
        # Extract the publish date
        item['publishDate'] = response.xpath('//time/@datetime').extract()
        # Extract word occurances (the reason we're here)
        item['ebolaOccurances'] = response.xpath('.//text()').extract().count("ebola")        

        return item        