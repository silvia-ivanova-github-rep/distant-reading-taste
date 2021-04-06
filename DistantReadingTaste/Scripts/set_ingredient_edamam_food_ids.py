import json
import requests
import sys
import time
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
    time.sleep(1.6)  # api allows only 100 queries per minute
    name_en = row['name_en']
    print(name_en)
    result = api_query(name_en)
    if result:
        if result['parsed']:
            item = result['parsed'][0]
        elif result['hints']:
            item = result['hints'][0]
        else:
            continue

        food_id = item['food']['foodId']  # e.g. food_abiw5baauresjmb6xpap2bg3otzu
        food_label = item['food']['label']

        print('Ingredient: ', name_en, ' (', food_label, ')')

        sql = "UPDATE ingredients SET edamam_food_id=%s, alt_name_1=%s, updated_at=%s WHERE id=%s"
        values = (food_id, food_label, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
        cursor.execute(sql, values)
        conn.commit()

conn.close()
