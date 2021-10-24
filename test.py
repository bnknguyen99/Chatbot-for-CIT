import sqlite3
conn = sqlite3.connect('chatbotdb')
cursor = conn.cursor()
ent = []
h = 0
a = []
with open ('qc.txt', 'r') as file:
    for i in file:
    	a.append(i[:-1])

print(a)
print(len(a))
for i in a:
    sqlite_select_Query = 'SELECT * from quyChe where lower(entity) = ' + '"'+i+'"'
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    ent.append(record)
for i in ent:
    print(i)
