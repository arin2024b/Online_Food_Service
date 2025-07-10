import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
tables = [
    'orders_order',
    'orders_orderitem',
    'orders_promocode',
    'orders_review',
    'orders_delivery',
    'orders_orderitem_add_ons',
]
for table in tables:
    c.execute(f"DROP TABLE IF EXISTS {table}")
conn.commit()
conn.close()
print('All orders_* tables dropped.') 