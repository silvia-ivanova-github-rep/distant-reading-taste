import json
import requests
import sys
import time
import MySQLdb

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, APP_KEY, APP_ID

api_url_base = 'https://api.edamam.com/api/food-database/v2/'


def get_nutrients(ingredient):
    api_url = '{0}parser'.format(api_url_base)
    payload = {'ingr': ingredient, 'app_id': APP_ID, 'app_key': APP_KEY}
    response = requests.get(api_url, params=payload)
    print(response.url)
    # print(response.text)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


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


conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')

cursor = conn.cursor(MySQLdb.cursors.DictCursor)

# get ingredients from database
cursor.execute("SELECT * FROM ingredients")
rows = cursor.fetchall()

for row in rows:
    if not row['name_en']:
        continue

    data = get_nutrients(row['name_en'])

    if data['parsed']:
        parsed = data['parsed'][0]
        energy = get_key(parsed, 'food', 'nutrients', 'ENERC_KCAL')
        protein = get_key(parsed, 'food', 'nutrients', 'PROCNT')
        fat = get_key(parsed, 'food', 'nutrients', 'FAT')
        saturated_fat = get_key(parsed, 'food', 'nutrients', 'FASAT')
        carbs = get_key(parsed, 'food', 'nutrients', 'CHOCDF')
        fiber = get_key(parsed, 'food', 'nutrients', 'FIBTG')
        sugar = get_key(parsed, 'food', 'nutrients', 'SUGAR')
        salt = get_key(parsed, 'food', 'nutrients', 'SALT')

        sql = "UPDATE ingredients SET energy=%s, fat=%s, saturated_fat=%s, sugar=%s, protein=%s, fibre=%s, salt=%s, updated_at=%s WHERE id=%s"
        values = (energy, fat, saturated_fat, sugar, protein, fiber, salt, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
        cursor.execute(sql, values)
        conn.commit()
        print(cursor.rowcount, "record(s) affected")
    else:
        print('[!] Request Failed')


conn.close()
