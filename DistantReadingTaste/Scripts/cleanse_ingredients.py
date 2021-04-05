import sys
import re
import MySQLdb
import csv

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)


def update_ingredient(old_name, new_name):
    print(old_name, ' > ', new_name)
    sql = "SELECT * FROM ingredients WHERE name=%s LIMIT 1"
    cursor.execute(sql, (new_name,))
    result = cursor.fetchone()
    if result is not None:  # target value name already exists
        sql = "SELECT * FROM ingredients WHERE name=%s LIMIT 1"
        cursor.execute(sql, (old_name,))
        row = cursor.fetchone()
        if row is not None:
            sql = "UPDATE recipe_ingredients SET ingredient_id=%s WHERE ingredient_id=%s"
            cursor.execute(sql, (result['id'], row['id']))
            conn.commit()
            sql = "DELETE FROM ingredients WHERE id=%s"
            cursor.execute(sql, (row['id'],))
            conn.commit()
    else:
        sql = "UPDATE ingredients SET name=%s WHERE name=%s"
        cursor.execute(sql, (new_name, old_name))
        conn.commit()


def update_ingredient_with_id(ingredient_id, new_name):
    print(ingredient_id, ' > ', new_name)
    sql = "SELECT * FROM ingredients WHERE name=%s LIMIT 1"
    cursor.execute(sql, (new_name,))
    result = cursor.fetchone()
    if result is not None:  # target value name already exists
        sql = "SELECT * FROM ingredients WHERE id=%s LIMIT 1"
        cursor.execute(sql, (ingredient_id,))
        row = cursor.fetchone()
        if row is not None:
            sql = "UPDATE recipe_ingredients SET ingredient_id=%s WHERE ingredient_id=%s"
            cursor.execute(sql, (result['id'], row['id']))
            conn.commit()
            sql = "DELETE FROM ingredients WHERE id=%s"
            cursor.execute(sql, (row['id'],))
            conn.commit()
    else:
        sql = "UPDATE ingredients SET name=%s WHERE id=%s"
        cursor.execute(sql, (new_name, ingredient_id))
        conn.commit()


# cleansing from csv file
with open('ingredient_data.csv', newline='') as f:
    reader = csv.reader(f)
    for item in reader:
        update_ingredient(item[0], item[1])


