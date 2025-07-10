import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS orders_order")
conn.commit()
conn.close()
print('orders_order table dropped.') 