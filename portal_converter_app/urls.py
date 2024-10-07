from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.converter_index_view, name='converter_index'),
]