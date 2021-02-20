# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Recipe(scrapy.Item):
    title = scrapy.Field()
    source_id = scrapy.Field()
    country = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    # pass
