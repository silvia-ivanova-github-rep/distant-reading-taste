# run in main directory with "scrapy crawl recipes"

import scrapy
import re

from ..items import Recipe


def cleanse(text):
    cleansed = re.sub(r'\(.*?\)', '', text)  # remove brackets and content
    cleansed = re.sub(r'\s{2,}', '', cleansed)  # remove multiple whitespaces
    cleansed = cleansed.strip()  # remove preceeding and trailing whitespaces
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

        # get infos from overview page
        for overviewRecipe in response.css('article.rsel-item'):
            title = overviewRecipe.css('h2.ds-heading-link::text').get(default='')
            url = overviewRecipe.css('a.rsel-recipe::attr("href")').get(default='')

            request = scrapy.Request(url, callback=self.parse_recipe, cb_kwargs=dict(main_url=response.url))
            request.cb_kwargs['title'] = title
            request.cb_kwargs['country'] = kwargs['country']
            request.cb_kwargs['source'] = kwargs['source']
            request.cb_kwargs['category'] = kwargs['category']
            yield request

        # next_page = response.css('ul.ds-pagination li.ds-next a::attr("href")').get()
        # if next_page is not None:
        #     self.logger.info('Proceeding with next page')
        #     yield response.follow(next_page, self.parse)

    def parse_recipe(self, response, **kwargs):
        self.logger.info('Processing recipe from {}'.format(response.url))

        ingredients = []
        for ingredientRow in response.css('table.ingredients tr'):
            amount = ingredientRow.css('td.td-left span::text').get(default='')  # amount + unit
            ingredient = ingredientRow.css('td.td-right span::text').get(default='')  # ingredient
            ingredient = cleanse(ingredient)
            if ingredient == '':
                ingredient = ingredientRow.css('td.td-right span a::text').get(default='')
                ingredient = cleanse(ingredient)
            amount = cleanse(amount)
            ingredients.append({'ingredient': ingredient, 'amount': amount})

        recipe = Recipe(
            title=kwargs['title'],
            country=kwargs['country'],
            source=kwargs['source'],
            category=kwargs['category'],
            url=response.url,
            ingredients=ingredients
        )

        # process recipe in pipeline
        yield recipe
