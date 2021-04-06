import MySQLdb
import sys
import time

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST


def num(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return 0
        
        
conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("SELECT * FROM recipes WHERE source_id=2")
result = cursor.fetchall()

for row in result:
    title = row['title']
    print('Recipe: ', title)

    sql = "SELECT * FROM recipe_ingredients AS ri JOIN ingredients AS i ON ri.ingredient_id = i.id WHERE ri.recipe_id=%s"
    cursor.execute(sql, (row['id'],))
    result2 = cursor.fetchall()

    energy = 0.0
    carbohydrates = 0.0
    fat = 0.0
    saturated_fat = 0.0
    sugar = 0.0
    protein = 0.0
    fibre = 0.0
    sodium = 0.0

    for row2 in result2:
        factor = num(row2['weight']) / 100
        energy += num(row['energy']) * factor
        carbohydrates += num(row['carbohydrates']) * factor
        fat += num(row['fat']) * factor
        saturated_fat += num(row['saturated_fat']) * factor
        sugar += num(row['sugar']) * factor
        protein += num(row['protein']) * factor
        fibre += num(row['fibre']) * factor
        sodium += num(row['sodium']) * factor

    # use existing data if available
    if row['energy']:
        print(energy, row['energy'])
        energy = row['energy']
    if row['carbohydrates']:
        print(carbohydrates, row['carbohydrates'])
        carbohydrates = row['carbohydrates']
    if row['fat']:
        print(fat, row['fat'])
        fat = row['fat']
    if row['saturated_fat']:
        print(saturated_fat, row['saturated_fat'])
        saturated_fat = row['saturated_fat']
    if row['sugar']:
        print(sugar, row['sugar'])
        sugar = row['sugar']
    if row['protein']:
        print(protein, row['protein'])
        protein = row['protein']
    if row['fibre']:
        print(fibre, row['fibre'])
        fibre = row['fibre']
    if row['sodium']:
        print(sodium, row['sodium'])
        sodium = row['sodium']

    sql = "UPDATE recipes SET energy=%s, carbohydrates=%s, fat=%s, saturated_fat=%s, sugar=%s, protein=%s, fibre=%s, sodium=%s, updated_at=%s WHERE id=%s"
    values = (energy, carbohydrates, fat, saturated_fat, sugar, protein, fibre, sodium, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
    cursor.execute(sql, values)
    conn.commit()

conn.close()
