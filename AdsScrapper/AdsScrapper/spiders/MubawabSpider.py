import scrapy


class MubawabspiderSpider(scrapy.Spider):
    name = "MubawabSpider"
    allowed_domains = ["mmubawab.tn"]
    start_urls = ["http://mmubawab.tn/"]

    def parse(self, response):
        pass
