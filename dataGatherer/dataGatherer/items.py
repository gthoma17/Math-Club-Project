# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LppsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class FoxNewsItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	publishDate = scrapy.Field()
	ebolaOccurances = scrapy.Field()
	#numberOfComments = scrapy.Field() #difficult to get on fox
