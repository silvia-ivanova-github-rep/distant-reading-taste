import sys
import re
import MySQLdb
import csv

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)


cursor.execute("SELECT MIN(id) AS id, name FROM ingredients GROUP BY name HAVING COUNT(*) > 1")
result = cursor.fetchall()
for row in result:
    print(row['name'])

    sql = "SELECT * FROM ingredients WHERE name=%s AND id<>%s"
    cursor.execute(sql, (row['name'], row['id']))
    result2 = cursor.fetchall()

    for row2 in result2:
        sql = "UPDATE recipe_ingredients SET ingredient_id=%s WHERE ingredient_id=%s"
        cursor.execute(sql, (row['id'], row2['id']))
        conn.commit()
        sql = "DELETE FROM ingredients WHERE id=%s"
        cursor.execute(sql, (row2['id'],))
        conn.commit()


conn.close()
