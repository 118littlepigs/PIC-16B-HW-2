# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/496243']
    
    def parse(self,response):
        '''
        Assuming starts on movie page, navigates to cast page
        '''
        cast_url = response.request.url + "/cast"
        yield scrapy.Request(cast_url,callback = self.parse_full_credits)
    
    def parse_full_credits(self,response):
        '''
        Scrapes list of actor pages from cast page and navigates to each
        '''
        
        #finds list of actor pages linked in cast page
        cast = response.css("section.panel.pad")[0]
        actor_pages = cast.css("div.info p a::attr(href)").getall()
        
        #calls parse_actor_page for each actor page in list
        for page in actor_pages:
            yield response.follow(page, callback=self.parse_actor_page)
    
    def parse_actor_page(self,response):
        '''
        Starts on actor page, scrapes and yields movies/shows that actor has been in
        '''
        
        #finds actor name
        actor_name = response.css("title::text").get().split(" — ")[0]
        
        #finds list of movies/shows that actor has been in
        credits = response.css("table.card.credits")[0]
        credit_names = credits.css("td.role a.tooltip bdi::text").getall()
        
        #yields dict for each movie/show, corresponds to a line in .csv
        for credit in credit_names:
            yield {"actor":actor_name,"movie_or_TV_name":credit}
            
        