import sys
import time
import MySQLdb

from googletrans import Translator
from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

t = Translator()

cursor.execute("SELECT * FROM ingredients WHERE name_en IS NULL OR name_en = ''")
rows = cursor.fetchall()
for row in rows:
    time.sleep(0.5)
    name = row['name']
    if not name:
        continue
    translated = t.translate(name, src='de', dest='en')
    if translated:
        print(translated.origin, ' > ', translated.text)
        sql = "UPDATE ingredients SET name_en=%s, updated_at=%s WHERE id=%s"
        values = (translated.text, time.strftime('%Y-%m-%d %H:%M:%S'), row['id'])
        cursor.execute(sql, values)
        conn.commit()

conn.close()




