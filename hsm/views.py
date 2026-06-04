from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.http import Http404
from .models import (
    Faculty, Accreditation, Leadership,
    QualityPrinciple, QualityDocument, QualityProcessGroup,
    QualityProcess, QualityStatistic, QualityAdvantage, QualitySettings,
    HSMInfo
)
from .serializers import (
    FacultySerializer,
    FacultyListSerializer,
    AccreditationSerializer,
    LeadershipSerializer,
    QualityPrincipleSerializer,
    QualityDocumentSerializer,
    QualityProcessGroupSerializer,
    QualityProcessSerializer,
    QualityStatisticSerializer,
    QualityAdvantageSerializer,
    QualitySettingsSerializer,
    QualityManagementSystemSerializer,
    HSMInfoSerializer
)


class HSMInfoView(APIView):
    """Общая информация о Высшей школе медицины."""
    def get(self, request):
        info = HSMInfo.objects.filter(is_active=True).first()
        if not info:
            return Response({}, status=status.HTTP_200_OK)
        return Response(HSMInfoSerializer(info).data)


class QualityManagementSystemView(APIView):
    """API для получения всех данных системы менеджмента качества"""
    
    def get(self, request):
        try:
            # Получаем основные настройки (должна быть только одна запись)
            settings = QualitySettings.objects.filter(is_active=True).first()
            
            # Получаем все активные данные
            principles = QualityPrinciple.objects.filter(is_active=True).order_by('order')
            documents = QualityDocument.objects.filter(is_active=True).order_by('category', 'order')
            process_groups = QualityProcessGroup.objects.filter(is_active=True).prefetch_related('processes').order_by('order')
            statistics = QualityStatistic.objects.filter(is_active=True).order_by('order')
            advantages = QualityAdvantage.objects.filter(is_active=True).order_by('order')
            
            # Сериализуем данные
            data = {
                'settings': QualitySettingsSerializer(settings, context={'request': request}).data if settings else None,
                'principles': QualityPrincipleSerializer(principles, many=True, context={'request': request}).data,
                'documents': QualityDocumentSerializer(documents, many=True, context={'request': request}).data,
                'process_groups': QualityProcessGroupSerializer(process_groups, many=True, context={'request': request}).data,
                'statistics': QualityStatisticSerializer(statistics, many=True, context={'request': request}).data,
                'advantages': QualityAdvantageSerializer(advantages, many=True, context={'request': request}).data,
            }
            
            return Response(data)
        except Exception as e:
            return Response(
                {'error': 'Ошибка получения данных системы качества', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QualityPrincipleViewSet(viewsets.ReadOnlyModelViewSet):
    """API для принципов качества"""
    queryset = QualityPrinciple.objects.filter(is_active=True).order_by('order')
    serializer_class = QualityPrincipleSerializer


class QualityDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """API для документов качества"""
    queryset = QualityDocument.objects.filter(is_active=True).order_by('category', 'order')
    serializer_class = QualityDocumentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Увеличить счетчик скачиваний документа"""
        try:
            document = self.get_object()
            document.download_count += 1
            document.save(update_fields=['download_count'])
            return Response({'success': True, 'download_count': document.download_count})
        except Exception as e:
            return Response(
                {'error': 'Ошибка обновления счетчика скачиваний', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить документы сгруппированные по категориям"""
        categories = dict(QualityDocument.DOCUMENT_CATEGORIES)
        result = {}
        
        for category_key, category_name in categories.items():
            documents = self.queryset.filter(category=category_key)
            result[category_key] = {
                'name': category_name,
                'documents': QualityDocumentSerializer(documents, many=True, context={'request': request}).data
            }
        
        return Response(result)


class QualityProcessGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """API для групп процессов качества"""
    queryset = QualityProcessGroup.objects.filter(is_active=True).prefetch_related('processes').order_by('order')
    serializer_class = QualityProcessGroupSerializer


class QualityProcessViewSet(viewsets.ReadOnlyModelViewSet):
    """API для процессов качества"""
    queryset = QualityProcess.objects.filter(is_active=True).select_related('group').order_by('group__order', 'order')
    serializer_class = QualityProcessSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group', None)
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)
            
        return queryset


class QualityStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """API для статистики качества"""
    queryset = QualityStatistic.objects.filter(is_active=True).order_by('order')
    serializer_class = QualityStatisticSerializer


class QualityAdvantageViewSet(viewsets.ReadOnlyModelViewSet):
    """API для преимуществ качества"""
    queryset = QualityAdvantage.objects.filter(is_active=True).order_by('order')
    serializer_class = QualityAdvantageSerializer


class QualitySettingsView(APIView):
    """API для настроек системы качества"""
    
    def get(self, request):
        try:
            settings = QualitySettings.objects.filter(is_active=True).first()
            if settings:
                serializer = QualitySettingsSerializer(settings, context={'request': request})
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Настройки системы качества не найдены'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {'error': 'Ошибка получения настроек', 'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LeadershipViewSet(viewsets.ReadOnlyModelViewSet):
    """API для руководства ВШМ"""
    queryset = Leadership.objects.filter(is_active=True)
    serializer_class = LeadershipSerializer
    
    def get_queryset(self):
        queryset = Leadership.objects.filter(is_active=True)
        leadership_type = self.request.query_params.get('type', None)
        department = self.request.query_params.get('department', None)
        
        if leadership_type:
            queryset = queryset.filter(leadership_type=leadership_type)
        
        if department:
            queryset = queryset.filter(department=department)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def directors(self, request):
        """Получить только директоров"""
        directors = Leadership.objects.filter(is_active=True, is_director=True).order_by('order')
        serializer = self.get_serializer(directors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def department_heads(self, request):
        """Получить заведующих кафедрами"""
        heads = Leadership.objects.filter(
            is_active=True, 
            is_director=False,
            leadership_type='department_head'
        ).order_by('order')
        serializer = self.get_serializer(heads, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """Получить руководство по департаментам"""
        department = request.query_params.get('department')
        if not department:
            return Response({'error': 'Department parameter is required'}, status=400)
        
        leadership = Leadership.objects.filter(
            is_active=True,
            department=department
        ).order_by('order')
        serializer = self.get_serializer(leadership, many=True)
        return Response(serializer.data)


class FacultyViewSet(viewsets.ReadOnlyModelViewSet):
    """API для профессорско-преподавательского состава ВШМ"""
    queryset = Faculty.objects.filter(is_active=True)
    serializer_class = FacultySerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FacultySerializer
        return FacultySerializer
    
    def get_queryset(self):
        queryset = Faculty.objects.filter(is_active=True)
        position = self.request.query_params.get('position', None)
        search = self.request.query_params.get('search', None)
        
        if position:
            queryset = queryset.filter(position=position)
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(middle_name__icontains=search) |
                Q(first_name_kg__icontains=search) |
                Q(last_name_kg__icontains=search) |
                Q(first_name_en__icontains=search) |
                Q(last_name_en__icontains=search) |
                Q(specialization__icontains=search) |
                Q(specialization_kg__icontains=search) |
                Q(specialization_en__icontains=search)
            )
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_position(self, request):
        """Получить преподавателей по должностям"""
        positions = Faculty.POSITIONS
        result = {}
        
        # Переводы для названий должностей
        position_translations = {
            'professor': {
                'ru': 'Профессор',
                'kg': 'Профессор', 
                'en': 'Professor'
            },
            'associate_professor': {
                'ru': 'Доцент',
                'kg': 'Доцент',
                'en': 'Associate Professor'
            },
            'senior_lecturer': {
                'ru': 'Старший преподаватель',
                'kg': 'Улук окутуучу',
                'en': 'Senior Lecturer'
            },
            'lecturer': {
                'ru': 'Преподаватель',
                'kg': 'Окутуучу',
                'en': 'Lecturer'
            },
            'assistant': {
                'ru': 'Ассистент',
                'kg': 'Ассистент',
                'en': 'Assistant'
            },
            'head_of_department': {
                'ru': 'Заведующий кафедрой',
                'kg': 'Кафедра башчысы',
                'en': 'Head of Department'
            },
            'dean': {
                'ru': 'Декан',
                'kg': 'Декан',
                'en': 'Dean'
            },
            'vice_dean': {
                'ru': 'Заместитель декана',
                'kg': 'Декандын орун басары',
                'en': 'Vice Dean'
            }
        }
        
        for position_code, position_name in positions:
            faculty = Faculty.objects.filter(
                is_active=True, 
                position=position_code
            ).order_by('order', 'last_name')
            
            if faculty.exists():  # Только если есть преподаватели с такой должностью
                serializer = FacultySerializer(faculty, many=True, context={'request': request})
                result[position_code] = {
                    'name': position_name,  # Русское название (по умолчанию)
                    'name_kg': position_translations.get(position_code, {}).get('kg', position_name),
                    'name_en': position_translations.get(position_code, {}).get('en', position_name),
                    'faculty': serializer.data
                }
        
        return Response(result)


class AccreditationViewSet(viewsets.ReadOnlyModelViewSet):
    """API для аккредитаций ВШМ"""
    queryset = Accreditation.objects.filter(is_active=True)
    serializer_class = AccreditationSerializer
    
    def get_queryset(self):
        queryset = Accreditation.objects.filter(is_active=True)
        accreditation_type = self.request.query_params.get('type', None)
        valid_only = self.request.query_params.get('valid_only', None)
        
        if accreditation_type:
            queryset = queryset.filter(accreditation_type=accreditation_type)
        
        if valid_only == 'true':
            from django.utils import timezone
            queryset = queryset.filter(
                Q(expiry_date__isnull=True) |
                Q(expiry_date__gte=timezone.now().date())
            )
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Получить аккредитации по типам"""
        types = Accreditation.ACCREDITATION_TYPES
        result = {}
        
        # Переводы для типов аккредитации
        type_translations = {
            'national': {
                'ru': 'Национальная',
                'kg': 'Улуттук',
                'en': 'National'
            },
            'international': {
                'ru': 'Международная',
                'kg': 'Эл аралык',
                'en': 'International'
            },
            'institutional': {
                'ru': 'Институциональная',
                'kg': 'Институционалдык',
                'en': 'Institutional'
            },
            'programmatic': {
                'ru': 'Программная',
                'kg': 'Программалык',
                'en': 'Programmatic'
            }
        }
        
        for type_code, type_name in types:
            accreditations = Accreditation.objects.filter(
                is_active=True,
                accreditation_type=type_code
            ).order_by('order', '-issue_date')
            
            if accreditations.exists():  # Только если есть аккредитации такого типа
                serializer = AccreditationSerializer(accreditations, many=True, context={'request': request})
                result[type_code] = {
                    'name': type_name,  # Русское название (по умолчанию)
                    'name_kg': type_translations.get(type_code, {}).get('kg', type_name),
                    'name_en': type_translations.get(type_code, {}).get('en', type_name),
                    'accreditations': serializer.data
                }
        
        return Response(result)


