import re
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
            "Besancon",
            "Dijon",
            "Annecy"
            ]

        # FormRequest used to make a search in a specific city
        for city in city_list:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'ss': city},
                callback=self.after_search
            )
    
    # callback used after login
    def after_search(self, response):

        # extract the links of the hotel pages on current search results page
        all_urls = response.xpath('//div[@data-testid="property-card"]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a')

        # number of hotels found for a specific city
        #//*[@id="right"]/div[1]/div/div/div/div[1]/h1
        #//*[@id="right"]/div[1]/div/div/div/div[1]/h1
        #//*[@id="right"]/div[1]/div/div/div/div[1]/h1
        #//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[1]
        hotels_found = response.xpath('//*[@id="search_results_table"]/div[2]/div/div/div/div[4]/div[1]/text()').get()
        if hotels_found is None:
            hotels_found = response.xpath('/html/body/div[2]/div/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/h1/text()').get()
 
        res = [int(i) for i in hotels_found.split() if i.isdigit()]
        nb_results = res[0]

        # go scrape useful data from hotel pages
        for url in all_urls:
            yield scrapy.Request(url.attrib['href'], callback = self.parse_dir_contents)

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
            yield response.follow(next_page, callback=self.after_search)
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

        yield {
            'address': address,
            'hotel_name': hotel_name,
            'url': page_url,
            'rating': rating,
            'coordinates' : coordinates,
            'description': description
            }
        
# Name of the file where the results will be saved
filename = "hotels_data.json"

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