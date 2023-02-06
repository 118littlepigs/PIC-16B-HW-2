# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/496243']
    
    def parse(self,response):
        '''
        '''
        cast_url = response.request.url + "/cast"
        yield scrapy.Request(cast_url,callback = self.parse_full_credits)
    
    def parse_full_credits(self,response):
        '''
        '''
        cast = response.css("section.panel.pad")[0]
        actor_pages = cast.css("div.info p a::attr(href)").getall()
        for page in actor_pages:
            yield response.follow(page, callback=self.parse_actor_page)
    
    def parse_actor_page(self,response):
        '''
        '''
        actor_name = response.css("title::text").get().split(" — ")[0]
        
        credits = response.css("table.card.credits")[0]
        credit_links = credits.css("td.role a.tooltip::attr(href)").getall()
        credit_names = credits.css("td.role a.tooltip bdi::text").getall()
        
        for credit in credit_names:
            yield {"actor":actor_name,"movie_or_TV_name":credit}
            
        