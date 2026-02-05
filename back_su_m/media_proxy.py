"""
Прокси view для публичного доступа к медиа файлам из S3
"""
from django.http import HttpResponse, Http404
from django.conf import settings
import boto3
from botocore.exceptions import ClientError


def serve_media(request, path):
    """
    Проксирует медиа файлы из S3 и отдает их как публичные
    """
    if not hasattr(settings, 'AWS_ACCESS_KEY_ID') or not settings.AWS_ACCESS_KEY_ID:
        raise Http404("S3 не настроен")
    
    try:
        # Создаем S3 клиент
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        
        # Получаем файл из S3
        s3_key = f"media/{path}"
        response = s3_client.get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=s3_key
        )
        
        # Читаем содержимое файла
        file_content = response['Body'].read()
        content_type = response.get('ContentType', 'application/octet-stream')
        
        # Возвращаем файл с правильным content-type
        http_response = HttpResponse(file_content, content_type=content_type)
        
        # Добавляем заголовки для кэширования
        http_response['Cache-Control'] = 'public, max-age=86400'  # 1 день
        
        # Если это изображение, можно добавить заголовок для отображения в браузере
        if content_type.startswith('image/'):
            http_response['Content-Disposition'] = 'inline'
        
        return http_response
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchKey':
            raise Http404("Файл не найден")
        raise
