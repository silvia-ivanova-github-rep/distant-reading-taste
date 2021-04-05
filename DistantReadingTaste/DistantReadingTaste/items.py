# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Ingredient(Item):
    name = Field()
    name_en = Field()
    quantity = Field()
    unit = Field()


class Nutrients(Item):
    energy = Field()
    fat = Field()
    saturated_fat = Field()
    sugar = Field()
    protein = Field()
    fibre = Field()
    carbohydrates = Field()
    sodium = Field()


class Recipe(Item):
    title = Field()
    source = Field()
    category = Field()
    country = Field()
    url = Field()
    ingredients = Field()
    nutrients = Field()
