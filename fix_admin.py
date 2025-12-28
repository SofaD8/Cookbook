import os
import django

from django.contrib.auth.models import User


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cookbook_project.settings.prod')
django.setup()


username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'Sofa')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"PASSWORD UPDATED FOR {username}")
else:
    User.objects.create_superuser(username=username, password=password, email="admin@example.com")
    print(f"SUPERUSER {username} CREATED FROM SCRATCH")
