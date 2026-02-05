import os
import django
from pathlib import Path
import sys

# Настройка Django
sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

print("=" * 60)
print("ПРОВЕРКА BUCKETEER S3 STORAGE")
print("=" * 60)

# Проверяем переменные окружения
print("\n1. Проверка переменных окружения:")
bucketeer_vars = {
    'BUCKETEER_AWS_ACCESS_KEY_ID': os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID'),
    'BUCKETEER_AWS_REGION': os.environ.get('BUCKETEER_AWS_REGION'),
    'BUCKETEER_BUCKET_NAME': os.environ.get('BUCKETEER_BUCKET_NAME'),
    'BUCKETEER_AWS_SECRET_ACCESS_KEY': '***' if os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY') else None,
}

for key, value in bucketeer_vars.items():
    status = "✅" if value else "❌"
    print(f"   {status} {key}: {value}")

# Проверяем Django настройки
print("\n2. Проверка Django настроек:")
print(f"   AWS_ACCESS_KEY_ID: {getattr(settings, 'AWS_ACCESS_KEY_ID', 'не установлен')}")
print(f"   AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'не установлен')}")
print(f"   AWS_S3_REGION_NAME: {getattr(settings, 'AWS_S3_REGION_NAME', 'не установлен')}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   Storage backend: {default_storage.__class__.__name__}")

# Тестируем загрузку файла
print("\n3. Тестирование загрузки файла в S3:")
try:
    test_content = "Это тестовый файл для проверки Bucketeer S3"
    test_file_name = "test/bucketeer_test.txt"
    
    # Загружаем файл
    path = default_storage.save(test_file_name, ContentFile(test_content.encode()))
    print(f"   ✅ Файл успешно загружен: {path}")
    
    # Получаем URL
    url = default_storage.url(path)
    print(f"   📎 URL файла: {url}")
    
    # Проверяем существование
    exists = default_storage.exists(path)
    print(f"   ✅ Файл существует в S3: {exists}")
    
    # Читаем файл обратно
    file = default_storage.open(path)
    content = file.read().decode()
    file.close()
    print(f"   ✅ Содержимое прочитано: '{content}'")
    
    # Удаляем тестовый файл
    default_storage.delete(path)
    print(f"   ✅ Тестовый файл удален")
    
    print("\n" + "=" * 60)
    print("✅ BUCKETEER S3 РАБОТАЕТ КОРРЕКТНО!")
    print("=" * 60)
    
except Exception as e:
    print(f"   ❌ Ошибка при работе с S3: {str(e)}")
    print("\n" + "=" * 60)
    print("❌ ОШИБКА: BUCKETEER S3 НЕ РАБОТАЕТ!")
    print("=" * 60)
    import traceback
    traceback.print_exc()
