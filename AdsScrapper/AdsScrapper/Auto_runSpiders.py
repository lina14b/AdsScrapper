import subprocess
import os
# Run spiders 1, 2, and 3 in parallel
bnb=subprocess.Popen(['scrapy', 'crawl', 'BnbSpider'])
tps=subprocess.Popen(['scrapy', 'crawl', 'TPSSpider'])
tp=subprocess.Popen(['scrapy', 'crawl', 'tunisiapromoSpider'])
tA=subprocess.Popen(['scrapy', 'crawl', 'TunisieAnnonceSpider'])
rmX=subprocess.Popen(['scrapy', 'crawl', 'remaxSpider'])
# Wait for all spiders to finish
bnb.wait()
tps.wait()
tp.wait()
tA.wait()
rmX.wait()

# Run spider 4
TV=subprocess.Popen(['scrapy', 'crawl', 'TunisieVenteSpider'])
TV.wait()
# Run last.py
file_path=os.getcwd()
file_path = file_path.replace('/', '\\')
print(file_path)
update=subprocess.Popen(['python',file_path+'\\AdsScrapper\\updatingDB.py'])
update.wait()
print("\n \n end.. close the tab")

