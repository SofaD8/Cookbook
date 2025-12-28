import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cookbook_project.settings.prod')


django.setup()


from django.contrib.auth.models import User

def fix_admin():
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'Sofa')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

    if not password:
        print("ERROR: DJANGO_SUPERUSER_PASSWORD is not set in Render Environment")
        return

    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"PASSWORD UPDATED FOR {username}")
    else:
        User.objects.create_superuser(username=username, password=password, email=email)
        print(f"SUPERUSER {username} CREATED FROM SCRATCH")

if __name__ == "__main__":
    fix_admin()
