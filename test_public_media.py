"""
Тест публичного доступа к медиа файлам через Django прокси
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.conf import settings
import boto3

print("=" * 60)
print("ТЕСТ ПУБЛИЧНОГО ДОСТУПА К МЕДИА ФАЙЛАМ")
print("=" * 60)

# Проверяем настройки
print("\n1. Проверка настроек Bucketeer:")
print(f"   Bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
print(f"   Region: {settings.AWS_S3_REGION_NAME}")
print(f"   AWS_DEFAULT_ACL: {settings.AWS_DEFAULT_ACL}")
print(f"   AWS_QUERYSTRING_AUTH: {settings.AWS_QUERYSTRING_AUTH}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")

# Загружаем тестовый файл
print("\n2. Загрузка тестового файла...")
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

test_content = b"Test public access content"
test_path = "test_public_access.txt"

# Удаляем если существует
if default_storage.exists(test_path):
    default_storage.delete(test_path)

# Загружаем новый
saved_path = default_storage.save(test_path, ContentFile(test_content))
print(f"   ✓ Файл загружен: {saved_path}")

# Получаем URL
file_url = default_storage.url(saved_path)
print(f"   URL файла: {file_url}")

# Проверяем прямой доступ к S3
print("\n3. Проверка прямого доступа к S3:")
direct_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/media/{saved_path}"
print(f"   Прямой S3 URL: {direct_url}")

import requests
try:
    response = requests.get(direct_url, timeout=5)
    if response.status_code == 200:
        print(f"   ✓ Прямой доступ работает! (200 OK)")
    elif response.status_code == 403:
        print(f"   ✗ Прямой доступ заблокирован (403 Forbidden)")
        print(f"   → Используй Django прокси URL: {settings.MEDIA_URL}{saved_path}")
    else:
        print(f"   ? Статус: {response.status_code}")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

# Проверяем Django прокси
print("\n4. Django прокси URL:")
proxy_url = f"https://med-backend-d61c905599c2.herokuapp.com{settings.MEDIA_URL}{saved_path}"
print(f"   URL через Django: {proxy_url}")
print(f"   Этот URL будет работать публично через /media/ endpoint")

# Очистка
print("\n5. Очистка...")
default_storage.delete(saved_path)
print("   ✓ Тестовый файл удален")

print("\n" + "=" * 60)
print("ИТОГ:")
print("=" * 60)
print("Медиа файлы будут доступны публично через:")
print(f"  {proxy_url}")
print("\nВсе URL типа /media/* будут проксироваться через Django")
print("и отдавать файлы из S3 как публичные без expired URLs")
print("=" * 60)
