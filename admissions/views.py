from django.conf import settings
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime
import os


ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
MAX_FILE_MB = 5
MAX_TOTAL_MB = 25


def _validate_file(name, f):
    if not f:
        return None
    ext = os.path.splitext(f.name)[1].lower().lstrip('.')
    if ext not in ALLOWED_EXTENSIONS:
        return f"Файл {name}: недопустимый формат (разрешены: {', '.join(sorted(ALLOWED_EXTENSIONS))})"
    size_mb = f.size / (1024 * 1024)
    if size_mb > MAX_FILE_MB:
        return f"Файл {name}: слишком большой ({size_mb:.1f} MB), максимум {MAX_FILE_MB} MB"
    return None


def _validate_total_size(files):
    total_mb = sum((f.size for f in files if f), 0) / (1024 * 1024)
    if total_mb > MAX_TOTAL_MB:
        return f"Общий размер вложений {total_mb:.1f} MB превышает максимум {MAX_TOTAL_MB} MB"
    return None


@csrf_exempt
@require_http_methods(["POST"]) 
def submit_application_email(request):
    """
    Accepts multipart/form-data with fields and files, composes an email and attaches uploaded documents.
    Expected fields (strings): firstName, lastName, middleName, birthDate, gender, phone, email, address,
    program, schoolName, graduationYear, certificateNumber, ortScore, subjects (JSON string optional).
    Files (optional): certificate, passport, medical, photos (multiple), ortCertificate.
    """
    try:
        # Build email subject and body
        first_name = request.POST.get('firstName', '')
        last_name = request.POST.get('lastName', '')
        program = request.POST.get('program', '')
        subject = f"Заявка на поступление | {last_name} {first_name} | {program}".strip(' |')

        def g(name, default=''):
            return request.POST.get(name, default)

        # Prefer full body from client if provided
        body = g('body')
        if not body:
            # Fallback: construct a readable body
            body = f"""
ЗАЯВКА НА ПОСТУПЛЕНИЕ
Салымбеков Университет

=== ЛИЧНЫЕ ДАННЫЕ ===
ФИО: {g('lastName')} {g('firstName')} {g('middleName')}
Дата рождения: {g('birthDate')}
Пол: {g('gender')}
Телефон: {g('phone')}
Email: {g('email')}
Адрес: {g('address')}

=== ПРОГРАММА ОБУЧЕНИЯ ===
Выбранная программа: {g('program')}

=== ОБРАЗОВАНИЕ ===
Название школы: {g('schoolName')}
Год окончания: {g('graduationYear')}
Номер аттестата: {g('certificateNumber')}
Балл ОРТ: {g('ortScore')}

=== ДОКУМЕНТЫ ===
См. вложения к письму (если приложены)

=== СОГЛАСИЯ ===
Согласие с условиями: {g('agreeTerms')}
Согласие на обработку данных: {g('agreePrivacy')}

Дата подачи заявки: {g('submittedAt')}
""".strip()

        # Files and validation
        single_fields = ['certificate', 'passport', 'medical', 'ortCertificate']
        files_to_check = [request.FILES.get(fname) for fname in single_fields]
        photos = request.FILES.getlist('photos')
        files_to_check.extend(photos)

        errors = []
        for fname in single_fields:
            err = _validate_file(fname, request.FILES.get(fname))
            if err:
                errors.append(err)
        for idx, pf in enumerate(photos, start=1):
            err = _validate_file(f'photos[{idx}]', pf)
            if err:
                errors.append(err)
        total_err = _validate_total_size([f for f in files_to_check if f])
        if total_err:
            errors.append(total_err)
        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        # Target recipients from env or default (support multiple addresses)
        recipient_setting = getattr(settings, 'ADMISSIONS_EMAIL_TO', None) or 'adilhansatymkulov40@gmail.com'
        recipients = [email.strip() for email in recipient_setting.split(',')]

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None) or recipients[0],
            to=recipients,
            reply_to=[g('email')] if g('email') else None,
        )

        # Получаем описания документов от фронтенда
        document_descriptions = {}
        try:
            import json
            descriptions_json = request.POST.get('document_descriptions', '{}')
            document_descriptions = json.loads(descriptions_json)
        except (ValueError, TypeError):
            # Если не удалось распарсить, используем значения по умолчанию
            document_descriptions = {
                'certificate': 'Аттестат об окончании школы (High school diploma)',
                'passport': 'Копия паспорта (Passport ID copies)', 
                'medical': 'Медицинское заключение (Medical certificate 086u)',
                'photos': 'Фотографии 3x4 см (3x4 cm photos)',
                'ortCertificate': 'ОРТ сертификат (ORT certificate)'
            }

        # Attach single-file fields if present
        for fname in ['certificate', 'passport', 'medical', 'ortCertificate']:
            f = request.FILES.get(fname)
            if f:
                description = document_descriptions.get(fname, fname)
                # Создаем новое имя файла с описанием
                original_name = f.name
                name_parts = original_name.rsplit('.', 1)
                if len(name_parts) == 2:
                    new_filename = f"{description} - {name_parts[0]}.{name_parts[1]}"
                else:
                    new_filename = f"{description} - {original_name}"
                
                email.attach(filename=new_filename, content=f.read(), mimetype=f.content_type)

        # Attach multiple photos
        photo_description = document_descriptions.get('photos', 'Фотографии')
        for idx, f in enumerate(request.FILES.getlist('photos'), 1):
            if f:
                original_name = f.name
                name_parts = original_name.rsplit('.', 1)
                if len(request.FILES.getlist('photos')) > 1:
                    photo_desc = f"{photo_description} ({idx})"
                else:
                    photo_desc = photo_description
                
                if len(name_parts) == 2:
                    new_filename = f"{photo_desc} - {name_parts[0]}.{name_parts[1]}"
                else:
                    new_filename = f"{photo_desc} - {original_name}"
                
                email.attach(filename=new_filename, content=f.read(), mimetype=f.content_type)

        # Send email to admissions
        email.send(fail_silently=False)

        # Не отправляем подтверждающее письмо заявителю, чтобы избежать ошибок доставки
        # При необходимости можно включить позже с проверкой валидности email

        ticket = datetime.now().strftime('%Y%m%d%H%M%S')
        return JsonResponse({'status': 'ok', 'ticket': ticket})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import OfficialContent
from .serializers import OfficialContentSerializer

@api_view(['GET'])
def official_content_list(request):
    """
    Returns all official site content keys/values, structured by key.
    E.g. { 'footer': { 'ru': {...}, 'en': {...} }, ... }
    """
    try:
        contents = OfficialContent.objects.all()
        # Build structured dict
        structured_data = {}
        for content in contents:
            structured_data[content.key] = content.content
            
        return Response({
            'success': True,
            'data': structured_data
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)

