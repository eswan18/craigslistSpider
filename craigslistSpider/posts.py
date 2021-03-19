from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from more_itertools import pairwise

from craigslistSpider.items import Post

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
        print('Found post!')
        url = response.url
        title = response.xpath('//span[@id="titletextonly"]//text()').extract_first()
        price = response.css('span.price *::text').get()
        # Attributes come in key-value pairs.
        raw_attrs = response.css('p.attrgroup > span *::text').getall()
        attrs = dict(pairwise(raw_attrs))
        post = Post(
            url=url,
            title=title,
            price=price,
            attrs=attrs
        )
        return post
