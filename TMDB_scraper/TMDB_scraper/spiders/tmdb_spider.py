# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/496243']
    
    def parse(self,response):
        '''
        '''
        pass
    
    def parse_full_credits(self,response):
        '''
        '''
        pass
    
    def parse_actor_page(self,response):
        '''
        '''
        pass