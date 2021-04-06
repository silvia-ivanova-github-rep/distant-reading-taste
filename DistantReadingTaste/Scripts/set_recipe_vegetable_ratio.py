import sys
import MySQLdb

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("SELECT * FROM recipes WHERE vegetables_fruits IS NULL")
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

    if weight_vegetable == 0:
        weight_vegetable_percent = 0
    else:
        weight_vegetable_percent = weight_vegetable / (weight_vegetable + weight_rest)

    sql = "UPDATE recipes SET vegetables_fruits=%s WHERE id=%s"
    cursor.execute(sql, (weight_vegetable_percent, row['id']))
    conn.commit()

conn.close()
