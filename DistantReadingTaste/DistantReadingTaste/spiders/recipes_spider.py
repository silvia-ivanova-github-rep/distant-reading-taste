# run in main directory with "scrapy crawl recipes"

import scrapy
import re

from ..items import Recipe, Ingredient, Nutrients
from ..spider_settings import SOURCE_SPECIFICS


def cleanse(text):
    cleansed = re.sub(r'\(.*?\)', '', text)  # remove brackets and content
    cleansed = re.sub(r'\s{2,}', '', cleansed)  # remove multiple whitespaces
    cleansed = cleansed.strip()  # remove preceeding and trailing whitespaces
    return cleansed


def cleanse_ingredient(text):
    cleansed = cleanse(text)
    cleansed = re.sub(r',.*', '', cleansed)  # remove ","
    cleansed = re.sub(r'\soder.*', '', cleansed)  # remove oder
    cleansed = re.sub(r'\sor.*', '', cleansed)  # remove or
    return cleansed


def get_css_item(source, element):
    if source in SOURCE_SPECIFICS and element in SOURCE_SPECIFICS[source]:
        return SOURCE_SPECIFICS[source][element]
    else:
        return None

# https://github.com/mrorii/cookbot/blob/master/cookbot/spiders/allrecipes.py
class RecipesSpider(scrapy.Spider):
    name = "recipes"
    download_delay = 1

    def start_requests(self):
        data = [
            {'country': 'Deutschland', 'source': 'chefkoch.de', 'category': 'Frühstück', 'url': 'https://www.chefkoch.de/rs/s0g31/Fruehstuecksrezepte.html'},
         #  {'country': 'Deutschland', 'source': 'kochbar.de', 'category': 'Hauptgerichte', 'url': 'https://www.kochbar.de/kochen/hauptspeisen-zubereiten-hauptgerichte.html'}
         #  {'country': 'Deutschland', 'source': 'daskochrezept.de', 'category': 'Hauptgerichte', 'url': 'https://www.daskochrezept.de/suche?search=Hauptgericht'},
         #  {'country': 'Deutschland', 'source': 'oetker.de', 'category': 'Hauptgerichte', 'url': 'https://www.oetker.de/kochen/hauptspeisen'},

         # {'country': 'Oestereich', 'source': 'gutekueche.at', 'category': 'Hauptspeisen', 'url': 'https://www.gutekueche.at/hauptspeisen-alle-rezepte'},
         #  {'country': 'Oestereich', 'source': 'kochrezepte.at', 'category': 'Hauptspeisen', 'url': 'https://www.kochrezepte.at/hauptspeisen-rezepte'},
         #  {'country': 'Oestereich', 'source': 'issgesund.at', 'category': 'Hauptspeisen', 'url': 'https://www.issgesund.at/t/hauptspeisen'},
         #  {'country': 'Oestereich', 'source': 'steiermark.com', 'category': 'Hauptspeisen', 'url': 'https://www.steiermark.com/de/urlaub/essen-trinken/rezepte?form-area-content-teasergrid-2--category-content-teasergrid-2=677804'},

         #  {'country': 'Schweiz', 'source': 'gutekueche.ch', 'category': 'Hauptspeisen', 'url': 'https://www.gutekueche.ch/hauptspeisen-alle-rezepte'},
         #  {'country': 'Schweiz', 'source': 'migusto.migros.ch', 'category': 'Hauptgericht', 'url': 'https://migusto.migros.ch/de/s/?q=Hauptgericht'},
         # {'country': 'Schweiz', 'source': 'fooby.ch', 'category': 'Hauptgericht', 'url': 'https://fooby.ch/de/suche.html?query=hauptgericht&start=0&filters[treffertyp]=rezepte&filters[menuart][0]=hauptgericht&filters[region][0]=schweiz&y=100&x=0'}

        ]
        for item in data:
            yield scrapy.Request(url=item['url'], callback=self.parse, cb_kwargs=dict(country=item['country'], source=item['source'], category=item['category']))

    def parse(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        # define source specific css
        list_items_css = get_css_item(kwargs['source'], 'list-items')
        list_item_header_css = get_css_item(kwargs['source'], 'list-item-header')
        list_item_url_css = get_css_item(kwargs['source'], 'list-item-url')
        list_item_next_css = get_css_item(kwargs['source'], 'list-item-next')

        # get infos from overview page
        for overviewRecipe in response.css(list_items_css):
            title = overviewRecipe.css(list_item_header_css).get(default='')
            url = overviewRecipe.css(list_item_url_css).get(default='')

            request = scrapy.Request(url, callback=self.parse_recipe, cb_kwargs=dict(main_url=response.url))
            request.cb_kwargs['title'] = title
            request.cb_kwargs['country'] = kwargs['country']
            request.cb_kwargs['source'] = kwargs['source']
            request.cb_kwargs['category'] = kwargs['category']
            yield request

        # next_page = response.css(list_item_next_css).get()
        # if next_page is not None:
        #     self.logger.info('Proceeding with next page')
        #     yield response.follow(next_page, self.parse)

    def parse_recipe(self, response, **kwargs):
        self.logger.info('Processing recipe from {}'.format(response.url))

        # define source specific css
        ingredients_css = get_css_item(kwargs['source'], 'ingredients')
        ingredient_amount_css = get_css_item(kwargs['source'], 'ingredient-amount')
        ingredient_name_css = get_css_item(kwargs['source'], 'ingredient-name')
        ingredient_name_secondary_css = get_css_item(kwargs['source'], 'ingredient-name-secondary')

        ingredients = []
        for ingredientRow in response.css(ingredients_css):
            amount = ingredientRow.css(ingredient_amount_css).get(default='')  # amount + unit
            ingredient = ingredientRow.css(ingredient_name_css).get(default='')  # ingredient
            ingredient = cleanse_ingredient(ingredient)
            if ingredient == '':
                ingredient = ingredientRow.css(ingredient_name_secondary_css).get(default='')
                ingredient = cleanse_ingredient(ingredient)
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
