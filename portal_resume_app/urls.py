from django.urls import path
from . import views

app_name = 'portal_resume_app'

urlpatterns = [ 
    # ================================
    #        Index Page and Form Submissions
    # ================================
    path('index/', views.resume_index_view, name='resume_index'),

    # ================================
    #        Save Resume
    # ================================
    path('save/', views.resume_save_view, name='resume_save'),

    # ================================
    #        List All Resumes
    # ================================
    path('list/', views.resume_list_view, name='resume_list'),

    # ================================
    #        View Specific Resume
    # ================================
    path('view/<int:resume_id>/', views.resume_display_view, name='resume_display'),

    # ================================
    #        Download Resume as PDF
    # ================================
    path('download/<int:resume_id>/', views.resume_download_view, name='resume_download'),

    # ================================
    #        Delete Resume Fields
    # ================================
    path('delete/hobbie/', views.delete_hobbie_view, name='resume_del_hob'),
    path('delete/skill/', views.delete_skill_view, name='resume_del_skill'),
    path('delete/certificate/', views.delete_certi_view, name='resume_del_certi'),
    path('delete/project/', views.delete_pro_view, name='resume_del_pro'),
    path('delete/language/', views.delete_lang_view, name='resume_del_lang'),
    path('delete/experience/', views.delete_exp_view, name='resume_del_exp'),
    path('delete/education/', views.delete_edu_view, name='resume_del_edu'),

    # ================================
    #        Test Resume Template
    # ================================
    path('test/', views.resume_test_view, name='test')
]