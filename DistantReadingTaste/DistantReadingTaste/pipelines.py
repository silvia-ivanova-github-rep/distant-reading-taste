# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
import time
# useful for handling different item types with a single interface
from scrapy.exceptions import NotConfigured


class RecipePipeline:
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:  # if we don't define db config in settings
            raise NotConfigured  # then reaise error
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)  # returning pipeline instance

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(db=self.db,
                                    user=self.user,
                                    passwd=self.passwd,
                                    host=self.host,
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def process_item(self, item, spider):
        source_id = self.get_source_id(item.get("source"), item.get("country"))
        category_id = self.get_category_id(item.get('category'))

        sql = "INSERT INTO recipes(source_id, category_id, title, url) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (
            source_id,
            category_id,
            item.get("title"),
            item.get("url")
        ))
        self.conn.commit()
        recipe_id = self.cursor.lastrowid
        self.save_recipe_ingredients(item.get("ingredients"), recipe_id)

        return item

    def close_spider(self, spider):
        self.conn.close()

    def get_source_id(self, source, country):
        self.cursor.execute("SELECT * FROM countries WHERE name=\"%s\" LIMIT 1" % (country,))
        result = self.cursor.fetchone()
        if result is None:
            print("ERROR: Country '%s' could not be found in database!" % (country,))
            return
        country_id = result['id']
        self.cursor.execute("SELECT * FROM sources WHERE country_id=\"%s\" AND name=\"%s\" LIMIT 1" % (country_id, source))
        result = self.cursor.fetchone()
        if result is None:  # source does not yet exist
            sql = "INSERT INTO sources(country_id, name, updated_at, created_at) VALUES(%s, %s, %s, %s)"
            self.cursor.execute(sql, (country_id, source, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))
            self.conn.commit()
            self.cursor.execute("SELECT * FROM sources WHERE country_id=\"%s\" AND name=\"%s\" LIMIT 1" % (country_id, source))
            result = self.cursor.fetchone()
        return result['id']

    def get_category_id(self, category):
        self.cursor.execute("SELECT * FROM categories WHERE name=\"%s\" LIMIT 1" % (category,))
        result = self.cursor.fetchone()
        if result is None:  # category does not yet exist
            sql = "INSERT INTO categories(name, updated_at, created_at) VALUES(%s, %s, %s)"
            self.cursor.execute(sql, (category, time.strftime('%Y-%m-%d %H:%M:%S'), time.strftime('%Y-%m-%d %H:%M:%S')))
            self.conn.commit()
            self.cursor.execute("SELECT * FROM categories WHERE name=\"%s\" LIMIT 1" % (category,))
            result = self.cursor.fetchone()
        return result['id']

    def save_recipe_ingredients(self, ingredients, recipe_id):
        for ingredient in ingredients:
            ingredient_id = self.get_or_create_ingredient(ingredient['ingredient'])
            amount = ingredient['amount']
            # split amount
            # unit_id = self.get_or_create_unit()

    def get_or_create_ingredient(self, ingredient):
        self.cursor.execute("SELECT * FROM ingredients WHERE name=\"%s\" OR alt_name_1=\"%s\" OR alt_name_2=\"%s\" OR alt_name_3=\"%s\"" % (ingredient, ingredient, ingredient, ingredient))
        result = self.cursor.fetchone()
        if result is None:  # ingredient does not yet exist
            return
        return result['id']
