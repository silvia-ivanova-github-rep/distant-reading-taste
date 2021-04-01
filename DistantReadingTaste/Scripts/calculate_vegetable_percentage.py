import json
import requests
import sys
import time
import re
import MySQLdb

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, APP_KEY, APP_ID

API_URL_BASSE = 'https://api.edamam.com/api/food-database/v2/'


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
    api_url = '{0}parser'.format(API_URL_BASSE)
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

cursor.execute("SELECT * FROM ingredients")
result = cursor.fetchall()

for row in result:
    time.sleep(1)
    name_en = row['name_en']

    result = api_query(name_en)
    if result:
        food_id = result['parsed'][0]['food']['foodId']  # e.g. food_abiw5baauresjmb6xpap2bg3otzu
        category = result['parsed'][0]['food']['category']  # e.g. 'Generic foods'
        type_id = 0
        if category == 'Generic foods':
            type_id = 5

        parsed = result['parsed'][0]
        energy = get_key(parsed, 'food', 'nutrients', 'ENERC_KCAL')
        protein = get_key(parsed, 'food', 'nutrients', 'PROCNT')
        fat = get_key(parsed, 'food', 'nutrients', 'FAT')
        saturated_fat = get_key(parsed, 'food', 'nutrients', 'FASAT')
        carbs = get_key(parsed, 'food', 'nutrients', 'CHOCDF')
        fiber = get_key(parsed, 'food', 'nutrients', 'FIBTG')
        sugar = get_key(parsed, 'food', 'nutrients', 'SUGAR')
        salt = get_key(parsed, 'food', 'nutrients', 'SALT')
        natrium = get_key(parsed, 'food', 'nutrients', 'NA')

        sql = "UPDATE ingredients SET type_id=%s, energy=%s, fat=%s, saturated_fat=%s, sugar=%s, protein=%s, fibre=%s, salt=%s, natrium=%s, edamam_food_id=%s, updated_at=%s WHERE id=%s"
        values = (type_id, energy, fat, saturated_fat, sugar, protein, fiber, salt, natrium, food_id, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
        cursor.execute(sql, values)
        conn.commit()

        sql = "SELECT * FROM recipe_ingredients WHERE ingredient_id=%s"
        cursor.execute(sql, (row['id'],))
        r = cursor.fetchall()
        for ri in r:
            amount = ri['amount']
            unit = ri['unit']
            print(name_en, ': ', amount, ' ', unit)

            # t['hints'][0]['measures'][0]['qualified'][3]['qualifiers'][0]['label']
            m = result['hints'][0]['measures']
            weight = ''
            if unit:
                unit = re.sub(r's$', '', unit).capitalize()
                m1 = next((item for item in m if item['label'] == unit), False)
                if m1:
                    weight = m1['weight']

            if not weight:
                m1 = next((item for item in m if item['label'] == 'Whole'), False)
                if m1:
                    weight = m1['weight']

            print("WEIGHT: ", weight)

            if weight:
                weight_sum = float(amount) * float(weight)

                sql = "UPDATE recipe_ingredients SET weight=%s WHERE id=%s"
                cursor.execute(sql, (weight_sum, ri['id']))






