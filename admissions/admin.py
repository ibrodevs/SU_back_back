from django.contrib import admin
from .models import OfficialContent

@admin.register(OfficialContent)
class OfficialContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'updated_at')
    search_fields = ('key',)
    ordering = ('key',)
