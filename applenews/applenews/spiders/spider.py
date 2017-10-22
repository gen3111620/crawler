# -*- coding: utf-8 -*-

# This is a crawler program

from applenews.items import ApplenewsItem

from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor

import datetime

class AppleNewsSpider(CrawlSpider):

	name = 'applenews'
	
	allowed_domains = ['appledaily.com.tw']
	
	start_urls = ['http://www.appledaily.com.tw/realtimenews/article/new/20171021/1226392/']
	
	rules = [Rule(LinkExtractor(), callback='parse_item', follow = True)]
	
	def parse_item(self, response):
	
		item = ApplenewsItem()
		
		item['date'] = response.xpath('//div[@class="gggs"]/time/text()').extract()

		item['title'] = response.xpath('//hgroup/h1/text()').extract()

		item['url'] = response.css('.fb-send::attr(data-href)').extract()

		item['content'] = response.css('.articulum > p::text').extract()
		
		for x in item:
		
			if len(item[x]) == 0:
			
				return
		
			item[x] = ''.join(item[x])
			
		try:

			d1 = datetime.datetime.strptime(item['date'], '%Y年%m月%d日%H:%M')
			
		except ValueError as e:

			d1 = datetime.datetime.strptime(item['date'], '%Y年%m月%d日')

		now = datetime.datetime.now()

		if (now-d1).days > 1:

			return
		
		yield item

