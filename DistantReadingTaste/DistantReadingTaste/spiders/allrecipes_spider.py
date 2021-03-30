import re

from scrapy.spiders import CrawlSpider
from scrapy.http import Request

from ..items import Recipe, Ingredient, Nutrients




class AllrecipesSpider(CrawlSpider):
    name = 'allrecipes'
    download_delay = 1

    def start_requests(self):
        data = [
            {'category': 'Hauptspeise', 'url': 'https://www.allrecipes.com/recipes/80/main-dish/?page=2'},  # page 1 has not a "next" button
        ]
        for item in data:
            yield Request(url=item['url'], callback=self.parse, cb_kwargs=dict(category=item['category']))

    def parse(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        # get infos from overview page
        for recipePreview in response.css('div.component.tout'):
            url = recipePreview.css('a.tout__titleLink::attr("href")').get(default='')
            url = 'https://www.allrecipes.com' + url

            request = Request(url, callback=self.parse_recipe)
            request.cb_kwargs['category'] = kwargs['category']
            yield request

        next_page = response.css('a.category-page-list-related-nav-next-button::attr(href)').get()
        self.logger.info('NEXT {}'.format(next_page))
        if next_page is not None:
            self.logger.info('Proceeding with next page')
            yield response.follow(url=next_page, callback=self.parse, cb_kwargs=dict(category=kwargs['category']))

    def parse_recipe(self, response, **kwargs):
        self.logger.info('Got successful response from {}'.format(response.url))

        recipe = Recipe()
        recipe['title'] = response.css('h1.headline.heading-content::text').get(default='')
        recipe['url'] = response.url
        recipe['country'] = 'USA'
        recipe['source'] = 'allrecipes.com'

        ingredients = []
        for ingredientRow in response.css('section.recipe-ingredients-new li.ingredients-item'):
            ingredient = Ingredient()
            name = ingredientRow.css('span.ingredients-item-name::text').get(default='').strip()  # ingredient
            name = re.sub(r'\(.*?\)|,.*|\sor', '', name)  # remove delimiter, brackets and their content
            name = re.sub(r'\s\s+', ' ', name)  # remove multiple whitespaces

            self.logger.info('INGREDIENT:' + name)

            ingredient['name'] = name
            #ingredient['quantity'] = quantity
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

        self.logger.info(recipe)
        self.logger.info(ingredients)
        self.logger.info(nutrients)

        # process recipe in pipeline
        #yield recipe

