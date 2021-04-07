import MySQLdb
import sys
import time

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST


def num(s):
    if not s:
        return 0
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
        energy += num(row2['energy']) * factor
        carbohydrates += num(row2['carbohydrates']) * factor
        fat += num(row2['fat']) * factor
        saturated_fat += num(row2['saturated_fat']) * factor
        sugar += num(row2['sugar']) * factor
        protein += num(row2['protein']) * factor
        fibre += num(row2['fibre']) * factor
        sodium += num(row2['sodium']) * factor

    # use existing data if available
    if row['energy'] and row['energy'] != '0':
        print(energy, row['energy'])
        energy = row['energy']
    if row['carbohydrates'] and row['carbohydrates'] != '0':
        print(carbohydrates, row['carbohydrates'])
        carbohydrates = row['carbohydrates']
    if row['fat'] and row['fat'] != '0':
        print(fat, row['fat'])
        fat = row['fat']
    if row['saturated_fat'] and row['saturated_fat'] != '0':
        print(saturated_fat, row['saturated_fat'])
        saturated_fat = row['saturated_fat']
    if row['sugar'] and row['sugar'] != '0':
        print(sugar, row['sugar'])
        sugar = row['sugar']
    if row['protein'] and row['protein'] != '0':
        print(protein, row['protein'])
        protein = row['protein']
    if row['fibre'] and row['fibre'] != '0':
        print(fibre, row['fibre'])
        fibre = row['fibre']
    if row['sodium'] and row['sodium'] != '0':
        print(sodium, row['sodium'])
        sodium = row['sodium']

    sql = "UPDATE recipes SET energy=%s, carbohydrates=%s, fat=%s, saturated_fat=%s, sugar=%s, protein=%s, fibre=%s, sodium=%s, updated_at=%s WHERE id=%s"
    values = (energy, carbohydrates, fat, saturated_fat, sugar, protein, fibre, sodium, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
    cursor.execute(sql, values)
    conn.commit()

conn.close()
