import json
import requests
import sys
import time
import MySQLdb

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, APP_KEY, APP_ID


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
cursor.execute("SELECT * FROM ingredients WHERE edamam_food_id IS NOT NULL AND energy IS NULL")
rows = cursor.fetchall()

headers = {'Content-Type': 'application/json'}
params = (('app_id', APP_ID), ('app_key', APP_KEY))

for row in rows:
    name = row['name_en']
    print('Ingredient: ', name)

    time.sleep(0.7)  # api allows only 100 queries per minute

    data = {"ingredients": [
        {
            "quantity": 100,
            "measureURI": "http://www.edamam.com/ontologies/edamam.owl#Measure_gram",
            "foodId": row['edamam_food_id']
        }
    ]}

    json_data = json.dumps(data)
    response = requests.post('https://api.edamam.com/api/food-database/v2/nutrients', headers=headers, params=params, data=json_data)

    if response.status_code == 200:
        result = json.loads(response.content.decode('utf-8'))
        energy = get_key(result, 'totalNutrients', 'ENERC_KCAL', 'quantity')
        fat = get_key(result, 'totalNutrients', 'FAT', 'quantity')
        saturated_fat = get_key(result, 'totalNutrients', 'FASAT', 'quantity')
        fiber = get_key(result, 'totalNutrients', 'FIBTG', 'quantity')
        sodium = get_key(result, 'totalNutrients', 'NA', 'quantity')
        carbohydrates = get_key(result, 'totalNutrients', 'CHOCDF', 'quantity')
        protein = get_key(result, 'totalNutrients', 'PROCNT', 'quantity')
        sugar = get_key(result, 'totalNutrients', 'SUGAR', 'quantity')

        print('  energy: ', energy)
        print('  fat: ', fat)
        print('  saturated_fat: ', saturated_fat)
        print('  fiber: ', fiber)
        print('  sodium: ', sodium)
        print('  carbohydrates: ', carbohydrates)
        print('  protein: ', protein)
        print('  sugar: ', sugar)

        sql = "UPDATE ingredients SET energy=%s, carbohydrates=%s, fat=%s, saturated_fat=%s, sugar=%s, protein=%s, fibre=%s, sodium=%s, updated_at=%s WHERE id=%s"
        values = (energy, carbohydrates, fat, saturated_fat, sugar, protein, fiber, sodium, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
        cursor.execute(sql, values)
        conn.commit()


conn.close()
