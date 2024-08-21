from django.urls import path
from . import views

app_name = 'portal_resume_app'

urlpatterns = [ 
	path('index/', views.resume_index_view, name = 'resume_index'),
    path('save/', views.resume_save_view, name='resume_save'),
    path('list/', views.resume_list_view, name='resume_list'),
    path('view/<int:resume_id>/', views.resume_display_view, name='resume_display'),
    path('download/<int:resume_id>/', views.resume_download_view, name='resume_download'),

    path('delete/hobbie/', views.delete_hobbie_view, name='resume_del_hob'),
    path('delete/skill/', views.delete_skill_view, name='resume_del_skill'),
    path('delete/certificate/', views.delete_certi_view, name='resume_del_certi'),
    path('delete/project/', views.delete_pro_view, name='resume_del_pro'),
    path('delete/language/', views.delete_lang_view, name='resume_del_lang'),
    path('delete/experience/', views.delete_exp_view, name='resume_del_exp'),
    path('delete/education/', views.delete_edu_view, name='resume_del_edu'),

    path('test/', views.resume_test_view, name='test')
]