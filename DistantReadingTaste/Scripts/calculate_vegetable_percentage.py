import json
import requests
import sys
import time
import re
import MySQLdb

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, APP_KEY, APP_ID

API_URL_BASE = 'https://api.edamam.com/api/food-database/v2/'


def get_key(element, *keys):
    # Check if *keys (nested) exists in `element` (dict).
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')
    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return None
    return _element


def api_query(ingredient):
    api_url = '{0}parser'.format(API_URL_BASE)
    payload = {'ingr': ingredient, 'app_id': APP_ID, 'app_key': APP_KEY}
    response = requests.get(api_url, params=payload)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("SELECT * FROM ingredients WHERE edamam_food_id IS NULL")
result = cursor.fetchall()

for row in result:
    time.sleep(1.5)  # api allows only 100 queries per minute
    name_en = row['name_en']
    print('Ingredient: ', name_en)

    result = api_query(name_en)
    if result:
        if result['parsed']:
            item = result['parsed'][0]
        elif result['hints']:
            item = result['hints'][0]
        else:
            continue

        food_id = item['food']['foodId']  # e.g. food_abiw5baauresjmb6xpap2bg3otzu

        sql = "UPDATE ingredients SET edamam_food_id=%s, updated_at=%s WHERE id=%s"
        values = (food_id, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
        cursor.execute(sql, values)
        conn.commit()

        sql = "SELECT * FROM recipe_ingredients WHERE ingredient_id=%s"
        cursor.execute(sql, (row['id'],))
        r = cursor.fetchall()
        for ri in r:
            amount = ri['amount']
            unit = ri['unit']
            print('   quantity: ', amount, ' ', unit)

            # t['hints'][0]['measures'][0]['qualified'][3]['qualifiers'][0]['label']
            # m = result['hints'][0]['measures']
            weight = ''
            for x in result['hints']:
                m = x['measures']
                if unit:
                    unit = re.sub(r's$', '', unit).capitalize()
                    m1 = next((item for item in m if unit in item.values() and item['label'] == unit), False)
                    if m1:
                        if 'weight' in m1:
                            weight = m1['weight']
                        elif 'qualified' in m1:
                            weight = m1['qualified'][0]['weight']
                        break

                if not weight:
                    m1 = next((item for item in m if 'Whole' in item.values() and item['label'] == 'Whole'), False)
                    if m1:
                        weight = m1['weight']
                        break

            print('   weight: ', weight)

            if weight:
                weight_sum = float(amount) * float(weight)

                sql = "UPDATE recipe_ingredients SET weight=%s WHERE id=%s"
                cursor.execute(sql, (weight_sum, ri['id']))


cursor.execute("SELECT * FROM recipes where vegetables_fruits IS NULL")
result = cursor.fetchall()

for row in result:
    title = row['title']
    print('Recipe: ', title)

    sql = "SELECT ri.weight, i.* FROM recipe_ingredients AS ri JOIN ingredients AS i ON ri.ingredient_id = i.id WHERE ri.recipe_id=%s"
    cursor.execute(sql, (row['id'],))
    r = cursor.fetchall()

    weight_vegetable = 0
    weight_rest = 0
    for item in r:
        if item['weight'] is None:
            weight = 0
        else:
            weight = float(item['weight'])

        if item['type_id'] in [1, 2, 3, 4]:
            weight_vegetable += weight
        else:
            weight_rest += weight

    weight_vegetable_percent = weight_vegetable / (weight_vegetable + weight_rest)

    sql = "UPDATE recipes SET vegetables_fruits=%s WHERE id=%s"
    cursor.execute(sql, (weight_vegetable_percent, row['id']))
    conn.commit()


