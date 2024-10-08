from django.urls import path
from . import views

urlpatterns = [
    path('', views.ats_home_view, name='ats_index'),
    path('upload/', views.ats_upload_view, name='ats_upload'),
    path('check/<int:resume_id>/', views.ats_check_view, name='ats_check'),
]