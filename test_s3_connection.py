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
print("ПРОВЕРКА AWS S3 ПОДКЛЮЧЕНИЯ")
print("=" * 60)

from django.conf import settings

print(f"\nБакет: {settings.AWS_STORAGE_BUCKET_NAME}")
print(f"Регион: {settings.AWS_S3_REGION_NAME}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"Storage backend: {default_storage.__class__.__name__}")

# Тест загрузки
print("\nТестирование загрузки...")
try:
    test_path = default_storage.save("test/connection_test.txt", ContentFile(b"Test successful!"))
    print(f"✅ Файл загружен: {test_path}")
    
    url = default_storage.url(test_path)
    print(f"✅ URL: {url}")
    
    if "X-Amz" in url:
        print("⚠️  URL содержит подпись (это Bucketeer)")
    else:
        print("✅ URL публичный (собственный S3 бакет)")
    
    default_storage.delete(test_path)
    print("✅ Файл удален")
    
    print("\n" + "=" * 60)
    print("✅ S3 РАБОТАЕТ КОРРЕКТНО!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
