# run in main directory with "scrapy crawl recipes"

import scrapy
import re

from DistantReadingTaste.items import Recipe


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
            'https://www.chefkoch.de/rs/s0g31/Fruehstuecksrezepte.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        items = []

        # get infos from overview page
        for overviewRecipe in response.css('article.rsel-item'):
            title = overviewRecipe.css('h2.ds-heading-link::text').get(default='')
            country = 'DE'
            url = overviewRecipe.css('a.rsel-recipe::attr("href")').get(default='')  # maybe ::first
            recipe = Recipe(title=title, country=country, url=url)

            items.append(recipe)
            self.logger.info('Added item {}'.format(recipe.items()))

        # next_page = response.css('ul.ds-pagination li.ds-next a::attr("href")').get()
        # if next_page is not None:
        #     self.logger.info('Proceeding with next page')
        #     yield response.follow(next_page, self.parse)
