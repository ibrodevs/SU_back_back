from rest_framework import serializers
from .models import OfficialContent

class OfficialContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialContent
        fields = ['id', 'key', 'content', 'created_at', 'updated_at']
