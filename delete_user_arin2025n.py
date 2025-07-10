import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lazizkhana.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'arin2025n'
try:
    user = User.objects.get(username=username)
    user.delete()
    print(f"User '{username}' deleted successfully.")
except User.DoesNotExist:
    print(f"User '{username}' does not exist.") 