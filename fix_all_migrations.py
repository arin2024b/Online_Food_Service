import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("DELETE FROM django_migrations")
conn.commit()
conn.close()
print('All migration records removed from django_migrations table.') 