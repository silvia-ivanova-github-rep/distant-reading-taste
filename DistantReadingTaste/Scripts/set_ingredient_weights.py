import json
import requests
import sys
import time
import MySQLdb

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, APP_KEY, APP_ID


def num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return 1


conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

headers = {'Content-Type': 'application/json'}
params = (('app_id', APP_ID), ('app_key', APP_KEY))
measure_uris = {'Tablespoon': 'http://www.edamam.com/ontologies/edamam.owl#Measure_tablespoon',
                'Teaspoon': 'http://www.edamam.com/ontologies/edamam.owl#Measure_teaspoon',
                'Ounce': 'http://www.edamam.com/ontologies/edamam.owl#Measure_ounce',
                'Gram': 'http://www.edamam.com/ontologies/edamam.owl#Measure_gram',
                'Pound': 'http://www.edamam.com/ontologies/edamam.owl#Measure_pound',
                'Kilogram': 'http://www.edamam.com/ontologies/edamam.owl#Measure_kilogram',
                'Pinch': 'http://www.edamam.com/ontologies/edamam.owl#Measure_pinch',
                'Liter': 'http://www.edamam.com/ontologies/edamam.owl#Measure_liter',
                'Fluid ounce': 'http://www.edamam.com/ontologies/edamam.owl#Measure_fluid_ounce',
                'Gallon': 'http://www.edamam.com/ontologies/edamam.owl#Measure_gallon',
                'Pint': 'http://www.edamam.com/ontologies/edamam.owl#Measure_pint',
                'Quart': 'http://www.edamam.com/ontologies/edamam.owl#Measure_quart',
                'Milliliter': 'http://www.edamam.com/ontologies/edamam.owl#Measure_milliliter',
                'Drop': 'http://www.edamam.com/ontologies/edamam.owl#Measure_drop',
                'Cup': 'http://www.edamam.com/ontologies/edamam.owl#Measure_cup',
                'Can': 'http://www.edamam.com/ontologies/edamam.owl#Measure_can',
                'Clove': 'http://www.edamam.com/ontologies/edamam.owl#Measure_clove',
                'Milligram': 'http://www.edamam.com/ontologies/edamam.owl#Measure_milligram',
                'Dash': 'http://www.edamam.com/ontologies/edamam.owl#Measure_dash',
                'Serving': 'http://www.edamam.com/ontologies/edamam.owl#Measure_serving',
                'Handful': 'http://www.edamam.com/ontologies/edamam.owl#Measure_handful',
                'Bunch': 'http://www.edamam.com/ontologies/edamam.owl#Measure_bunch',
                'Carton': 'http://www.edamam.com/ontologies/edamam.owl#Measure_carton',
                'Bottle': 'http://www.edamam.com/ontologies/edamam.owl#Measure_bottle',
                'Bag': 'http://www.edamam.com/ontologies/edamam.owl#Measure_bag'}
DEFAULT_MEASURE_URI = 'http://www.edamam.com/ontologies/edamam.owl#Measure_unit'

cursor.execute("SELECT ingredient_id, name_en, amount, unit, edamam_food_id "
               "FROM recipe_ingredients ri "
               "JOIN ingredients i on ri.ingredient_id = i.id "
               "JOIN recipes r on ri.recipe_id = r.id "
               "WHERE ri.weight IS NULL AND r.source_id=2 "
               "GROUP BY ingredient_id, name_en, amount, unit, edamam_food_id")
result = cursor.fetchall()

for row in result:
    time.sleep(0.7)  # api allows only 100 queries per minute
    name = row['name_en']
    food_id = row['edamam_food_id']
    print(name, row['amount'], row['unit'])

    measure_uri = measure_uris.get(row['unit'], DEFAULT_MEASURE_URI)
    amount = num(row['amount'])

    data = {
        "ingredients": [
            {
                "quantity": amount,
                "measureURI": measure_uri,
                "foodId": food_id
            }
        ]
    }

    json_data = json.dumps(data)
    response = requests.post('https://api.edamam.com/api/food-database/v2/nutrients', headers=headers, params=params, data=json_data)

    if response.status_code == 200:
        result = json.loads(response.content.decode('utf-8'))
        weight = result['totalWeight']

        sql = "UPDATE recipe_ingredients SET weight=%s WHERE ingredient_id=%s AND amount=%s AND unit=%s"
        cursor.execute(sql, (weight, row['ingredient_id'], row['amount'], row['unit']))
        conn.commit()
        print('   Weight with', measure_uri, '(', row['edamam_food_id'], ') => ', weight)
    else:
        print('   No weight found with', measure_uri, '(', row['edamam_food_id'], ')')

conn.close()
