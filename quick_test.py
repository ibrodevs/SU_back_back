from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

print("Bucketeer переменные:")
print("KEY_ID:", os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID', 'НЕТ'))
print("BUCKET:", os.environ.get('BUCKETEER_BUCKET_NAME', 'НЕТ'))
print("REGION:", os.environ.get('BUCKETEER_AWS_REGION', 'НЕТ'))
print("\nDjango настройки:")
print("AWS_KEY:", getattr(settings, 'AWS_ACCESS_KEY_ID', 'НЕТ'))
print("BUCKET:", getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'НЕТ'))
print("MEDIA_URL:", settings.MEDIA_URL)
print("Storage:", default_storage.__class__.__name__)

# Тест
try:
    path = default_storage.save('test.txt', ContentFile(b'test'))
    print(f"\n✅ Загрузка работает! Файл: {path}")
    print(f"URL: {default_storage.url(path)}")
    default_storage.delete(path)
    print("✅ Удаление работает!")
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
