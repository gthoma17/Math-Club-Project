from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from dataGatherer.items import FoxNewsItem
import articleUtils

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
        ebolaCount = str(response.xpath('.//text()').extract()).lower().count("ebola")
        if 0 != ebolaCount:  #contains ebola smoke test
            analizedArticle = articleUtils.analizeArticle(response.url)
            ebolaCount = analizedArticle["main_body"].lower().count("ebola")
            if 0 != ebolaCount:  #contains ebola concrete test
                # Extract word occurances (the reason we're here)
                item['ebolaOccurances'] = ebolaCount
                # Extract the publish date
                item['publishDate'] = response.xpath('//time/@datetime').extract()
                # Extract title
                item['title'] = analizedArticle["title"]
                # Extract url
                item['url'] = response.url
                # Get sentiment if it's an article we care about
                sentiment = articleUtils.getsentiment(analizedArticle["main_body"])
                item['sentiment'] = sentiment["pos"] - sentiment["neg"]
        return item        