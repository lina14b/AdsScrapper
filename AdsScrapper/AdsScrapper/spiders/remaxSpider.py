import scrapy


class RemaxspiderSpider(scrapy.Spider):
    name = "remaxSpider"
    allowed_domains = ["remax.com.tn"]
    start_urls = ["http://remax.com.tn/"]

    def parse(self, response):
        pass
