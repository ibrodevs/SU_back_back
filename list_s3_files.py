"""
Список всех файлов в Bucketeer S3
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.conf import settings
import boto3

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

print("=" * 60)
print("ФАЙЛЫ В BUCKETEER S3")
print("=" * 60)

paginator = s3_client.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='media/')

file_count = 0
for page in pages:
    if 'Contents' in page:
        for obj in page['Contents']:
            file_count += 1
            print(f"{file_count}. {obj['Key']} ({obj['Size']} bytes)")

print(f"\nВсего файлов: {file_count}")
print("=" * 60)

if file_count > 0:
    # Проверяем первый файл
    first_file = None
    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix='media/')
    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                first_file = obj['Key']
                break
            break
    
    if first_file:
        # Убираем media/ prefix для URL
        url_path = first_file.replace('media/', '', 1)
        proxy_url = f"https://med-backend-d61c905599c2.herokuapp.com/media/{url_path}"
        print(f"\nПример URL через прокси:")
        print(f"  {proxy_url}")
