from django.db import models

class OfficialContent(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name="Ключ секции")
    content = models.JSONField(verbose_name="Контент (все языки)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Официальный контент"
        verbose_name_plural = "Официальный контент"
        ordering = ['key']
        
    def __str__(self):
        return self.key
