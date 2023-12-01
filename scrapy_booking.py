import os 
import pandas as pd

# Import logging => Library used for logs manipulation 
## More info => https://docs.python.org/3/library/logging.html
import logging

# Import scrapy and scrapy.crawler 
import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy.utils.misc
import scrapy.core.scraper

from urllib.parse import unquote


class BookingSpider(scrapy.Spider):
    # Name of your spider
    name = "booking"

    #last_nav = None
    #start_url = None

    def warn_on_generator_with_return_value_stub(spider, callable):
        pass

    scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
    scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
    #def start_requests(self):
    cities = [
        "Mont Saint Michel",
        "St Malo",
        "Bayeux",
        "Le Havre",
        "Rouen",
        "Paris",
        "Amiens",
        "Lille",
        "Strasbourg",
        "Chateau du Haut Koenigsbourg",
        "Colmar",
        "Eguisheim",
        "Besancon",
        "Dijon",
        "Annecy",
        "Grenoble",
        "Lyon",
        "Gorges du Verdon",
        "Bormes les Mimosas",
        "Cassis",
        "Marseille",
        "Aix en Provence",
        "Avignon",
        "Uzes",
        "Nimes",
        "Aigues Mortes",
        "Saintes Maries de la mer",
        "Collioure",
        "Carcassonne",
        "Ariege",
        "Toulouse",
        "Montauban",
        "Biarritz",
        "Bayonne",
        "La Rochelle"
    ]


    base_url ="https://www.booking.com/searchresults.html?label=gen173nr-1FCAQoggJCDHNlYXJjaF9wYXJpc0gzWARoTYgBAZgBMbgBB8gBDNgBAegBAfgBA4gCAagCA7gClq2RqwbAAgHSAiRkOGYwYmI5Ni02NmJiLTQ3MzktODAwYi0wMDlkZjVhN2UyMzXYAgXgAgE&aid=304142&ss={}&nflt=ht_id%3D204%3Bdistance%3D5000%3Breview_score%3D70"
    all_urls = []
    for city in cities : 
        new_url = base_url.format(city)
        offset_list = []
        limit = 40 #maximum number of page for a destination in booking
        for i in range(limit+1):
            offset = new_url + f'&offset={i*25}'
            offset_list.append(offset)
        all_urls+=offset_list
    
    start_urls = all_urls
         

    def parse(self, response):
        city= response.url.split("ss=")[1].split("&")[0]
        city = unquote(city)
            #if self.start_url[city] is None:
             #   self.start_url[city] = response.url
            #    self.last_nav[city] = response.xpath('//li[@class="b16a89683f"]/button/text()').getall()
              #  self.max_pages[city] = int(self.last_nav[city][-1])

        cards = response.xpath('//div[@class="c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 c6710787a4"]')
        for card in cards:
                hotel_name = card.xpath('.//div[@class="f6431b446c a15b38c233"]/text()').getall()
                hotel_url = card.xpath('.//a[@class="a78ca197d0"]/@href').getall()
                score = card.xpath('.//div[@class="a3b8729ab1 d86cee9b25"]/text()').getall()
                #price = card.xpath('.//div[@class="e84eb96b1f a661120d62"]span/text()').get()

                yield {
                # 'url': response.url,
                    'hotel_name': hotel_name,
                    'score': score,
                    'city':city,
                    #'price': price,
                    'hotel_link': hotel_url,
                    #'offset':self.offsets[city],
                    #'max_pages':self.max_pages[city],
                    }

        
         



filename = "booking_hotels.json"

# If file already exists, delete it before crawling (because Scrapy will 
# concatenate the last and new results otherwise)
if filename in os.listdir('src/'):
        os.remove('src/' + filename)


process3 = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'src/' + filename : {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process3.crawl(BookingSpider)
process3.start()

