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
            {'category': 'Main Dish', 'url': 'https://www.chefkoch.de/rs/s0t21/Hauptspeise-Rezepte.html'},
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

        servings = response.css('div.recipe-servings input[name="portionen"]::attr("value")').get(default='1')

        ingredients = []
        for ingredientRow in response.css('table.ingredients tr'):
            ingredient_item = Ingredient()

            ingredient_str = ingredientRow.css('td.td-right span::text').get(default='')  # ingredient
            if ingredient_str == '':
                ingredient_str = ingredientRow.css('td.td-right span a::text').get(default='')
            ingredient_str = re.sub(r'\(.*?\)|\*', '', ingredient_str)  # remove brackets and their content
            ingredient_str = re.sub(r'\boder\b.*|\bfür\b.*|\bwenn\b.*|\bund\b.*|\bplus\b.*|\bzum\b.*|\bnach\b.*|\balternativ\b.*|\bbzw\b.*|\bevtl\b.*|\bca\b.*|\bz\.B\b.*|\bzB\b.*|\bin\b.*', '', ingredient_str)  # remove everything after delimiters
            omitted_words = ['geschält', 'gewürfelt', 'aus dem Glas', 'unbehandelt', 'gepresst', 'zerdrückt', 'etwas', 'klein', 'grob', 'gehackt', 'möglichst', 'lang',
                             'geschnitten', 'jeweils', 'daumengroß', 'gemahlen', 'grob', 'grobes', 'flach', 'flache', 'eingeweicht', 'abgetropft', 'TK', 'tiefgekühlt',
                             'aus der Mühle', 'daumendick']
            for o in omitted_words:
                ingredient_str = re.sub(rf'\b{o}\b', '', ingredient_str)
            re.sub(r'[,-./\\]$', '', ingredient_str.strip())  # remove special chars at end of string
            ingredient = re.sub(r'\s\s+', ' ', ingredient_str).strip()  # remove multiple whitespaces

            quantity_unit_str = ingredientRow.css('td.td-left span::text').get(default='')  # amount + unit
            quantity_unit_str = re.sub(r'\(.*?\)|\*', '', quantity_unit_str)  # remove brackets and their content
            quantity = quantity_unit_str
            unit = ''
            quantity_search = re.search(r'^[\d\s\.\,\/\u00BC-\u00BE\u2150-\u215E\u2189]+', quantity_unit_str)
            if quantity_search:
                quantity = quantity_search[0]
                unit = re.sub(quantity, '', quantity_unit_str, 1)  # remove quantity from string
            quantity = re.sub(r'\s\s+', ' ', quantity).strip()  # remove multiple whitespaces
            unit = re.sub(r'\s\s+', ' ', unit).strip()  # remove multiple whitespaces

            ingredient_item['name'] = ingredient
            ingredient_item['name_en'] = ''
            ingredient_item['quantity'] = quantity
            ingredient_item['unit'] = unit

            if ingredient:
                ingredients.append(ingredient_item)

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
        recipe['servings'] = servings
        recipe['category'] = kwargs['category']

        # process recipe in pipeline
        yield recipe
