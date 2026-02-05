import os
import django
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

print("=" * 60)
print("ПРОВЕРКА СТАТИЧЕСКИХ ФАЙЛОВ АДМИНКИ")
print("=" * 60)

print("\n1. Django настройки:")
print(f"   STATIC_URL: {settings.STATIC_URL}")
print(f"   Storage: {staticfiles_storage.__class__.__name__}")

print("\n2. Проверка CSS файлов админки:")
admin_css_files = [
    'admin/css/base.css',
    'admin/css/dashboard.css',
    'admin/css/forms.css',
]

for css_file in admin_css_files:
    try:
        url = staticfiles_storage.url(css_file)
        exists = staticfiles_storage.exists(css_file)
        print(f"   {'✅' if exists else '❌'} {css_file}")
        print(f"      URL: {url}")
    except Exception as e:
        print(f"   ❌ {css_file}: {e}")

print("\n" + "=" * 60)
