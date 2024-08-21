from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.admin_login_view, name='admin_login'),
    path('index/', views.admin_index_view, name='admin_index'),
    path('logout/', views.admin_logout_view, name='admin_logout'),

    path('job/', views.jobs_view, name='admin_job'),
    path('job/add/', views.jobs_add_view, name='admin_add_job'),
    path('job/list/', views.jobs_list_view, name='admin_list_job'),
    path('freshers/list/', views.fresher_list_view, name='admin_fresher_jobs'),
    path('experienced/list/', views.exp_list_view, name='admin_exp_jobs'),
    path('featured/list/', views.feat_list_view, name='admin_feat_jobs'),
    path('deleted/list/', views.del_list_view, name='admin_del_jobs'),

    path('job/delete/<int:job_id>/', views.jobs_delete_view, name='admin_delete_job'),
    path('job/edit/<int:job_id>/', views.jobs_edit_view, name='admin_edit_job'),

    path('user/', views.users_view, name='admin_user'),
    path('user/list/', views.users_list_view, name='admin_list_user'),
    path('user/profile/', views.admin_profile_view, name='admin_profile'),
]