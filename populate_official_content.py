#!/usr/bin/env python3
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_su_m.settings')
django.setup()

from admissions.models import OfficialContent

def populate():
    json_path = os.path.join(os.path.dirname(__file__), 'official_content.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for key, content_data in data.items():
        obj, created = OfficialContent.objects.update_or_create(
            key=key,
            defaults={'content': content_data}
        )
        status = 'Created' if created else 'Updated'
        print(f"{status} OfficialContent: {key}")
        
    print("Population completed successfully!")

if __name__ == '__main__':
    populate()
