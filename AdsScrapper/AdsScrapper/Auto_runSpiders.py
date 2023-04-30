import subprocess

# Run spiders 1, 2, and 3 in parallel
bnb=subprocess.Popen(['scrapy', 'crawl', 'BnbSpider'])
tps=subprocess.Popen(['scrapy', 'crawl', 'TPSSpider'])
tp=subprocess.Popen(['scrapy', 'crawl', 'tunisiapromoSpider'])
tA=subprocess.Popen(['scrapy', 'crawl', 'TunisieAnnonceSpider'])
# Wait for all spiders to finish
bnb.wait()
tps.wait()
tp.wait()
tA.wait()

# Run spider 4
TV=subprocess.Popen(['scrapy', 'crawl', 'TunisieVenteSpider'])
TV.wait()
# Run last.py
subprocess.Popen(['python', 'C:\\Users\\Lina\\Desktop\\AdsScrapper\\AdsScrapper\\AdsScrapper\\AdsScrapper\\updatingDB.py'])
