# run in main directory with "scrapy crawl recipes"

import scrapy
import re

from ..items import Recipe


def cleanse(text):
    cleansed = re.sub(r'\(.*?\)', '', text)  # remove brackets and content
    cleansed = cleansed.strip()  # remove trailing whitespaces
    return cleansed


class RecipesSpider(scrapy.Spider):
    name = "recipes"

    def start_requests(self):
        data = [
            {'country': 'Deutschland', 'source': 'chefkoch.de', 'category': 'Frühstück', 'url': 'https://www.chefkoch.de/rs/s0g31/Fruehstuecksrezepte.html'},
            {'country': 'Deutschland', 'source': 'chefkoch.de', 'category': 'Dessert', 'url': 'https://www.chefkoch.de/rs/s0g19/Dessert-Rezepte.html'}
        ]
        for item in data:
            yield scrapy.Request(url=item['url'], callback=self.parse, cb_kwargs=dict(country=item['country'], source=item['source'], category=item['category']))

    def parse(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        country = kwargs['country']
        source = kwargs['source']
        category = kwargs['category']

        items = []

        # get infos from overview page
        for overviewRecipe in response.css('article.rsel-item'):
            title = overviewRecipe.css('h2.ds-heading-link::text').get(default='')
            url = overviewRecipe.css('a.rsel-recipe::attr("href")').get(default='')
            recipe = Recipe(title=title, country=country, source=source, category=category, url=url)
            yield recipe

            items.append(recipe)
            self.logger.info('Added item {}'.format(recipe.items()))

        # next_page = response.css('ul.ds-pagination li.ds-next a::attr("href")').get()
        # if next_page is not None:
        #     self.logger.info('Proceeding with next page')
        #     yield response.follow(next_page, self.parse)
