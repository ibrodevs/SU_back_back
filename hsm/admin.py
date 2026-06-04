from django.contrib import admin
from .models import (
    Faculty, Accreditation, Leadership,
    QualityPrinciple, QualityDocument, QualityProcessGroup,
    QualityProcess, QualityStatistic, QualityAdvantage, QualitySettings,
    HSMInfo
)

admin.site.register(HSMInfo)


@admin.register(QualityPrinciple)
class QualityPrincipleAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'title_kg', 'title_en', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'title_kg', 'title_en', 'icon')
        }),
        ('Описание', {
            'fields': ('description', 'description_kg', 'description_en')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(QualityDocument)
class QualityDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'document_type', 'version', 'approval_date', 'download_count', 'order', 'is_active']
    list_filter = ['category', 'document_type', 'is_active', 'approval_date']
    search_fields = ['title', 'title_kg', 'title_en', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'download_count']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'title_kg', 'title_en', 'category')
        }),
        ('Описание', {
            'fields': ('description', 'description_kg', 'description_en')
        }),
        ('Файл', {
            'fields': ('document_type', 'file_size', 'file_path', 'external_url')
        }),
        ('Версия и даты', {
            'fields': ('version', 'approval_date', 'effective_date', 'expiry_date')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active', 'download_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(QualityProcessGroup)
class QualityProcessGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'title_kg', 'title_en', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'title_kg', 'title_en', 'icon')
        }),
        ('Описание', {
            'fields': ('description', 'description_kg', 'description_en')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(QualityProcess)
class QualityProcessAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'responsible_person', 'responsible_department', 'order', 'is_active']
    list_filter = ['group', 'is_active']
    search_fields = ['title', 'title_kg', 'title_en', 'responsible_person', 'responsible_department']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('group', 'title', 'title_kg', 'title_en')
        }),
        ('Описание', {
            'fields': ('description', 'description_kg', 'description_en')
        }),
        ('Ответственные', {
            'fields': ('responsible_person', 'responsible_department')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(QualityStatistic)
class QualityStatisticAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'unit', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'title_kg', 'title_en', 'value']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'title_kg', 'title_en', 'icon')
        }),
        ('Значение', {
            'fields': ('value', 'unit')
        }),
        ('Описание', {
            'fields': ('description', 'description_kg', 'description_en')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(QualityAdvantage)
class QualityAdvantageAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'title_kg', 'title_en', 'description']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'title_kg', 'title_en', 'icon')
        }),
        ('Описание', {
            'fields': ('description', 'description_kg', 'description_en')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(QualitySettings)
class QualitySettingsAdmin(admin.ModelAdmin):
    list_display = ['title', 'iso_standard', 'compliance_percentage', 'is_active']
    list_filter = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Заголовок и описание', {
            'fields': ('title', 'title_kg', 'title_en', 'description', 'description_kg', 'description_en')
        }),
        ('О системе качества', {
            'fields': ('about_text', 'about_text_kg', 'about_text_en')
        }),
        ('Стандарты', {
            'fields': ('iso_standard', 'compliance_percentage')
        }),
        ('Настройки', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        # Разрешаем создавать только если нет активных записей
        return not QualitySettings.objects.filter(is_active=True).exists()


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'department', 'leadership_type', 'is_director', 'is_active', 'order']
    list_filter = ['leadership_type', 'department', 'is_director', 'is_active']
    search_fields = ['name', 'name_kg', 'name_en', 'position', 'email']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'name_kg', 'name_en', 'image')
        }),
        ('Должность', {
            'fields': ('position', 'position_kg', 'position_en', 'leadership_type', 'is_director')
        }),
        ('Ученая степень', {
            'fields': ('degree', 'degree_kg', 'degree_en')
        }),
        ('Опыт работы', {
            'fields': ('experience', 'experience_kg', 'experience_en')
        }),
        ('Департамент/Кафедра', {
            'fields': ('department', 'department_kg', 'department_en')
        }),
        ('Специализация', {
            'fields': ('specialization', 'specialization_kg', 'specialization_en'),
            'classes': ('collapse',)
        }),
        ('Количество сотрудников', {
            'fields': ('staff_count', 'staff_count_kg', 'staff_count_en'),
            'classes': ('collapse',)
        }),
        ('Контакты', {
            'fields': ('email', 'phone')
        }),
        ('Биография', {
            'fields': ('bio', 'bio_kg', 'bio_en'),
            'classes': ('collapse',)
        }),
        ('Достижения', {
            'fields': ('achievements', 'achievements_kg', 'achievements_en'),
            'classes': ('collapse',)
        }),
        ('Системные поля', {
            'fields': ('is_active', 'order', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        # Автоматически устанавливаем тип руководства для директоров
        if obj.is_director:
            obj.leadership_type = 'director'
        super().save_model(request, obj, form, change)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'academic_degree', 'email', 'is_active', 'order']
    list_filter = ['position', 'academic_degree', 'is_active']
    search_fields = ['first_name', 'last_name', 'middle_name', 'first_name_kg', 'last_name_kg',
                    'first_name_en', 'last_name_en', 'email', 'specialization']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'full_name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'photo')
        }),
        ('Перевод на кыргызский', {
            'fields': ('first_name_kg', 'last_name_kg', 'middle_name_kg'),
            'classes': ('collapse',)
        }),
        ('Перевод на английский', {
            'fields': ('first_name_en', 'last_name_en', 'middle_name_en'),
            'classes': ('collapse',)
        }),
        ('Должность и степень', {
            'fields': ('position', 'position_custom', 'academic_degree', 'academic_title')
        }),
        ('Контакты', {
            'fields': ('email', 'phone', 'office')
        }),
        ('Биография', {
            'fields': ('bio', 'bio_kg', 'bio_en'),
            'classes': ('collapse',)
        }),
        ('Специализация', {
            'fields': ('specialization', 'specialization_kg', 'specialization_en'),
            'classes': ('collapse',)
        }),
        ('Образование', {
            'fields': ('education', 'education_kg', 'education_en'),
            'classes': ('collapse',)
        }),
        ('Опыт работы', {
            'fields': ('experience', 'experience_kg', 'experience_en'),
            'classes': ('collapse',)
        }),
        ('Публикации', {
            'fields': ('publications', 'publications_kg', 'publications_en'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Accreditation)
class AccreditationAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'accreditation_type', 'issue_date', 'expiry_date', 'is_valid', 'is_active']
    list_filter = ['accreditation_type', 'is_active', 'issue_date', 'expiry_date']
    search_fields = ['name', 'name_kg', 'name_en', 'organization', 'certificate_number']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'is_valid']
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'name_kg', 'name_en', 'accreditation_type')
        }),
        ('Организация', {
            'fields': ('organization', 'organization_kg', 'organization_en', 'organization_logo')
        }),
        ('Описание', {
            'fields': ('description', 'description_kg', 'description_en'),
            'classes': ('collapse',)
        }),
        ('Сертификат', {
            'fields': ('certificate_image', 'certificate_number', 'issue_date', 'expiry_date')
        }),
        ('Настройки', {
            'fields': ('is_active', 'order')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at', 'is_valid'),
            'classes': ('collapse',)
        })
    )
