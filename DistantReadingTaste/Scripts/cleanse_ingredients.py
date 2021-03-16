import sys
import time
import MySQLdb
import csv

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

data = {}
with open('ingredient_data.csv', newline='') as f:
    reader = csv.reader(f)
    for item in reader:
        cursor.execute("SELECT * FROM ingredients WHERE name='%s' LIMIT 1" % (item[1]))
        result = cursor.fetchone()
        if result is not None:  # target value name already exists
            cursor.execute("SELECT * FROM ingredients WHERE name='%s' LIMIT 1" % (item[0]))
            row = cursor.fetchone()
            if row is not None:
                cursor.execute("UPDATE recipe_ingredients SET ingredient_id='%s' WHERE ingredient_id='%s'" % (result['id'], row['id']))
                conn.commit()
                cursor.execute("DELETE FROM ingredients WHERE id='%s'" % (row['id']))
                conn.commit()
        else:
            cursor.execute("UPDATE ingredients SET name='%s' WHERE name='%s'" % (item[1], item[0]))
            conn.commit()

conn.close()
