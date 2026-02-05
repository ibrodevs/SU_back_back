"""
Скрипт для создания суперпользователя на Heroku
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Данные суперпользователя из переменных окружения
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@su-medical.edu.kg')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Проверяем, существует ли пользователь
if User.objects.filter(username=username).exists():
    print(f"✅ Пользователь '{username}' уже существует")
    user = User.objects.get(username=username)
    print(f"   Email: {user.email}")
    print(f"   Is superuser: {user.is_superuser}")
    print(f"   Is staff: {user.is_staff}")
else:
    # Создаем суперпользователя
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Суперпользователь создан успешно!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\n⚠️  ВАЖНО: Смените пароль после первого входа!")
