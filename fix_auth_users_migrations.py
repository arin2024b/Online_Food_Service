import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Remove problematic auth migrations
migrations_auth = [
    '0009_alter_user_last_name_max_length',
    '0010_alter_group_name_max_length',
    '0011_update_proxy_permissions',
    '0012_alter_user_first_name_max_length',
]
for mig in migrations_auth:
    c.execute("DELETE FROM django_migrations WHERE app='auth' AND name=?", (mig,))

# Remove all users migrations (if any)
c.execute("DELETE FROM django_migrations WHERE app='users'")
# Remove all orders migrations (if any)
c.execute("DELETE FROM django_migrations WHERE app='orders'")
# Remove admin initial migration (if any)
c.execute("DELETE FROM django_migrations WHERE app='admin' AND name='0001_initial'")

conn.commit()
conn.close()
print('Problematic auth, users, orders, and admin migrations removed.') 