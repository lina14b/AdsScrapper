import scrapy
from scrapy.selector import Selector
from urllib.parse import urljoin
from datetime import datetime
import re


class MenzilispiderSpider(scrapy.Spider):
    name = "MenziliSpider"
    allowed_domains = ["menzili.tn"]
    start_urls = ["https://www.menzili.tn/immo/vente-immobilier-tunisie"]
    base_url = "https://www.menzili.tn/"

    custom_settings = {
        
        'DOWNLOAD_DELAY':  10, # seconds delay
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 408]

    }

    def parse(self, response):

        links = response.css('div.col-md-5.col-sm-5.col-xs-12.li-item-list-img a::attr(href)').getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_details, meta={'url': response.urljoin(link)})
        
        next_page = response.css('ul.pagination li a.pag-item.btn.btn-default:contains(">")::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_details(self, response):
        
        sel = Selector(response)

        Prix = response.css('div.product-price p::text').get().strip()

        Addresse = response.css('div.product-title-h1 p:last-of-type::text').get().strip()

        Date_Insertion = response.css('time[itemprop="datePublished"]::attr(datetime)').get()
        Date_Insertion = datetime.strptime(Date_Insertion, '%Y-%m-%d').strftime('%d/%m/%Y')

        Description = response.css('div.block-descr p')
        Description = Description.get().replace('<br>', '')

        details = response.xpath('//div[@class="col-md-12 col-xs-12 col-sm-12 block-detail"]')[0]

        Chambres = details.xpath('.//div[contains(., "Chambres")]/strong/text()').get()

        Salle_de_bain  = details.xpath('.//div[contains(., "Salle de bain")]/strong/text()').get()

        Pieces = details.xpath('.//div[contains(., "Piéces (Totale)")]/strong/text()').get()

        Surface_habitable  = details.xpath('.//div[contains(., "Surf habitable")]/strong/text()').get()

        Surface  = details.xpath('.//div[contains(., "Surf terrain")]/strong/text()').get()

        Année_Construction = details.xpath('.//div[contains(., "Année construction")]/strong/text()').get()

        Equipement = details.xpath('.//div[@class="col-md-12 col-xs-12 col-sm-12 block-over"]//span[contains(@class, "span-opts")]/strong/text()').getall()

        image_urls = response.css('div.slider-product img::attr(src)').extract()