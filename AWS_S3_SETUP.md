# Создание собственного AWS S3 бакета для медиа файлов

## Шаг 1: Создание AWS аккаунта и IAM пользователя

### 1.1 Регистрация в AWS (если нет аккаунта)
1. Перейди на https://aws.amazon.com/
2. Нажми "Create an AWS Account"
3. Заполни данные (нужна кредитная карта для верификации)
4. Выбери Free Tier план

### 1.2 Создание IAM пользователя с доступом к S3
1. Войди в AWS Console: https://console.aws.amazon.com/
2. Найди сервис **IAM** (через поиск сверху)
3. Слева выбери **Users** → **Create user**
4. Введи имя пользователя: `django-s3-user`
5. Нажми **Next**
6. Выбери **Attach policies directly**
7. Найди и выбери политику: **AmazonS3FullAccess**
8. Нажми **Next** → **Create user**

### 1.3 Получение ключей доступа
1. Нажми на созданного пользователя `django-s3-user`
2. Перейди на вкладку **Security credentials**
3. Нажми **Create access key**
4. Выбери **Application running outside AWS**
5. Нажми **Next** → **Create access key**
6. **ВАЖНО:** Скопируй и сохрани:
   - `Access key ID` (например: AKIAIOSFODNN7EXAMPLE)
   - `Secret access key` (например: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY)

---

## Шаг 2: Создание S3 бакета

### 2.1 Создание бакета
1. Найди сервис **S3** через поиск
2. Нажми **Create bucket**
3. Заполни данные:
   - **Bucket name**: `su-medical-school-media` (или любое уникальное имя)
   - **AWS Region**: выбери `US East (N. Virginia) us-east-1`
4. В разделе **Block Public Access settings**:
   - **Сними галочку** "Block all public access"
   - Поставь галочку подтверждения
5. Оставь остальные настройки по умолчанию
6. Нажми **Create bucket**

### 2.2 Настройка публичного доступа
1. Открой созданный бакет
2. Перейди на вкладку **Permissions**
3. Найди раздел **Bucket policy** → нажми **Edit**
4. Вставь эту политику (замени `YOUR-BUCKET-NAME` на имя твоего бакета):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

5. Нажми **Save changes**

### 2.3 Настройка CORS
1. В том же разделе **Permissions**
2. Найди **Cross-origin resource sharing (CORS)** → нажми **Edit**
3. Вставь:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag"]
    }
]
```

4. Нажми **Save changes**

---

## Шаг 3: Настройка Heroku

Добавь переменные окружения на Heroku:

```bash
heroku config:set AWS_ACCESS_KEY_ID="твой-access-key-id" --app med-backend
heroku config:set AWS_SECRET_ACCESS_KEY="твой-secret-access-key" --app med-backend
heroku config:set AWS_STORAGE_BUCKET_NAME="su-medical-school-media" --app med-backend
heroku config:set AWS_S3_REGION_NAME="us-east-1" --app med-backend
```

---

## Готово! 🎉

Теперь все медиа файлы будут публично доступны по адресу:
```
https://su-medical-school-media.s3.us-east-1.amazonaws.com/media/banners/image.jpg
```

Никаких подписанных URL, работает навсегда!
