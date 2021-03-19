# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field
import scrapy


class Post(scrapy.Item):
    url = Field()
    title = Field()
    price = Field()
    attrs = Field()
