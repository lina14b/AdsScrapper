import scrapy
import logging

class TAYARASpider(scrapy.spider):
    name= "tay"

    start_urls = [
        "https://www.tayara.tn/"
    ]

custom_settings = {
    'LOG_LEVEL': Logging.WARNING,
    'ITEM_PIPELINES': { '__main__CsvPipeline':1},
    'FEED_FORMAT': 'csv', #used fo pipeline
    'FEED_URI':tayararesult.csv'
}

def parse(self ,response):
    for result in response.css('howa hat unorderlist'):
    scrapy.Request(url=result.xpath('@href').extract_first(),)