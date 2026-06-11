from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class PartnerOrganization(models.Model):
    """Организации-партнеры для практики"""
    TYPE_CHOICES = [
        ('government', _('Государственная больница')),
        ('private', _('Частная клиника')),
        ('specialized', _('Специализированный центр')),
    ]
    
    # Мультиязычные поля
    name_ru = models.CharField('Название (русский)', max_length=255)
    name_kg = models.CharField('Название (кыргызский)', max_length=255)
    name_en = models.CharField('Название (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Немультиязычные поля
    type = models.CharField(_('Тип'), max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(_('Местоположение'), max_length=255)
    contact_person = models.CharField(_('Контактное лицо'), max_length=255)
    phone = models.CharField(_('Телефон'), max_length=50)
    email = models.EmailField(_('Email'))
    website = models.URLField(_('Веб-сайт'), blank=True, null=True)
    logo = models.ImageField(
        upload_to='partner_organizations/',
        verbose_name=_('Логотип'),
        blank=True,
        null=True,
        help_text='Логотип или фото организации-партнера'
    )
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Организация-партнер')
        verbose_name_plural = _('Организации-партнеры')
        ordering = ['name_ru']

    def __str__(self):
        return self.name_ru


class OrganizationSpecialization(models.Model):
    """Специализации организаций-партнеров"""
    organization = models.ForeignKey(
        PartnerOrganization, 
        on_delete=models.CASCADE,
        related_name='specializations'
    )
    # Мультиязычные поля
    name_ru = models.CharField('Название специализации (русский)', max_length=255)
    name_kg = models.CharField('Название специализации (кыргызский)', max_length=255)
    name_en = models.CharField('Название специализации (английский)', max_length=255)

    class Meta:
        verbose_name = _('Специализация')
        verbose_name_plural = _('Специализации')

    def __str__(self):
        return f"{self.organization.name_ru} - {self.name_ru}"


class InternshipRequirement(models.Model):
    """Требования к практике"""
    CATEGORY_CHOICES = [
        ('academic', _('Академические требования')),
        ('documents', _('Документы для практики')),
        ('duration', _('Продолжительность практики')),
    ]
    
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок (русский)', max_length=255)
    title_kg = models.CharField('Заголовок (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Немультиязычные поля
    category = models.CharField(_('Категория'), max_length=20, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активно'), default=True)

    class Meta:
        verbose_name = _('Требование к практике')
        verbose_name_plural = _('Требования к практике')
        ordering = ['category', 'order']

    def __str__(self):
        return self.title_ru


class InternshipRequirementItem(models.Model):
    """Элементы требований к практике"""
    requirement = models.ForeignKey(
        InternshipRequirement,
        on_delete=models.CASCADE,
        related_name='items'
    )
    # Мультиязычные поля
    text_ru = models.TextField('Текст (русский)')
    text_kg = models.TextField('Текст (кыргызский)')
    text_en = models.TextField('Текст (английский)')
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Элемент требования')
        verbose_name_plural = _('Элементы требований')
        ordering = ['order']

    def __str__(self):
        return f"{self.requirement.title_ru} - {self.text_ru[:50]}..."


class ReportTemplate(models.Model):
    """Шаблоны отчетов по практике"""
    # Мультиязычные поля
    name_ru = models.CharField('Название шаблона (русский)', max_length=255)
    name_kg = models.CharField('Название шаблона (кыргызский)', max_length=255)
    name_en = models.CharField('Название шаблона (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Файл шаблона
    file = models.FileField(
        upload_to='report_templates/',
        validators=[FileExtensionValidator(['doc', 'docx', 'pdf'])],
        verbose_name=_('Файл шаблона')
    )
    
    # Немультиязычные поля
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Шаблон отчета')
        verbose_name_plural = _('Шаблоны отчетов')
        ordering = ['name_ru']

    def __str__(self):
        return self.name_ru


# =============================================================================
# МОДЕЛИ ДЛЯ АКАДЕМИЧЕСКОЙ МОБИЛЬНОСТИ
# =============================================================================

class PartnerUniversity(models.Model):
    """Университеты-партнеры для академической мобильности"""
    # Мультиязычные поля
    name_ru = models.CharField('Название университета (русский)', max_length=255)
    name_kg = models.CharField('Название университета (кыргызский)', max_length=255)
    name_en = models.CharField('Название университета (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Немультиязычные поля
    country = models.CharField(_('Страна'), max_length=100)
    city = models.CharField(_('Город'), max_length=100)
    website = models.URLField(_('Веб-сайт'), blank=True)
    logo = models.ImageField(upload_to='universities/', blank=True, null=True, verbose_name=_('Логотип'))
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Университет-партнер')
        verbose_name_plural = _('Университеты-партнеры')
        ordering = ['name_ru']

    def __str__(self):
        return f"{self.name_ru} ({self.country})"


class UniversityProgram(models.Model):
    """Программы обмена в университетах-партнерах"""
    university = models.ForeignKey(
        PartnerUniversity,
        on_delete=models.CASCADE,
        related_name='programs'
    )
    
    # Мультиязычные поля
    name_ru = models.CharField('Название программы (русский)', max_length=255)
    name_kg = models.CharField('Название программы (кыргызский)', max_length=255)
    name_en = models.CharField('Название программы (английский)', max_length=255)
    
    description_ru = models.TextField('Описание программы (русский)', blank=True)
    description_kg = models.TextField('Описание программы (кыргызский)', blank=True)
    description_en = models.TextField('Описание программы (английский)', blank=True)
    
    # Немультиязычные поля
    duration = models.CharField(_('Продолжительность'), max_length=100)
    language = models.CharField(_('Язык обучения'), max_length=100)

    class Meta:
        verbose_name = _('Программа обмена')
        verbose_name_plural = _('Программы обмена')

    def __str__(self):
        return f"{self.university.name_ru} - {self.name_ru}"


class ExchangeOpportunity(models.Model):
    """Возможности обмена для студентов"""
    TYPE_CHOICES = [
        ('semester', _('Семестровый обмен')),
        ('year', _('Годовой обмен')),
    ]
    
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок (русский)', max_length=255)
    title_kg = models.CharField('Заголовок (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)')
    description_kg = models.TextField('Описание (кыргызский)')
    description_en = models.TextField('Описание (английский)')
    
    # Немультиязычные поля
    type = models.CharField(_('Тип обмена'), max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(_('Активна'), default=True)

    class Meta:
        verbose_name = _('Возможность обмена')
        verbose_name_plural = _('Возможности обмена')

    def __str__(self):
        return self.title_ru


class ExchangeBenefit(models.Model):
    """Преимущества программ обмена"""
    opportunity = models.ForeignKey(
        ExchangeOpportunity,
        on_delete=models.CASCADE,
        related_name='benefits'
    )
    
    # Мультиязычные поля
    text_ru = models.TextField('Текст преимущества (русский)')
    text_kg = models.TextField('Текст преимущества (кыргызский)')
    text_en = models.TextField('Текст преимущества (английский)')
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Преимущество')
        verbose_name_plural = _('Преимущества')
        ordering = ['order']

    def __str__(self):
        return f"{self.opportunity.title_ru} - {self.text_ru[:50]}..."


class MobilityRequirement(models.Model):
    """Требования для участия в академической мобильности"""
    CATEGORY_CHOICES = [
        ('academic', _('Академические требования')),
        ('language', _('Языковые требования')),
        ('documents', _('Документы')),
    ]
    
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок (русский)', max_length=255)
    title_kg = models.CharField('Заголовок (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Немультиязычные поля
    category = models.CharField(_('Категория'), max_length=20, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активно'), default=True)

    class Meta:
        verbose_name = _('Требование мобильности')
        verbose_name_plural = _('Требования мобильности')
        ordering = ['category', 'order']

    def __str__(self):
        return self.title_ru


# =============================================================================
# МОДЕЛИ ДЛЯ РЕГЛАМЕНТОВ И ПРАВИЛ
# =============================================================================

class InternalRule(models.Model):
    """Правила внутреннего распорядка"""
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок (русский)', max_length=255)
    title_kg = models.CharField('Заголовок (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Немультиязычные поля
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активно'), default=True)

    class Meta:
        verbose_name = _('Правило внутреннего распорядка')
        verbose_name_plural = _('Правила внутреннего распорядка')
        ordering = ['order']

    def __str__(self):
        return self.title_ru


class InternalRuleItem(models.Model):
    """Элементы правил внутреннего распорядка"""
    rule = models.ForeignKey(
        InternalRule,
        on_delete=models.CASCADE,
        related_name='items'
    )
    
    # Мультиязычные поля
    text_ru = models.TextField('Текст правила (русский)')
    text_kg = models.TextField('Текст правила (кыргызский)')
    text_en = models.TextField('Текст правила (английский)')
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Элемент правила')
        verbose_name_plural = _('Элементы правил')
        ordering = ['order']

    def __str__(self):
        return f"{self.rule.title_ru} - {self.text_ru[:50]}..."


class AcademicRegulation(models.Model):
    """Учебные регламенты"""
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок (русский)', max_length=255)
    title_kg = models.CharField('Заголовок (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Немультиязычные поля
    version = models.CharField(_('Версия'), max_length=50)
    effective_date = models.DateField(_('Дата вступления в силу'))
    is_active = models.BooleanField(_('Активен'), default=True)

    class Meta:
        verbose_name = _('Учебный регламент')
        verbose_name_plural = _('Учебные регламенты')
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.title_ru} v{self.version}"


class AcademicRegulationSection(models.Model):
    """Разделы учебных регламентов"""
    regulation = models.ForeignKey(
        AcademicRegulation,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок раздела (русский)', max_length=255)
    title_kg = models.CharField('Заголовок раздела (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок раздела (английский)', max_length=255)
    
    # Немультиязычные поля
    number = models.CharField(_('Номер раздела'), max_length=10)
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Раздел регламента')
        verbose_name_plural = _('Разделы регламентов')
        ordering = ['order']

    def __str__(self):
        return f"{self.regulation.title_ru} - {self.number}. {self.title_ru}"


class AcademicRegulationRule(models.Model):
    """Правила в разделах учебных регламентов"""
    section = models.ForeignKey(
        AcademicRegulationSection,
        on_delete=models.CASCADE,
        related_name='rules'
    )
    
    # Мультиязычные поля
    text_ru = models.TextField('Текст правила (русский)')
    text_kg = models.TextField('Текст правила (кыргызский)')
    text_en = models.TextField('Текст правила (английский)')
    
    # Немультиязычные поля
    number = models.CharField(_('Номер правила'), max_length=10)
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Правило регламента')
        verbose_name_plural = _('Правила регламентов')
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title_ru} - {self.number}"


class DownloadableDocument(models.Model):
    """Документы для скачивания"""
    # Мультиязычные поля
    title_ru = models.CharField('Название документа (русский)', max_length=255)
    title_kg = models.CharField('Название документа (кыргызский)', max_length=255)
    title_en = models.CharField('Название документа (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Файл документа
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        verbose_name=_('Файл документа')
    )
    
    # Немультиязычные поля
    file_size = models.PositiveIntegerField(_('Размер файла (байты)'), null=True, blank=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Документ для скачивания')
        verbose_name_plural = _('Документы для скачивания')
        ordering = ['title_ru']

    def __str__(self):
        return self.title_ru


# =============================================================================
# МОДЕЛИ ДЛЯ ИНСТРУКЦИЙ
# =============================================================================

class StudentGuide(models.Model):
    """Инструкции для студентов"""
    CATEGORY_CHOICES = [
        ('academic', _('Академические вопросы')),
        ('administrative', _('Административные вопросы')),
        ('documents', _('Документы и справки')),
        ('financial', _('Финансовые вопросы')),
        ('appeals', _('Заявления и обращения')),
    ]
    
    ICON_CHOICES = [
        ('CalendarDaysIcon', 'Календарь'),
        ('UserGroupIcon', 'Группа пользователей'),
        ('ClipboardDocumentListIcon', 'Список документов'),
        ('DocumentTextIcon', 'Документ'),
        ('AcademicCapIcon', 'Академическая шапочка'),
        ('BuildingOfficeIcon', 'Офисное здание'),
    ]
    
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок (русский)', max_length=255)
    title_kg = models.CharField('Заголовок (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    estimated_time_ru = models.CharField('Ориентировочное время (русский)', max_length=100, blank=True)
    estimated_time_kg = models.CharField('Ориентировочное время (кыргызский)', max_length=100, blank=True)
    estimated_time_en = models.CharField('Ориентировочное время (английский)', max_length=100, blank=True)
    
    max_duration_ru = models.CharField('Максимальный срок (русский)', max_length=100, blank=True)
    max_duration_kg = models.CharField('Максимальный срок (кыргызский)', max_length=100, blank=True)
    max_duration_en = models.CharField('Максимальный срок (английский)', max_length=100, blank=True)
    
    contact_info_ru = models.TextField('Контактная информация (русский)', blank=True)
    contact_info_kg = models.TextField('Контактная информация (кыргызский)', blank=True)
    contact_info_en = models.TextField('Контактная информация (английский)', blank=True)
    
    # Немультиязычные поля
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='academic')
    icon = models.CharField('Иконка', max_length=50, choices=ICON_CHOICES, default='DocumentTextIcon')
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    is_active = models.BooleanField(_('Активна'), default=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Инструкция для студентов')
        verbose_name_plural = _('Инструкции для студентов')
        ordering = ['order']

    def __str__(self):
        return self.title_ru


class GuideRequirement(models.Model):
    """Требования в инструкциях"""
    guide = models.ForeignKey(
        StudentGuide,
        on_delete=models.CASCADE,
        related_name='requirements'
    )
    
    # Мультиязычные поля
    text_ru = models.TextField('Текст требования (русский)')
    text_kg = models.TextField('Текст требования (кыргызский)')
    text_en = models.TextField('Текст требования (английский)')
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Требование инструкции')
        verbose_name_plural = _('Требования инструкций')
        ordering = ['order']

    def __str__(self):
        return f"{self.guide.title_ru} - {self.text_ru[:50]}..."


class GuideStep(models.Model):
    """Шаги в инструкциях"""
    guide = models.ForeignKey(
        StudentGuide,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    
    # Мультиязычные поля
    title_ru = models.CharField('Заголовок шага (русский)', max_length=255)
    title_kg = models.CharField('Заголовок шага (кыргызский)', max_length=255)
    title_en = models.CharField('Заголовок шага (английский)', max_length=255)
    
    description_ru = models.TextField('Описание шага (русский)', blank=True)
    description_kg = models.TextField('Описание шага (кыргызский)', blank=True)
    description_en = models.TextField('Описание шага (английский)', blank=True)
    
    timeframe_ru = models.CharField('Время выполнения (русский)', max_length=100, blank=True)
    timeframe_kg = models.CharField('Время выполнения (кыргызский)', max_length=100, blank=True)
    timeframe_en = models.CharField('Время выполнения (английский)', max_length=100, blank=True)
    
    step_number = models.PositiveIntegerField('Номер шага', default=1)
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Шаг инструкции')
        verbose_name_plural = _('Шаги инструкций')
        ordering = ['order']

    def __str__(self):
        return f"{self.guide.title_ru} - Шаг {self.order}: {self.title_ru}"


class GuideStepDetail(models.Model):
    """Детали шагов в инструкциях"""
    step = models.ForeignKey(
        GuideStep,
        on_delete=models.CASCADE,
        related_name='details'
    )
    
    # Мультиязычные поля
    text_ru = models.TextField('Текст детали (русский)')
    text_kg = models.TextField('Текст детали (кыргызский)')
    text_en = models.TextField('Текст детали (английский)')
    
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Деталь шага')
        verbose_name_plural = _('Детали шагов')
        ordering = ['order']

    def __str__(self):
        return f"{self.step.title_ru} - {self.text_ru[:50]}..."


# =============================================================================
# МОДЕЛИ ДЛЯ ОБРАЩЕНИЙ СТУДЕНТОВ
# =============================================================================

class StudentAppeal(models.Model):
    """Обращения студентов"""
    STATUS_CHOICES = [
        ('new', _('Новое')),
        ('in_progress', _('В обработке')),
        ('resolved', _('Решено')),
        ('closed', _('Закрыто')),
    ]
    
    CATEGORY_CHOICES = [
        ('academic', _('Академические вопросы')),
        ('administrative', _('Административные вопросы')),
        ('financial', _('Финансовые вопросы')),
        ('technical', _('Технические вопросы')),
        ('other', _('Другое')),
    ]
    
    # Контактная информация
    full_name = models.CharField(_('ФИО'), max_length=255)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Телефон'), max_length=50, blank=True)
    student_id = models.CharField(_('Студенческий билет'), max_length=50, blank=True)
    
    # Обращение
    category = models.CharField(_('Категория'), max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(_('Тема обращения'), max_length=255)
    message = models.TextField(_('Сообщение'))
    
    # Файлы
    attachment = models.FileField(
        upload_to='appeals/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])],
        verbose_name=_('Прикрепленный файл')
    )
    
    # Статус и метаданные
    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default='new')
    response = models.TextField(_('Ответ'), blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    processed_by = models.CharField(_('Обработано'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Обращение студента')
        verbose_name_plural = _('Обращения студентов')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


# =============================================================================
# МОДЕЛИ ДЛЯ ФОТОГАЛЕРЕИ И ВИДЕО
# =============================================================================

class PhotoAlbum(models.Model):
    """Фотоальбомы студенческой жизни"""
    # Мультиязычные поля
    title_ru = models.CharField('Название альбома (русский)', max_length=255)
    title_kg = models.CharField('Название альбома (кыргызский)', max_length=255)
    title_en = models.CharField('Название альбома (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Обложка альбома
    cover_image = models.ImageField(
        upload_to='photo_albums/covers/',
        verbose_name=_('Обложка альбома')
    )
    
    # Теги для поиска
    tags_ru = models.TextField('Теги (русский)', help_text='Разделяйте запятыми', blank=True)
    tags_kg = models.TextField('Теги (кыргызский)', help_text='Разделяйте запятыми', blank=True)
    tags_en = models.TextField('Теги (английский)', help_text='Разделяйте запятыми', blank=True)
    
    # Немультиязычные поля
    event_date = models.DateField(_('Дата события'))
    is_active = models.BooleanField(_('Активен'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Фотоальбом')
        verbose_name_plural = _('Фотоальбомы')
        ordering = ['-event_date', 'order']

    def __str__(self):
        return self.title_ru

    @property
    def photo_count(self):
        """Количество фотографий в альбоме"""
        return self.photos.filter(is_active=True).count()


class Photo(models.Model):
    """Фотографии в альбомах"""
    album = models.ForeignKey(
        PhotoAlbum,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_('Альбом')
    )
    
    # Мультиязычные поля
    title_ru = models.CharField('Название фото (русский)', max_length=255, blank=True)
    title_kg = models.CharField('Название фото (кыргызский)', max_length=255, blank=True)
    title_en = models.CharField('Название фото (английский)', max_length=255, blank=True)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Файл изображения
    image = models.ImageField(
        upload_to='photos/',
        verbose_name=_('Изображение'),
        blank=True,
        null=True
    )
    
    # URL изображения (для внешних ссылок)
    url = models.URLField(
        verbose_name=_('URL изображения'),
        blank=True,
        null=True,
        help_text='Ссылка на внешнее изображение (альтернатива загрузке файла)'
    )
    
    # Теги для поиска
    tags_ru = models.TextField('Теги (русский)', help_text='Разделяйте запятыми', blank=True)
    tags_kg = models.TextField('Теги (кыргызский)', help_text='Разделяйте запятыми', blank=True)
    tags_en = models.TextField('Теги (английский)', help_text='Разделяйте запятыми', blank=True)
    
    # Немультиязычные поля
    photographer = models.CharField(_('Фотограф'), max_length=255, blank=True)
    is_active = models.BooleanField(_('Активно'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    uploaded_at = models.DateTimeField(_('Дата загрузки'), auto_now_add=True)

    class Meta:
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
        ordering = ['order', '-uploaded_at']

    def __str__(self):
        return f"{self.album.title_ru} - {self.title_ru or f'Фото {self.id}'}"


class VideoContent(models.Model):
    """Видеоконтент студенческой жизни"""
    VIDEO_TYPE_CHOICES = [
        ('event', _('Мероприятие')),
        ('interview', _('Интервью')),
        ('tutorial', _('Обучающее видео')),
        ('announcement', _('Объявление')),
        ('documentary', _('Документальное')),
    ]
    
    # Мультиязычные поля
    title_ru = models.CharField('Название видео (русский)', max_length=255)
    title_kg = models.CharField('Название видео (кыргызский)', max_length=255)
    title_en = models.CharField('Название видео (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Файлы
    video_file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(['mp4', 'avi', 'mov', 'wmv'])],
        verbose_name=_('Видеофайл'),
        blank=True,
        null=True
    )
    
    video_url = models.URLField(_('Ссылка на видео'), blank=True, help_text='YouTube, Vimeo и т.д.')
    
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/',
        verbose_name=_('Превью видео'),
        blank=True,
        null=True
    )
    
    # URL превью (для внешних ссылок)
    thumbnail_url = models.URLField(
        verbose_name=_('URL превью'),
        max_length=500,
        blank=True,
        null=True,
        help_text='Ссылка на внешнее превью (альтернатива загрузке файла)'
    )
    
    # Теги для поиска
    tags_ru = models.TextField('Теги (русский)', help_text='Разделяйте запятыми', blank=True)
    tags_kg = models.TextField('Теги (кыргызский)', help_text='Разделяйте запятыми', blank=True)
    tags_en = models.TextField('Теги (английский)', help_text='Разделяйте запятыми', blank=True)
    
    # Немультиязычные поля
    type = models.CharField(_('Тип видео'), max_length=20, choices=VIDEO_TYPE_CHOICES)
    duration = models.CharField(_('Продолжительность'), max_length=20, blank=True)
    event_date = models.DateField(_('Дата события'), blank=True, null=True)
    views_count = models.PositiveIntegerField(_('Количество просмотров'), default=0)
    is_active = models.BooleanField(_('Активно'), default=True)
    is_featured = models.BooleanField(_('Рекомендуемое'), default=False)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Видеоконтент')
        verbose_name_plural = _('Видеоконтент')
        ordering = ['-created_at', 'order']

    def __str__(self):
        return self.title_ru

    def get_video_source(self):
        """Возвращает источник видео (файл или URL)"""
        return self.video_file.url if self.video_file else self.video_url


class StudentLifeStatistic(models.Model):
    """Статистика студенческой жизни"""
    STATISTIC_TYPE_CHOICES = [
        ('clubs', _('Клубы и организации')),
        ('events', _('Мероприятия')),
        ('photos', _('Фотографии')),
        ('videos', _('Видео')),
        ('students', _('Активные студенты')),
        ('achievements', _('Достижения')),
    ]
    
    # Мультиязычные поля
    label_ru = models.CharField('Название показателя (русский)', max_length=255)
    label_kg = models.CharField('Название показателя (кыргызский)', max_length=255)
    label_en = models.CharField('Название показателя (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)', blank=True)
    description_kg = models.TextField('Описание (кыргызский)', blank=True)
    description_en = models.TextField('Описание (английский)', blank=True)
    
    # Значение статистики
    value = models.CharField(_('Значение'), max_length=50)
    
    # Немультиязычные поля
    type = models.CharField(_('Тип статистики'), max_length=20, choices=STATISTIC_TYPE_CHOICES)
    icon = models.CharField(_('Иконка'), max_length=100, blank=True)
    is_active = models.BooleanField(_('Активна'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    last_updated = models.DateTimeField(_('Последнее обновление'), auto_now=True)

    class Meta:
        verbose_name = _('Статистика студенческой жизни')
        verbose_name_plural = _('Статистика студенческой жизни')
        ordering = ['order', 'type']

    def __str__(self):
        return f"{self.label_ru}: {self.value}"


class EResourceCategory(models.Model):
    """Категории электронных ресурсов"""
    # Мультиязычные поля
    name_ru = models.CharField('Название (русский)', max_length=255)
    name_kg = models.CharField('Название (кыргызский)', max_length=255)
    name_en = models.CharField('Название (английский)', max_length=255)
    
    # Немультиязычные поля
    icon = models.CharField(_('Иконка'), max_length=100, default='📚')
    color = models.CharField(_('Цвет градиента'), max_length=100, default='from-blue-500 to-blue-600')
    is_active = models.BooleanField(_('Активна'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Категория электронных ресурсов')
        verbose_name_plural = _('Категории электронных ресурсов')
        ordering = ['order', 'name_ru']

    def __str__(self):
        return self.name_ru

    @property
    def count(self):
        """Количество активных ресурсов в категории"""
        return self.eresources.filter(is_active=True).count()


class EResource(models.Model):
    """Электронные ресурсы"""
    STATUS_CHOICES = [
        ('online', _('В сети')),
        ('maintenance', _('Техническое обслуживание')),
        ('offline', _('Офлайн')),
    ]
    
    # Связи
    category = models.ForeignKey(
        EResourceCategory, 
        on_delete=models.CASCADE,
        related_name='eresources',
        verbose_name=_('Категория')
    )
    
    # Мультиязычные поля
    title_ru = models.CharField('Название (русский)', max_length=255)
    title_kg = models.CharField('Название (кыргызский)', max_length=255)
    title_en = models.CharField('Название (английский)', max_length=255)
    
    description_ru = models.TextField('Описание (русский)')
    description_kg = models.TextField('Описание (кыргызский)')
    description_en = models.TextField('Описание (английский)')
    
    # Немультиязычные поля
    icon = models.CharField(_('Иконка'), max_length=100, default='🔗')
    color = models.CharField(_('Цвет градиента'), max_length=100, default='from-blue-500 to-blue-600')
    url = models.URLField(_('URL ресурса'), blank=True, null=True)
    users_count = models.PositiveIntegerField(_('Количество пользователей'), default=0)
    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default='online')
    is_popular = models.BooleanField(_('Популярный'), default=False)
    is_active = models.BooleanField(_('Активен'), default=True)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Электронный ресурс')
        verbose_name_plural = _('Электронные ресурсы')
        ordering = ['order', 'title_ru']

    def __str__(self):
        return self.title_ru

    @property
    def users_display(self):
        """Форматированное отображение количества пользователей"""
        if self.users_count >= 1000:
            return f"{self.users_count // 1000}k+"
        return f"{self.users_count}+"


class EResourceFeature(models.Model):
    """Особенности электронных ресурсов"""
    # Связи
    resource = models.ForeignKey(
        EResource,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name=_('Ресурс')
    )
    
    # Мультиязычные поля
    text_ru = models.CharField('Текст (русский)', max_length=255)
    text_kg = models.CharField('Текст (кыргызский)', max_length=255)
    text_en = models.CharField('Текст (английский)', max_length=255)
    
    # Немультиязычные поля
    order = models.PositiveIntegerField(_('Порядок'), default=0)

    class Meta:
        verbose_name = _('Особенность ресурса')
        verbose_name_plural = _('Особенности ресурсов')
        ordering = ['order']

    def __str__(self):
        return f"{self.resource.title_ru} - {self.text_ru}"
