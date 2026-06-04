from rest_framework import serializers
from .models import (
    Faculty, Accreditation, Leadership,
    QualityPrinciple, QualityDocument, QualityProcessGroup,
    QualityProcess, QualityStatistic, QualityAdvantage, QualitySettings,
    HSMInfo
)


class HSMInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSMInfo
        fields = [
            'id', 'title', 'title_en', 'title_kg',
            'description', 'description_en', 'description_kg',
            'history', 'history_en', 'history_kg',
            'main_directions', 'main_directions_en', 'main_directions_kg',
        ]


class QualityPrincipleSerializer(serializers.ModelSerializer):
    """Сериализатор для принципов качества"""
    
    class Meta:
        model = QualityPrinciple
        fields = [
            'id', 'title', 'title_kg', 'title_en',
            'description', 'description_kg', 'description_en',
            'icon', 'order', 'is_active'
        ]


class QualityDocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для документов качества"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = QualityDocument
        fields = [
            'id', 'title', 'title_kg', 'title_en',
            'description', 'description_kg', 'description_en',
            'category', 'category_display', 'document_type', 'document_type_display',
            'file_size', 'file_url', 'external_url', 'version',
            'approval_date', 'formatted_date', 'download_count', 'order'
        ]
    
    def get_file_url(self, obj):
        if obj.file_path:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file_path.url)
            return obj.file_path.url
        return obj.external_url
    
    def get_formatted_date(self, obj):
        if obj.approval_date:
            return obj.approval_date.strftime('%d.%m.%Y')
        return obj.created_at.strftime('%d.%m.%Y')


class QualityProcessSerializer(serializers.ModelSerializer):
    """Сериализатор для процессов качества"""
    
    class Meta:
        model = QualityProcess
        fields = [
            'id', 'title', 'title_kg', 'title_en',
            'description', 'description_kg', 'description_en',
            'responsible_person', 'responsible_department', 'order'
        ]


class QualityProcessGroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп процессов качества"""
    processes = QualityProcessSerializer(many=True, read_only=True)
    
    class Meta:
        model = QualityProcessGroup
        fields = [
            'id', 'title', 'title_kg', 'title_en',
            'description', 'description_kg', 'description_en',
            'icon', 'order', 'processes'
        ]


class QualityStatisticSerializer(serializers.ModelSerializer):
    """Сериализатор для статистики качества"""
    display_value = serializers.SerializerMethodField()
    
    class Meta:
        model = QualityStatistic
        fields = [
            'id', 'title', 'title_kg', 'title_en',
            'value', 'unit', 'display_value',
            'description', 'description_kg', 'description_en',
            'icon', 'order'
        ]
    
    def get_display_value(self, obj):
        if obj.unit:
            return f"{obj.value} {obj.unit}"
        return obj.value


class QualityAdvantageSerializer(serializers.ModelSerializer):
    """Сериализатор для преимуществ качества"""
    
    class Meta:
        model = QualityAdvantage
        fields = [
            'id', 'title', 'title_kg', 'title_en',
            'description', 'description_kg', 'description_en',
            'icon', 'order'
        ]


class QualitySettingsSerializer(serializers.ModelSerializer):
    """Сериализатор для настроек качества"""
    
    class Meta:
        model = QualitySettings
        fields = [
            'id', 'title', 'title_kg', 'title_en',
            'description', 'description_kg', 'description_en',
            'about_text', 'about_text_kg', 'about_text_en',
            'iso_standard', 'compliance_percentage'
        ]


class QualityManagementSystemSerializer(serializers.Serializer):
    """Комплексный сериализатор для всей системы менеджмента качества"""
    settings = QualitySettingsSerializer(read_only=True)
    principles = QualityPrincipleSerializer(many=True, read_only=True)
    documents = QualityDocumentSerializer(many=True, read_only=True)
    process_groups = QualityProcessGroupSerializer(many=True, read_only=True)
    statistics = QualityStatisticSerializer(many=True, read_only=True)
    advantages = QualityAdvantageSerializer(many=True, read_only=True)


class LeadershipSerializer(serializers.ModelSerializer):
    """Сериализатор для руководства ВШМ"""
    leadership_type_display = serializers.CharField(source='get_leadership_type_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Leadership
        fields = [
            'id', 'name', 'name_kg', 'name_en',
            'position', 'position_kg', 'position_en',
            'degree', 'degree_kg', 'degree_en',
            'experience', 'experience_kg', 'experience_en',
            'bio', 'bio_kg', 'bio_en',
            'achievements', 'achievements_kg', 'achievements_en',
            'department', 'department_kg', 'department_en',
            'specialization', 'specialization_kg', 'specialization_en',
            'staff_count', 'staff_count_kg', 'staff_count_en',
            'email', 'phone', 'image', 'image_url',
            'leadership_type', 'leadership_type_display',
            'is_director', 'order'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class FacultyListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка преподавателей (краткая информация)"""
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    academic_degree_display = serializers.CharField(source='get_academic_degree_display', read_only=True)
    full_name = serializers.CharField(read_only=True)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = [
            'id', 'first_name', 'last_name', 'middle_name',
            'first_name_kg', 'last_name_kg', 'middle_name_kg',
            'first_name_en', 'last_name_en', 'middle_name_en',
            'position', 'position_display', 'position_custom',
            'position_kg', 'position_en',
            'academic_degree', 'academic_degree_display', 
            'academic_degree_kg', 'academic_degree_en',
            'academic_title', 'academic_title_kg', 'academic_title_en',
            'photo', 'photo_url', 'full_name', 'order'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class FacultySerializer(serializers.ModelSerializer):
    """Полный сериализатор для преподавателей"""
    position_display = serializers.CharField(source='get_position_display', read_only=True)
    academic_degree_display = serializers.CharField(source='get_academic_degree_display', read_only=True)
    full_name = serializers.CharField(read_only=True)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Faculty
        fields = '__all__'

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class AccreditationSerializer(serializers.ModelSerializer):
    accreditation_type_display = serializers.CharField(source='get_accreditation_type_display', read_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    certificate_image_url = serializers.SerializerMethodField()
    organization_logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Accreditation
        fields = '__all__'

    def get_certificate_image_url(self, obj):
        if obj.certificate_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.certificate_image.url)
            return obj.certificate_image.url
        return None

    def get_organization_logo_url(self, obj):
        if obj.organization_logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.organization_logo.url)
            return obj.organization_logo.url
        return None
