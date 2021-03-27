#!/usr/bin/env python3

import re

from scrapy.spiders import CrawlSpider
from scrapy.http import Request

from ..items import Recipe, Ingredient, Nutrients


class ChefkochSpider(CrawlSpider):
    name = 'chefkoch'
    # download_delay = 1

    def start_requests(self):
        data = [
            {'category': 'Hauptspeise', 'url': 'https://www.chefkoch.de/rs/s0t21/Hauptspeise-Rezepte.html'},
        ]
        for item in data:
            yield Request(url=item['url'], callback=self.parse, cb_kwargs=dict(category=item['category']))

    def parse(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        # get infos from overview page
        for recipePreview in response.css('article.rsel-item'):
            # title
            title = recipePreview.css('h2.ds-heading-link::text').get(default='')

            # url
            url = recipePreview.css('a.rsel-recipe::attr("href")').get(default='')

            request = Request(url, callback=self.parse_recipe)
            request.cb_kwargs['category'] = kwargs['category']
            request.cb_kwargs['title'] = title
            yield request

        next_page = response.css('ul.ds-pagination li.ds-next a::attr(href)').get()
        self.logger.info('NEXT {}'.format(next_page))
        if next_page is not None:
            self.logger.info('Proceeding with next page')
            # yield response.follow(next_page, self.parse)
            yield response.follow(url=next_page, callback=self.parse, cb_kwargs=dict(category=kwargs['category']))

    def parse_recipe(self, response, **kwargs):
        self.logger.info('Processing recipe from {}'.format(response.url))
        recipe = Recipe()

        ingredients = []
        for ingredientRow in response.css('table.ingredients tr'):
            ingredient = Ingredient()
            quantity = ingredientRow.css('td.td-left span::text').get(default='')  # amount + unit
            name = ingredientRow.css('td.td-right span::text').get(default='').strip()  # ingredient
            if name == '':
                name = ingredientRow.css('td.td-right span a::text').get(default='').strip()
            name = re.sub(r'\(.*?\)|\s{2,}|,.*|\soder|\sor', '', name)  # remove multiple whitespaces, delimiter and brackets and their content
            quantity = re.sub(r'\(.*?\)|\s{2,}', '', quantity)  # remove multiple whitespaces and brackets and their content

            ingredient['name'] = name
            ingredient['quantity'] = quantity
            ingredients.append(ingredient)

        nutrients_list = response.css('article.recipe-nutrition .ds-col-3::text').getall()

        nutrients = Nutrients()

        if len(nutrients_list) == 8:
            # remove html tags with content and multiple whitespaces
            nutrients['energy'] = re.sub(r'<.*>|\s{2,}', '', nutrients_list[1]).strip()
            nutrients['protein'] = re.sub(r'<.*>|\s{2,}', '', nutrients_list[3]).strip()
            nutrients['fat'] = re.sub(r'<.*>|\s{2,}', '', nutrients_list[5]).strip()
            nutrients['carbohydrates'] = re.sub(r'<.*>|\s{2,}', '', nutrients_list[7]).strip()

        recipe['url'] = response.url
        recipe['country'] = 'Deutschland'
        recipe['source'] = 'chefkoch.de'
        recipe['ingredients'] = ingredients
        recipe['nutrients'] = nutrients
        recipe['title'] = kwargs['title']
        recipe['category'] = kwargs['category']

        # process recipe in pipeline
        yield recipe
