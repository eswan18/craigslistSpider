from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider

counter = 0

class PostSpider(CrawlSpider):
    name = 'posts'
    allowed_domains = ['chicago.craigslist.org']
    # The main page for "Computers"
    start_urls = ['https://chicago.craigslist.org/d/computers/search/sya']
    rules = [
        #  Results pages
        Rule(
            LinkExtractor(allow=r'https://chicago.craigslist.org/d/computers/search/sya.*'),
            follow=True
        ),
        # Posts
        Rule(
            LinkExtractor(allow=r'https://chicago.craigslist.org/.*/sys/d/.*'),
            callback='parse_post'
        ),
     ]

    def parse_post(self, response):
        global counter
        counter = counter + 1
        if counter > 10:
            raise CloseSpider('hit 10')
        print('Found article!')
        print(response.url)
        title = response.xpath('//span[@id="titletextonly"]//text()').extract_first()
        print(title)

