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


conn = MySQLdb.connect(db=DATABASE_NAME, user=DATABASE_USER, passwd=DATABASE_PASSWORD, host=DATABASE_HOST, charset='utf8', use_unicode=True)
if conn is None:
    sys.exit('Database connection could not be established!')
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

energy_scores = [[10, 3350], [9, 3015], [8, 2680], [7, 2345], [6, 2010], [5, 1675], [4, 1340], [3, 1005], [2, 670], [1, 335]]
sugar_scores = [[10, 45], [9, 40], [8, 36], [7, 31], [6, 27], [5, 22.5], [4, 18], [3, 13.5], [2, 9], [1, 4.5]]
saturated_fat_scores = [[10, 10], [9, 9], [8, 8], [7, 7], [6, 6], [5, 5], [4, 4], [3, 3], [2, 2], [1, 1]]
natrium_scores = [[10, 900], [9, 810], [8, 720], [7, 630], [6, 540], [5, 450], [4, 360], [3, 270], [2, 180], [1, 90]]
vegetables_scores = [[-5, 80], [-2, 60], [-1, 40]]
fibre_scores = [[-5, 4.7], [-4, 3.7], [-3, 2.8], [-2, 1.9], [-1, 0.9]]
protein_scores = [[-5, 8.0], [-4, 6.4], [-3, 4.8], [-2, 3.2], [-1, 1.6]]

cursor.execute("SELECT * FROM recipes WHERE source_id=2 LIMIT 10")
recipes = cursor.fetchall()
for r in recipes:
    a = get_score(energy_scores, r['energy'])
    b = get_score(sugar_scores, r['sugar'])
    c = get_score(saturated_fat_scores, r['saturated_fat'])
    d = get_score(natrium_scores, r['natrium'])
    e = get_score(vegetables_scores, r['vegetables_fruits'])
    f = get_score(fibre_scores, r['fibre'])
    g = get_score(protein_scores, r['protein'])

    score = a + b + c + d + e + f + g

    print('RECIPE: ', r['title'], ': ', score)
