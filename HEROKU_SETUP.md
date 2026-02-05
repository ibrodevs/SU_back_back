# Настройка Heroku для медицинского университета

## Необходимые переменные окружения на Heroku

### Обязательные переменные:

```bash
# Генерация SECRET_KEY (выполните локально и скопируйте результат)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Установка переменных на Heroku
heroku config:set SECRET_KEY="your-generated-secret-key" --app med-backend-d61c905599c2
heroku config:set DEBUG=False --app med-backend-d61c905599c2
heroku config:set ALLOWED_HOSTS="med-backend-d61c905599c2.herokuapp.com,www.su-medical-school.com" --app med-backend-d61c905599c2
```

### База данных (автоматически создается при добавлении Heroku Postgres):

```bash
heroku addons:create heroku-postgresql:essential-0 --app med-backend-d61c905599c2
# DATABASE_URL устанавливается автоматически
```

### AWS S3 (опционально, для хранения медиа и статики):

```bash
heroku config:set AWS_ACCESS_KEY_ID="your-aws-access-key" --app med-backend-d61c905599c2
heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-key" --app med-backend-d61c905599c2
heroku config:set AWS_STORAGE_BUCKET_NAME="your-bucket-name" --app med-backend-d61c905599c2
heroku config:set AWS_S3_REGION_NAME="us-east-1" --app med-backend-d61c905599c2
```

### Email настройки (опционально):

```bash
heroku config:set EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend" --app med-backend-d61c905599c2
heroku config:set EMAIL_HOST="smtp.gmail.com" --app med-backend-d61c905599c2
heroku config:set EMAIL_PORT=587 --app med-backend-d61c905599c2
heroku config:set EMAIL_USE_TLS=True --app med-backend-d61c905599c2
heroku config:set EMAIL_HOST_USER="your-email@gmail.com" --app med-backend-d61c905599c2
heroku config:set EMAIL_HOST_PASSWORD="your-app-password" --app med-backend-d61c905599c2
```

## Проверка текущих переменных:

```bash
heroku config --app med-backend-d61c905599c2
```

## Деплой на Heroku:

```bash
# Добавить remote (если еще не добавлен)
heroku git:remote -a med-backend-d61c905599c2

# Проверить текущую ветку
git branch

# Деплой
git push heroku master

# Или если вы на другой ветке (например, iliyar):
git push heroku iliyar:master
```

## Миграции и collectstatic:

```bash
# Выполнить миграции
heroku run python manage.py migrate --app med-backend-d61c905599c2

# Собрать статику (если не используете S3)
heroku run python manage.py collectstatic --noinput --app med-backend-d61c905599c2

# Создать суперпользователя
heroku run python manage.py createsuperuser --app med-backend-d61c905599c2
```

## Просмотр логов:

```bash
# Последние логи
heroku logs --tail --app med-backend-d61c905599c2

# Логи с ошибками
heroku logs --tail --app med-backend-d61c905599c2 | grep -i error

# Последние 500 строк
heroku logs -n 500 --app med-backend-d61c905599c2
```

## Решение частых проблем:

### Ошибка 500 при входе в админку:

1. Проверьте, что SECRET_KEY установлен
2. Проверьте, что DATABASE_URL установлен (должен быть автоматически)
3. Проверьте, что миграции выполнены
4. Проверьте логи: `heroku logs --tail --app med-backend-d61c905599c2`

### База данных не работает:

```bash
# Проверить, что postgres addon установлен
heroku addons --app med-backend-d61c905599c2

# Если нет, добавить:
heroku addons:create heroku-postgresql:essential-0 --app med-backend-d61c905599c2
```

### Проблемы с SSL при подключении к БД:

Уже исправлено в settings.py: `ssl_require=False`

## Проверка работоспособности:

```bash
# Проверить переменные окружения
heroku run python check_heroku_env.py --app med-backend-d61c905599c2

# Открыть сайт
heroku open --app med-backend-d61c905599c2

# Открыть админку
heroku open /admin/ --app med-backend-d61c905599c2
```
