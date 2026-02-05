"""
Скрипт для проверки переменных окружения на Heroku
"""
import os
import sys

required_vars = [
    'SECRET_KEY',
    'DATABASE_URL',
]

optional_vars = [
    'DEBUG',
    'ALLOWED_HOSTS',
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_STORAGE_BUCKET_NAME',
    'AWS_S3_REGION_NAME',
]

print("=== Проверка переменных окружения ===\n")

missing_required = []
for var in required_vars:
    value = os.environ.get(var)
    if value:
        # Маскируем значение для безопасности
        masked = value[:5] + '...' if len(value) > 5 else '***'
        print(f"✅ {var}: {masked}")
    else:
        print(f"❌ {var}: НЕ УСТАНОВЛЕНА")
        missing_required.append(var)

print("\n=== Опциональные переменные ===\n")
for var in optional_vars:
    value = os.environ.get(var)
    if value:
        masked = value[:5] + '...' if len(value) > 5 else '***'
        print(f"✅ {var}: {masked}")
    else:
        print(f"⚠️  {var}: не установлена (используется значение по умолчанию)")

if missing_required:
    print(f"\n❌ ОШИБКА: Не установлены обязательные переменные: {', '.join(missing_required)}")
    sys.exit(1)
else:
    print("\n✅ Все обязательные переменные установлены!")
    sys.exit(0)
