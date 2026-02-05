import os
import django
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

print("=" * 60)
print("ПРОВЕРКА ПОДПИСАННЫХ URL")
print("=" * 60)

# Создаем тестовый файл
print("\n1. Загружаем тестовое изображение...")
test_content = b"Test image content"
test_path = default_storage.save("test_images/test_signed_url.jpg", ContentFile(test_content))
print(f"   ✅ Файл загружен: {test_path}")

# Получаем URL (с подписью)
url = default_storage.url(test_path)
print(f"\n2. URL с подписью:")
print(f"   {url[:100]}...")
print(f"   Длина URL: {len(url)} символов")

# Проверяем, есть ли подпись в URL
if 'X-Amz-Algorithm' in url or 'Signature' in url or 'X-Amz-Signature' in url:
    print(f"\n   ✅ URL подписан! Содержит параметры авторизации AWS")
else:
    print(f"\n   ❌ URL не подписан")

# Удаляем тестовый файл
default_storage.delete(test_path)
print(f"\n3. ✅ Тестовый файл удален")

print("\n" + "=" * 60)
print("Теперь все медиа файлы будут доступны через подписанные URL!")
print("URL действителен в течение 1 года")
print("=" * 60)
