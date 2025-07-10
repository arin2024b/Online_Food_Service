import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("PRAGMA table_info(orders_order)")
columns = c.fetchall()
print('orders_order columns:')
for col in columns:
    print(col)
conn.close() 