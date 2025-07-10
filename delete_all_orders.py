import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lazizkhana.settings')
django.setup()

from orders.models import Order, OrderItem

OrderItem.objects.all().delete()
Order.objects.all().delete()
print('All orders and order items deleted.') 