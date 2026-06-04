from django.urls import path
from .views import submit_application_email, official_content_list

urlpatterns = [
    path('applications/submit-email/', submit_application_email, name='submit_application_email'),
    path('official-content/', official_content_list, name='official_content_list'),
]
