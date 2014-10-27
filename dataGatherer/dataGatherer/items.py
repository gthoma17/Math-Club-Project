# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FoxNewsItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	publishDate = scrapy.Field()
	ebolaOccurances = scrapy.Field()
	sentiment = scrapy.Field()

class CnnItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	publishDate = scrapy.Field()
	ebolaOccurances = scrapy.Field()
	sentiment = scrapy.Field()