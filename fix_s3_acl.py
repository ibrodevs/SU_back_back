import os
import django
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.conf import settings
import boto3

print("=" * 60)
print("ОБНОВЛЕНИЕ ACL ДЛЯ СТАТИЧЕСКИХ ФАЙЛОВ")
print("=" * 60)

# Создаем S3 клиент
s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

bucket_name = settings.AWS_STORAGE_BUCKET_NAME
prefix = 'static/'

print(f"\nБакет: {bucket_name}")
print(f"Обновляем ACL для файлов с префиксом: {prefix}")

try:
    # Получаем список всех объектов
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    
    count = 0
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                try:
                    # Обновляем ACL для каждого файла
                    s3.put_object_acl(
                        Bucket=bucket_name,
                        Key=key,
                        ACL='public-read'
                    )
                    count += 1
                    if count % 50 == 0:
                        print(f"   Обработано {count} файлов...")
                except Exception as e:
                    print(f"   ❌ Ошибка для {key}: {e}")
    
    print(f"\n✅ Успешно обновлено ACL для {count} файлов!")
    print("\nТеперь статические файлы должны быть доступны публично.")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
