import scrapy


class RemaxspiderSpider(scrapy.Spider):
    name = "remaxSpider"
    allowed_domains = ["remax.com.tn"]
    start_urls = ["https://www.remax.com.tn/vente-appartement"]

    custom_settings = {
        
        'DOWNLOAD_DELAY': 4, # 10, #seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def parse(self, response):
        #
        
        links = response.css('div.gallery-title a::attr(href)').getall()
        for link in links:
         yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})

        
        
        next_page_href = response.css('li a.ajax-page-link[aria-label=""]::attr(href)').get()
        print(next_page_href)



    def parse_details(self, response):
       print(response.url)

