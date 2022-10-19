import re
import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
    
class BookingSpider1(scrapy.Spider):
    # Name of your spider
    name = "hotels1"

    # Starting URL
    start_urls = ['https://www.booking.com/']

    # Parse function for form request
    def parse(self, response):
        
        city_list = ['les sables d olonne']
        # FormRequest used to make a search in a specific city
        for city in city_list:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'ss': city},
                callback=self.after_search
            )
    
    # Callback used after login
    def after_search(self, response):
        #city_name = response.xpath('/html/body/div[2]/div/div[3]/div[1]/div[2]/div[1]/div[1]/div/div/form/div/div[2]/div/div[2]/div[1]/div/div/input')
        all_names = response.xpath('//div[@data-testid="title"]/text()')
        all_urls = response.xpath('//div[@data-testid="property-card"]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a')
        all_ratings = response.xpath('//div[@data-testid="review-score"]/div[1]/text()')
        hotels_found = response.xpath('//*[@id="right"]/div[1]/div/div/div/h1/text()').get()
        res = [int(i) for i in hotels_found.split() if i.isdigit()]
        nb_results = res[0]

        for name, url, rating in zip(all_names, all_urls, all_ratings):
            yield {
                #'city': city_name.attrib['value'],
                'hotel_name': name.get(),
                'url' : url.attrib['href'],
                'rating': rating.get()
            }
        
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

# Name of the file where the results will be saved
filename = "hotels.json"

# If file already exists, delete it before crawling (because Scrapy will concatenate the last and new results otherwise)
if filename in os.listdir('scrapping-booking/'):
        os.remove('scrapping-booking/' + filename)

# Declare a new CrawlerProcess with some settings
process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/103.0.5060.114',
    'LOG_LEVEL': logging.INFO,
    "FEEDS": {
        'scrapping-booking/' + filename: {"format": "json"},
    }
})

# Start the crawling using the spider you defined above
process.crawl(BookingSpider1)
process.start()