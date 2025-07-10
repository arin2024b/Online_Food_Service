import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

migrations = [
    '0010_alter_group_name_max_length',
    '0011_update_proxy_permissions',
    '0012_alter_user_first_name_max_length',
]
for mig in migrations:
    c.execute("DELETE FROM django_migrations WHERE app='auth' AND name=?", (mig,))

conn.commit()
conn.close()
print('Problematic auth migrations removed.') 