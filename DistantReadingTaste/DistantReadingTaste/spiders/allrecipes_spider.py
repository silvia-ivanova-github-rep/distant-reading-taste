import re

from scrapy.spiders import CrawlSpider
from scrapy.http import Request

from ..items import Recipe, Ingredient, Nutrients




class AllrecipesSpider(CrawlSpider):
    name = 'allrecipes'
    # download_delay = 1

    def start_requests(self):
        data = [
            {'category': 'Main Dish', 'url': 'https://www.allrecipes.com/recipes/80/main-dish/?page=2'},  # page 1 has no "next" button
            # {'category': 'Everyday Cooking', 'url': 'https://www.allrecipes.com/recipes/1642/everyday-cooking/?page=2'},
            # {'category': 'US Recipes', 'url': 'https://www.allrecipes.com/recipes/236/us-recipes/?page=2'},
            # {'category': 'Soups, Stews and Chili', 'url': 'https://www.allrecipes.com/recipes/94/soups-stews-and-chili/?page=2'},
            # {'category': 'Seafood', 'url': 'https://www.allrecipes.com/recipes/93/seafood/?page=2'},
            # {'category': 'Pasta and Noodles', 'url': 'https://www.allrecipes.com/recipes/95/pasta-and-noodles/?page=2'},
            # {'category': 'Meat and Poultry', 'url': 'https://www.allrecipes.com/recipes/92/meat-and-poultry/?page=2'},
            # {'category': 'Lunch', 'url': 'https://www.allrecipes.com/recipes/17561/lunch/?page=2'},
            # {'category': 'Healthy Recipes', 'url': 'https://www.allrecipes.com/recipes/84/healthy-recipes/?page=2'},
            # {'category': 'Dinner', 'url': 'https://www.allrecipes.com/recipes/17562/dinner/?page=2'},
            # {'category': 'BBQ Grilling', 'url': 'https://www.allrecipes.com/recipes/88/bbq-grilling/?page=2'},
        ]
        for item in data:
            yield Request(url=item['url'], callback=self.parse, cb_kwargs=dict(category=item['category']))

    def parse(self, response, **kwargs):
        # self.logger.info('Got successful response from {}'.format(response.url))

        # get infos from overview page
        for recipePreview in response.css('div.component.tout'):
            url = recipePreview.css('a.tout__titleLink::attr("href")').get(default='')
            url = 'https://www.allrecipes.com' + url

            request = Request(url, callback=self.parse_recipe)
            request.cb_kwargs['category'] = kwargs['category']
            yield request

        # next_page = response.css('a.category-page-list-related-nav-next-button::attr(href)').get()
        # self.logger.info('NEXT {}'.format(next_page))
        # if next_page is not None:
        #     self.logger.info('Proceeding with next page')
        #     yield response.follow(url=next_page, callback=self.parse, cb_kwargs=dict(category=kwargs['category']))

    def parse_recipe(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        recipe = Recipe()
        recipe['title'] = response.css('h1.headline.heading-content::text').get(default='')
        recipe['url'] = response.url
        recipe['country'] = 'USA'
        recipe['source'] = 'allrecipes.com'
        recipe['category'] = kwargs['category']

        ingredients = []
        for ingredientRow in response.css('section.recipe-ingredients-new li.ingredients-item'):
            ingredient = Ingredient()
            ingredient_str = ingredientRow.css('span.ingredients-item-name::text').get(default='').strip()  # ingredient

            ingredient_str = re.sub(r'\(.*?\)|\*', '', ingredient_str)  # remove brackets and their content

            quantity = ''
            quantity_search = re.search(r'^[\d\s\.\,\u00BC-\u00BE\u2150-\u215E\u2189\/]+', ingredient_str)
            if quantity_search:
                quantity = quantity_search[0].strip()
                ingredient_str = re.sub(quantity, '', ingredient_str, 1)  # remove quantity from string

            unit = ''
            units = ['teaspoon', 'tablespoon', 'fluid ounce', 'gill', 'cup', 'can', 'bit', 'stalk', 'cube', 'pint', 'pinch', 'pinches', 'quart', 'gallon', 'pound', 'ounce',
                     'milligram', 'milligramme', 'gram', 'gramme', 'kilogram', 'kilogramme', 'deciliter', 'decilitre', 'milliliter', 'millilitre', 'liter', 'litre', 'dL', 'mg',
                     'g', 'kg', 'ml', 'l', 'L', 'dl', 'lb', 'oz', 't', 'tsp', 'tsp.', 'T', 'tbl', 'tbl.', 'tbs', 'tbs.', 'tbsp', 'tbsp.', 'fl oz', 'c', 'p', 'pt', 'fl pt', 'q',
                     'qt', 'pkg', 'pkg.', 'fl qt', 'gal', 'cc', 'mL', 'package', 'clove', 'bottle', 'jar', 'container', 'sleeve', 'head', 'tub', 'slice', 'bunch', 'rib',
                     'carton', 'bag', 'sprig', 'dash', 'dashes']
            for u in units:
                unit_search = re.search(rf'\b({u}s?)\b', ingredient_str)
                if unit_search:
                    unit = unit_search[0].strip()
                    ingredient_str = re.sub(unit, '', ingredient_str, 1)  # remove unit from string
                    break

            omitted_words = ['thick-cut', 'large', 'small', 'medium', 'jumbo', 'thick', 'thinly', 'minced', 'diced', 'cooked', 'cut', 'chopped', 'sliced', 'grated', 'to taste', 'cubed', 'fresh', 'toasted',
                             'shredded', 'prepared', 'crushed', 'whole', 'finely', 'uncooked', 'cooked', 'freshly', 'for frying', 'sauteed', 'reserved', 'frozen', 'raw',
                             'cold', 'processed', 'peeled', 'halved', 'julienned', 'juiced']
            for o in omitted_words:
                ingredient_str = re.sub(rf'\b{o}s?\b', '', ingredient_str)

            ingredient_str = re.sub(r',;|\bor\b.*', '', ingredient_str)  # remove everything after delimiters
            ingredient_str = re.sub(r'\s\s+', ' ', ingredient_str).strip()  # remove multiple whitespaces

            ingredient['name'] = ''
            ingredient['name_en'] = ingredient_str
            ingredient['quantity'] = quantity
            ingredient['unit'] = unit
            ingredients.append(ingredient)

        recipe['ingredients'] = ingredients

        nutrients = Nutrients()
        nutrients['energy'] = response.css('section.recipe-nutrition .nutrition-top::text').getall()[2].strip()
        for nutrientRow in response.css('section.recipe-nutrition .nutrition-body .nutrition-row'):
            nutrient_name = nutrientRow.css('span.nutrient-name::text').get(default='').strip()
            nutrient_value = nutrientRow.css('span.nutrient-name span[aria-label]::attr(aria-label)').get(default='').strip()
            if nutrient_name == 'protein:':
                nutrients['protein'] = nutrient_value
            elif nutrient_name == 'carbohydrates:':
                nutrients['carbohydrates'] = nutrient_value
            elif nutrient_name == 'fat:':
                nutrients['fat'] = nutrient_value
            elif nutrient_name == 'saturated fat:':
                nutrients['saturated_fat'] = nutrient_value
            elif nutrient_name == 'sugars:':
                nutrients['sugar'] = nutrient_value
            elif nutrient_name == 'dietary fiber:':
                nutrients['fibre'] = nutrient_value
            elif nutrient_name == 'sodium:':
                nutrients['natrium'] = nutrient_value

        recipe['nutrients'] = nutrients

        # self.logger.info(recipe)

        # process recipe in pipeline
        yield recipe