# general cleansing operations
cursor.execute("SELECT * FROM ingredients WHERE name <> ''")
ingredients = cursor.fetchall()
for ingredient_row in ingredients:
    name = ingredient_row['name']
    cleansed = name

    # parts
    cleansed = cleansed.replace('zum Garnieren', '')
    cleansed = cleansed.replace('zum Einstreichen', '')
    cleansed = cleansed.replace('für die Arbeitsfläche', '')
    cleansed = cleansed.replace('zum Bestreuen', '')
    cleansed = cleansed.replace('in Stückchen', '')
    cleansed = cleansed.replace('nach Wahl', '')
    cleansed = cleansed.replace('aus dem Glas', '')
    cleansed = cleansed.replace('nach Belieben', '')
    cleansed = cleansed.replace('zum Braten', '')
    cleansed = cleansed.replace('für die Pfanne', '')
    cleansed = cleansed.replace('in Scheiben', '')
    cleansed = cleansed.replace('ohne Knochen', '')
    cleansed = cleansed.replace('mit Knochen', '')
    cleansed = cleansed.replace('zum Garnieren', '')
    cleansed = cleansed.replace('am Stück', '')
    cleansed = cleansed.replace('im Stück', '')
    cleansed = cleansed.replace('mit Haut', '')
    cleansed = cleansed.replace('ohne Haut', '')
    cleansed = cleansed.replace('mit Schale', '')
    cleansed = cleansed.replace('aus der Mühle', '')
    cleansed = cleansed.replace('für das Blech', '')
    cleansed = cleansed.replace('nach Bedarf', '')
    cleansed = cleansed.replace('bei Bedarf', '')
    cleansed = cleansed.replace('zum Anbraten', '')
    cleansed = cleansed.replace('zum Binden', '')
    cleansed = cleansed.replace('zum Andicken', '')
    cleansed = cleansed.replace('zum Servieren', '')
    cleansed = cleansed.replace('zum Verzieren', '')
    cleansed = cleansed.replace('aus dem Kühlregal', '')
    cleansed = cleansed.replace('zum Bestreichen', '')
    # cleansed = cleansed.replace('Type 405', '')
    # cleansed = cleansed.replace('Typ 405', '')
    # cleansed = cleansed.replace('405', '')
    # cleansed = cleansed.replace('550', '')
    cleansed = cleansed.replace('vom Vortag', '')
    cleansed = cleansed.replace('zum Kochen', '')
    cleansed = cleansed.replace('für die Form', '')
    cleansed = cleansed.replace('aus der Dose', '')
    cleansed = cleansed.replace('für die Mehlschwitze', '')
    cleansed = cleansed.replace('ohne Stein', '')
    cleansed = cleansed.replace('o.ä.', '')
    cleansed = cleansed.replace('n.B.', '')
    cleansed = cleansed.replace('nach Geschmack', '')
    cleansed = cleansed.replace('und/oder', 'oder')
    cleansed = cleansed.replace('TK', '')
    cleansed = cleansed.replace('in Würfeln', '')
    cleansed = cleansed.replace('mit Grün', '')
    # cleansed = cleansed.replace('Maggi', '')
    # cleansed = cleansed.replace('Dr. Oetker', '')
    cleansed = cleansed.replace('in Stücken', '')
    cleansed = cleansed.replace('zum Anrichten', '')
    cleansed = cleansed.replace('zum Weichkochen', '')
    cleansed = cleansed.replace('zum Abschmecken', '')
    cleansed = cleansed.replace(' - ', '-')
    cleansed = cleansed.replace('- ', '-')
    cleansed = cleansed.replace(' -', '-')
    cleansed = cleansed.replace('+', ' und ')
    cleansed = cleansed.replace('/', ' oder ')
    cleansed = cleansed.replace('in dünnen Scheiben', '')
    cleansed = cleansed.replace('zum Grillen', '')
    cleansed = cleansed.replace('zum Marinieren', '')
    cleansed = cleansed.replace('püriert', '')
    cleansed = cleansed.replace('im Mixer', '')
    cleansed = cleansed.replace('abgetropfte', '')
    cleansed = cleansed.replace('abgetropft', '')
    cleansed = cleansed.replace('abgewaschen', '')
    cleansed = re.sub(r'\d+\s?(g|kg|ml|mm|l|L|cm|EL)', '', cleansed)
    cleansed = re.sub(r'\boptional\b.*', '', cleansed)
    cleansed = re.sub(r'\bAbtropfgewicht\b.*', '', cleansed)
    cleansed = re.sub(r'\bgestiftelt\b.*', '', cleansed)
    cleansed = re.sub(r'\bgestiftelte\b.*', '', cleansed)
    cleansed = re.sub(r'\breif\b.*', '', cleansed)
    cleansed = re.sub(r'\bmittelreif\b.*', '', cleansed)
    cleansed = re.sub(r'\bgekocht\b.*', '', cleansed)
    cleansed = re.sub(r'\bgekochte\b.*', '', cleansed)
    cleansed = re.sub(r'\bschmal\b.*', '', cleansed)
    cleansed = re.sub(r'\bschmale\b.*', '', cleansed)
    cleansed = re.sub(r'\bfrisch\b.*', '', cleansed)
    cleansed = re.sub(r'\bfrische\b.*', '', cleansed)
    cleansed = re.sub(r'\bfein\b.*', '', cleansed)
    cleansed = re.sub(r'\bfeine\b.*', '', cleansed)
    cleansed = re.sub(r'\beinige\b.*', '', cleansed)
    cleansed = re.sub(r'\bgehackt\b.*', '', cleansed)
    cleansed = re.sub(r'\bgehackte\b.*', '', cleansed)
    cleansed = re.sub(r'\bgehacktes\b.*', '', cleansed)
    cleansed = re.sub(r'\bgehackter\b.*', '', cleansed)
    cleansed = re.sub(r'\bkleingeschnitten\b.*', '', cleansed)
    cleansed = re.sub(r'\baufgetaut\b.*', '', cleansed)
    cleansed = re.sub(r'\baufgetaute\b.*', '', cleansed)
    cleansed = re.sub(r'\bá\b.*', '', cleansed)
    cleansed = re.sub(r'\bà\b.*', '', cleansed)
    cleansed = re.sub(r'\bje\b.*', '', cleansed)
    cleansed = re.sub(r'\bersatzweise\b.*', '', cleansed)
    cleansed = re.sub(r'\bz\?\.?B\.?\b.*', '', cleansed)

    # characters and whitespaces
    cleansed = cleansed.replace('"', '')
    cleansed = cleansed.replace('.', ' ')
    cleansed = cleansed.replace(',', ' ')
    cleansed = cleansed.replace(':', '')
    cleansed = cleansed.replace(';', '')
    # cleansed = re.sub(r'[„“,*]]', '', cleansed)
    # cleansed = re.sub(r'[`´]]', '\'', cleansed)
    # cleansed = re.sub(r'[àáâ]', 'a', cleansed)
    # cleansed = re.sub(r'[èéê]', 'e', cleansed)
    # cleansed = re.sub(r'[ìíî]', 'i', cleansed)
    # cleansed = re.sub(r'[òóô]', 'o', cleansed)
    # cleansed = re.sub(r'[ùúû]', 'u', cleansed)
    cleansed = re.sub(r'\s\s+', ' ', cleansed)
    cleansed = cleansed.strip()

    if name != cleansed:  # update only if there are changes
        update_ingredient(name, cleansed)


with open('ingredient_data_manual_2.csv', newline='') as f:
    reader = csv.reader(f)
    for item in reader:
        update_ingredient(item[0], item[1])

# remove ingredient with blank name
# cursor.execute("SELECT * FROM ingredients WHERE name='' AND name_en=''")
# result = cursor.fetchone()
# if result is not None:
#     sql = "DELETE FROM recipe_ingredients WHERE ingredient_id=%s"
#     cursor.execute(sql, (result['id'],))
#     conn.commit()
#     sql = "DELETE FROM ingredients WHERE id=%s"
#     cursor.execute(sql, (result['id'],))
#     conn.commit()


conn.close()
