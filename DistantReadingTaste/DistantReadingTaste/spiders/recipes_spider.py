# run in main directory with "scrapy crawl recipes"

import scrapy
import re
import datetime


# remove whitespaces, brackets and other unnecessary elements from string
def cleanse(text):
    cleansed = re.sub(r'\(.*?\)', '', text)  # remove brackets and content
    cleansed = cleansed.strip()  # remove trailing whitespaces
    return cleansed


class RecipesSpider(scrapy.Spider):
    name = "recipes"
    filename = "recipe_results.txt"

    def start_requests(self):
        # create or overwrite results file

        open(self.filename, "w+").close()
        urls = [
            'https://www.lecker.de/ofen-haehnchen-paprika-rahm-80809.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        # get recipe title
        title = cleanse(response.css('header.article-header h1::text').get(default=''))

        items = []
        for ingredient in response.css('ul.list--ingredients li'):
            item = {
                'quantity': cleanse(ingredient.css('li span.quantityBlock span.ingredient-quantity::text').get(default='0')),
                'ingredient': cleanse(ingredient.css('li span.ingredientBlock::text').get(default=''))
            }
            items.append(item)

        with open(self.filename, 'a+') as f:
            f.write("Results from crawling at {}\n\n".format(datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
            f.write("%s\n" % title)
            for item in items:
                f.write("{}\n".format(','.join(str(x) for x in item.values())))
                # f.write("{}\n".format('\t'.join(str(item[quantity]))))
        self.log(f'Updated file {self.filename}')
