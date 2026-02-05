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
print("НАСТРОЙКА ПУБЛИЧНОГО ДОСТУПА К S3 BUCKETEER")
print("=" * 60)

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

bucket_name = settings.AWS_STORAGE_BUCKET_NAME

print(f"\nБакет: {bucket_name}")

# Пытаемся получить текущую bucket policy
print("\n1. Проверка текущей bucket policy...")
try:
    policy = s3_client.get_bucket_policy(Bucket=bucket_name)
    print(f"   Текущая policy: {policy.get('Policy', 'Нет')}")
except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
        print("   ❌ Bucket policy не настроена")
    else:
        print(f"   ❌ Ошибка: {e}")

# Пытаемся установить публичную bucket policy
print("\n2. Попытка установить публичную bucket policy...")
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/media/*"
        }
    ]
}

try:
    s3_client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(bucket_policy)
    )
    print("   ✅ Bucket policy успешно установлена!")
    print("   Медиа файлы теперь доступны публично")
except ClientError as e:
    print(f"   ❌ Ошибка при установке bucket policy: {e}")
    print(f"   Код ошибки: {e.response['Error']['Code']}")
    print(f"   Сообщение: {e.response['Error']['Message']}")

# Проверяем Block Public Access настройки
print("\n3. Проверка Block Public Access...")
try:
    block_config = s3_client.get_public_access_block(Bucket=bucket_name)
    config = block_config['PublicAccessBlockConfiguration']
    print(f"   BlockPublicAcls: {config.get('BlockPublicAcls', 'N/A')}")
    print(f"   IgnorePublicAcls: {config.get('IgnorePublicAcls', 'N/A')}")
    print(f"   BlockPublicPolicy: {config.get('BlockPublicPolicy', 'N/A')}")
    print(f"   RestrictPublicBuckets: {config.get('RestrictPublicBuckets', 'N/A')}")
except ClientError as e:
    print(f"   ❌ Ошибка: {e}")

print("\n" + "=" * 60)
