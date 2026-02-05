import os
import django
from pathlib import Path
import sys
import json

sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.conf import settings
import boto3
from botocore.exceptions import ClientError

print("=" * 60)
print("НАСТРОЙКА ПУБЛИЧНОГО ДОСТУПА ЧЕРЕЗ PUBLIC/ ПАПКУ")
print("=" * 60)

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

bucket_name = settings.AWS_STORAGE_BUCKET_NAME

print(f"\nБакет: {bucket_name}")

# Шаг 1: Настройка Block Public Access
print("\n1. Настройка Block Public Access...")
try:
    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': False,  # Разрешаем публичные политики
            'RestrictPublicBuckets': False  # Разрешаем публичные бакеты
        }
    )
    print("   ✅ Block Public Access настроен")
except ClientError as e:
    print(f"   ❌ Ошибка: {e}")

# Шаг 2: Создание bucket policy для public/ папки
print("\n2. Создание bucket policy для папки public/...")
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/public/*"
        }
    ]
}

try:
    s3_client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(bucket_policy)
    )
    print("   ✅ Bucket policy установлена!")
    print(f"   Все файлы в папке public/ теперь публично доступны")
except ClientError as e:
    print(f"   ❌ Ошибка: {e}")

# Проверка
print("\n3. Проверка bucket policy...")
try:
    policy = s3_client.get_bucket_policy(Bucket=bucket_name)
    print("   ✅ Bucket policy активна:")
    print(f"   {json.dumps(json.loads(policy['Policy']), indent=2)}")
except ClientError as e:
    print(f"   ❌ Ошибка: {e}")

print("\n" + "=" * 60)
print("✅ ГОТОВО! Теперь все файлы в public/ будут публично доступны")
print("=" * 60)
