import scrapy
import os
# Vérifier si le fichier existe déjà
if os.path.exists('data.json'):
    # Si le fichier existe, supprimer son contenu
    open('data.json', 'w').close()
class TunisiapromospiderSpider(scrapy.Spider):
    if os.path.exists('resultat.json'):
        os.remove('resultat.json')
        
    name = "tunisiapromoSpider"
    allowed_domains = ["tunisiapromo.com"]
    start_urls = [
        'https://www.tunisiapromo.com/recherche?listing_type=4&property_type=1&region1=ANY&submit_listing=trouver+%21&property_search=a',
    ]

    def parse(self, response):
        
        for job in response.css('a.headline::attr(href)').getall():
            yield response.follow(job, self.parse_listing)

        next_page = response.css("p a:contains('Suivant')::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_listing(self, response):
        # Extract the property details from the HTML code
        price = response.css('span.property_price::text').get().strip()
        reference = response.xpath('//span[text()="Référence :"]/following-sibling::span/text()').get().strip()
        property_type = response.xpath('//span[text()="Type du bien :"]/following-sibling::span/text()').get().strip()
        # Extract the additional details from the HTML code
        pieces = response.xpath('//span[text()="Nombre de pièce(s) :"]/following-sibling::span/text()').get().strip()
        salles_bain = response.xpath('//span[text()="Nombre de salle(s) de bain :"]/following-sibling::span/text()').get().strip()
        salles_eau = response.xpath('//span[text()="Nombre de salle(s) d\'eau :"]/following-sibling::span/text()').get().strip()
        annee_construction = response.xpath('//span[text()="Année de Construction :"]/following-sibling::span/text()').get().strip()
        surface_habitable = response.xpath('//span[text()="Surface habitable :"]/following-sibling::span/text()').get().strip()
        surface_totale = response.xpath('//span[text()="Surface Totale :"]/following-sibling::span/text()').get().strip()
        place_voiture = response.xpath('//span[text()="Nombre de place de Voiture :"]/following-sibling::span/text()').get().strip()
        num_etages = response.xpath('//span[text()="Numéro / Nombre d\'étages :"]/following-sibling::span/text()').get().strip()
        description = response.css(".clear p::text").get()

        # Yield the results as a dictionary
        #dictionnaire contenant les données extraites du code HTML
        yield {
            'price': price,
            'reference': reference,
            'property_type': property_type,
            'pieces': pieces,
            'salles_bain': salles_bain,
            'salles_eau': salles_eau,
            'annee_construction': annee_construction,
            'surface_habitable': surface_habitable,
            'surface_totale': surface_totale,
            'place_voiture': place_voiture,
            'num_etages': num_etages,
            'description': description,
        }
