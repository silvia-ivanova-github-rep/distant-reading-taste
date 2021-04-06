import MySQLdb
import sys

from credentials import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST


def get_score(score_list, value):
    if not value:
        return 0
    value = float(value)
    for x in score_list:
        if value > x[1]:
            return x[0]
    return 0


ENERGY_SCORES = [[10, 3350], [9, 3015], [8, 2680], [7, 2345], [6, 2010], [5, 1675], [4, 1340], [3, 1005], [2, 670], [1, 335]]
SUGAR_SCORES = [[10, 45], [9, 40], [8, 36], [7, 31], [6, 27], [5, 22.5], [4, 18], [3, 13.5], [2, 9], [1, 4.5]]
SATURATED_FAT_SCORE = [[10, 10], [9, 9], [8, 8], [7, 7], [6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1]]
SODIUM_SCORES = [[10, 900], [9, 810], [8, 720], [7, 630], [6, 540], [5, 450], [4, 360], [3, 270], [2, 180], [1, 90]]
VEGETABLES_SCORE = [[-5, 0.8], [-2, 0.6], [-1, 0.4]]
FIBRE_SCORES = [[-5, 4.7], [-4, 3.7], [-3, 2.8], [-2, 1.9], [-1, 0.9]]
PROTEIN_SCORES = [[-5, 8.0], [-4, 6.4], [-3, 4.8], [-2, 3.2], [-1, 1.6]]

conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

cursor.execute("SELECT * FROM recipes WHERE nutri_score IS NULL")
recipes = cursor.fetchall()
for r in recipes:
    a = get_score(ENERGY_SCORES, r['energy'])
    b = get_score(SUGAR_SCORES, r['sugar'])
    c = get_score(SATURATED_FAT_SCORE, r['saturated_fat'])
    d = get_score(SODIUM_SCORES, r['sodium'])
    e = get_score(VEGETABLES_SCORE, r['vegetables_fruits'])
    f = get_score(FIBRE_SCORES, r['fibre'])
    g = get_score(PROTEIN_SCORES, r['protein'])

    score = 0
    plus_points = a + b + c + d
    if plus_points >= 11 and e > -5:
        score = plus_points + e + f
    else:
        score = plus_points + e + f + g

    score_label = ''
    if score <= -1:
        score_label = 'A'
    elif score <= 2:
        score_label = 'B'
    elif score <= 10:
        score_label = 'C'
    elif score <= 18:
        score_label = 'D'
    else:
        score_label = 'E'

    print('RECIPE: ', r['title'], ': ', score, '-', score_label, ' (', a, ',', b, ',', c, ',', d, ',', e, ',', f, ',', g, ')')

    sql = "UPDATE recipes SET nutri_score=%s, nutri_score_label=%s WHERE id=%s"
    values = (score, score_label, r['id'])
    cursor.execute(sql, values)
    conn.commit()

conn.close()
