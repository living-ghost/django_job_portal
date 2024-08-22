# ================================
#        URL Configuration
# ================================

from django.urls import path
from . import views

urlpatterns = [
    # Route for the file converter index view
    path('index/', views.converter_index_view, name='converter_index'),
]