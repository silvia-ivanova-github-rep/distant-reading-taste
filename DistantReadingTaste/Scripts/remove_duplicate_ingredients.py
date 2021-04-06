import sys
import re
import MySQLdb
import csv

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)


# cursor.execute("SELECT MAX(id) AS id, edamam_food_id FROM ingredients WHERE edamam_food_id<>'' AND edamam_food_id IS NOT NULL GROUP BY edamam_food_id HAVING COUNT(*) > 1")
# result = cursor.fetchall()
# for row in result:
#     print(row['edamam_food_id'])
#
#     sql = "SELECT * FROM ingredients WHERE edamam_food_id=%s AND id<>%s"
#     cursor.execute(sql, (row['edamam_food_id'], row['id']))
#     result2 = cursor.fetchall()
#
#     for row2 in result2:
#         sql = "UPDATE recipe_ingredients SET ingredient_id=%s WHERE ingredient_id=%s"
#         cursor.execute(sql, (row['id'], row2['id']))
#         conn.commit()
#         sql = "DELETE FROM ingredients WHERE id=%s"
#         cursor.execute(sql, (row2['id'],))
#         conn.commit()


cursor.execute("SELECT MAX(id) AS max_id, name FROM ingredients WHERE name<>'' GROUP BY name HAVING COUNT(*) > 1")
result = cursor.fetchall()
for row in result:
    print(row['name'])

    sql = "SELECT MAX(id) AS max_id FROM ingredients WHERE name=%s AND name_en<>'' AND name_en IS NOT NULL LIMIT 1"
    cursor.execute(sql, (row['name'],))
    result2 = cursor.fetchone()
    if result2['max_id']:
        max_id = result2['max_id']
    else:
        max_id = row['max_id']

    sql = "SELECT * FROM ingredients WHERE name=%s AND id<>%s"
    cursor.execute(sql, (row['name'], max_id))
    result3 = cursor.fetchall()

    for row3 in result3:
        sql1 = "UPDATE recipe_ingredients SET ingredient_id=%s WHERE ingredient_id=%s"
        cursor.execute(sql1, (max_id, row3['id']))
        conn.commit()
        sql2 = "DELETE FROM ingredients WHERE id=%s"
        cursor.execute(sql2, (row3['id'],))
        conn.commit()
        print(cursor.rowcount, "record(s) deleted")

conn.close()
