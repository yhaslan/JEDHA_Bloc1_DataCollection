# Import scrapy and scrapy.crawler 
import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy.utils.misc
import scrapy.core.scraper
import pandas as pd
import os
import logging


class BookingCoordinateSpider(scrapy.Spider):
    # Name of your spider
    name = "coordinates"
    #last_nav = None
    #start_url = None

    def warn_on_generator_with_return_value_stub(spider, callable):
        pass

    scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
    scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
    df = pd.read_json('src/booking_hotels.json')
    hotel_pages = []
    for item in df['hotel_link']:
         hotel_pages.append(item[0])
    
    start_urls = hotel_pages
         

    def parse(self, response):
        #hotel_n = response.xpath('/html/body/div[3]/div/div[5]/div[1]/div[1]/div[1]/div/div[3]/div[9]/div[1]/div/div/h2/text()').get()
        coords = response.xpath('//p[@class="address address_clean"]/a/@data-atlas-latlng').get()
        lat_hotel = coords.split(",")[0]
        lon_hotel = coords.split(",")[1]
        

        yield {
                'hotel_link': response.url,
                'lat_hotel': lat_hotel,
                'lon_hotel': lon_hotel,

                    }

        
         



filename = "booking_coordinates.json"

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
process3.crawl(BookingCoordinateSpider)
process3.start()

