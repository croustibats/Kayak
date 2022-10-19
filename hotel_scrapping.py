# this function convert unicode to ascii

def reformat_string(str_input):
    str_input = str_input.replace("\n", "")
    str_input = str_input.replace("\u00c0", "À")
    str_input = str_input.replace("\u00c1", "Á")
    str_input = str_input.replace("\u00c2", "Â")
    str_input = str_input.replace("\u00c3", "Ã")
    str_input = str_input.replace("\u00c4", "Ä")
    str_input = str_input.replace("\u00c5", "Å")
    str_input = str_input.replace("\u00c6", "Æ")
    str_input = str_input.replace("\u00c7", "Ç")
    str_input = str_input.replace("\u00c8", "È")
    str_input = str_input.replace("\u00c9", "É")
    str_input = str_input.replace("\u00ca", "Ê")
    str_input = str_input.replace("\u00cb", "Ë")
    str_input = str_input.replace("\u00cc", "Ì")
    str_input = str_input.replace("\u00cd", "Í")
    str_input = str_input.replace("\u00ce", "Î")
    str_input = str_input.replace("\u00cf", "Ï")
    str_input = str_input.replace("\u00d1", "Ñ")
    str_input = str_input.replace("\u00d2", "Ò")
    str_input = str_input.replace("\u00d3", "Ó")
    str_input = str_input.replace("\u00d4", "Ô")
    str_input = str_input.replace("\u00d5", "Õ")
    str_input = str_input.replace("\u00d6", "Ö")
    str_input = str_input.replace("\u00d8", "Ø")
    str_input = str_input.replace("\u00d9", "Ù")
    str_input = str_input.replace("\u00da", "Ú")
    str_input = str_input.replace("\u00db", "Û")
    str_input = str_input.replace("\u00dc", "Ü")
    str_input = str_input.replace("\u00dd", "Ý")
    # now lower case accents
    str_input = str_input.replace("\u00df", "ß")
    str_input = str_input.replace("\u00e0", "à")
    str_input = str_input.replace("\u00e1", "á")
    str_input = str_input.replace("\u00e2", "â")
    str_input = str_input.replace("\u00e3", "ã")
    str_input = str_input.replace("\u00e4", "ä")
    str_input = str_input.replace("\u00e5", "å")
    str_input = str_input.replace("\u00e6", "æ")
    str_input = str_input.replace("\u00e7", "ç")
    str_input = str_input.replace("\u00e8", "è")
    str_input = str_input.replace("\u00e9", "é")
    str_input = str_input.replace("\u00ea", "ê")
    str_input = str_input.replace("\u00eb", "ë")
    str_input = str_input.replace("\u00ec", "ì")
    str_input = str_input.replace("\u00ed", "í")
    str_input = str_input.replace("\u00ee", "î")
    str_input = str_input.replace("\u00ef", "ï")
    str_input = str_input.replace("\u00f0", "ð")
    str_input = str_input.replace("\u00f1", "ñ")
    str_input = str_input.replace("\u00f2", "ò")
    str_input = str_input.replace("\u00f3", "ó")
    str_input = str_input.replace("\u00f4", "ô")
    str_input = str_input.replace("\u00f5", "õ")
    str_input = str_input.replace("\u00f6", "ö")
    str_input = str_input.replace("\u00f8", "ø")
    str_input = str_input.replace("\u00f9", "ù")
    str_input = str_input.replace("\u00fa", "ú")
    str_input = str_input.replace("\u00fb", "û")
    str_input = str_input.replace("\u00fc", "ü")
    str_input = str_input.replace("\u00fd", "ý")
    str_input = str_input.replace("\u00ff", "ÿ")

    return str_input

####################################################

import re
import unidecode
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
    
class BookingSpider(scrapy.Spider):
    # name of my spider
    name = "hotels"

    # starting URL
    start_urls = ['https://www.booking.com/']

    # parse function for form request
    def parse(self, response):

        city_list = [
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
            
        # FormRequest used to make a search in a specific city
        for city in city_list:
            id = city_list.index(city)
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'ss': city},
                callback=self.after_search,
                # keep track of the city id
                meta = {'id' : id}
            )
    
    # callback used after login
    def after_search(self, response):

        # keep track of the city id
        id = response.meta['id']

        # extract the links of the hotel pages on current search results page
        all_urls = response.xpath('//div[@data-testid="property-card"]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a')

        # number of hotels found for a specific city
        hotels_found = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[1]/text()').get()
        if hotels_found is None:
            hotels_found = response.xpath('/html/body/div[2]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/h1/text()').get()
 
        res = [int(i) for i in hotels_found.split() if i.isdigit()]
        nb_results = res[0]

        # go scrape useful data from hotel pages
        for url in all_urls:
            yield scrapy.Request(url.attrib['href'], callback = self.parse_dir_contents, meta = {'id' : id})

        # loop if there is a next results page       
        current_url = response.request.url
        if current_url.find('offset') == -1:
            current_url += '&offset=0'
        url_list = current_url.split('offset=')

        temp = re.findall(r'\d+', url_list[1])
        incr_step = 25
        new_offset = int(temp[0]) + incr_step

        if new_offset <= nb_results - nb_results % 25:
            next_page = url_list[0] + 'offset=' + str(new_offset) + url_list[1][len(temp[0]):]
            yield response.follow(next_page, callback=self.after_search, meta = {'id' : id})
        else:
            logging.info('No next page. Terminating crawling process.')

    # callback used after urls gathering
    def parse_dir_contents(self, response):
        #/html/body/div[4]/div/div[4]/div[1]/div[1]/div/div[2]/div[10]/div[1]/div/div/div/h2/text()
        #//*[@id="hp_hotel_name"]/div/div/h2/text()
        hotel_name = response.xpath('//*[@id="hp_hotel_name"]/div/div/h2/text()').get()
        page_url = response.request.url
        rating = response.xpath('//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div/div[1]/text()').get()
        coordinates = response.xpath('//*[@id="hotel_header"]').attrib['data-atlas-latlng']
        description = response.xpath('//*[@id="property_description_content"]/p').get()
        address = response.xpath('//*[@id="showMap2"]/span[1]/text()').get()
        clean_adress = unidecode.unidecode(reformat_string(address))
        city = re.findall("\d{5} (.*), France", clean_adress)

        yield {
            'id' : response.meta['id'],
            'city' : city,
            'address': address,
            'hotel_name': hotel_name,
            'url': page_url,
            'rating': rating,
            'coordinates' : coordinates,
            'description': description
            }
        
# Name of the file where the results will be saved
filename = "hotel_data.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('booking_json/'):
        os.remove('booking_json/' + filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/103.0.5060.114',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'booking_json/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(BookingSpider)
process.start()