import sys
import MySQLdb

from googletrans import Translator
from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

t = Translator()

cursor.execute("SELECT * FROM ingredients")
rows = cursor.fetchall()
for row in rows:
    name = row['name']
    translated = t.translate(name, src='de', dest='en')
    if translated:
        print(translated.origin, ' > ', translated.text)
        cursor.execute("UPDATE ingredients SET name_en='%s' WHERE id='%s'" % (translated.text, row['id']))
        conn.commit()

conn.close()




