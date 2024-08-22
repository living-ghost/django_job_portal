from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [

    # Main Pages

    path('', views.index_view, name='user_index'),
    path('about/', views.about_view, name='user_about'),

    # Job Listings

    path('job/fresher/', views.fresher_jobs_view, name='fresher_jobs'),
    path('job/professionals/', views.exp_jobs_view, name='experienced_jobs'),

    # Search

    path('search/', views.search_jobs_view, name='user_search'),

    # User Actions

    path('user/subscribe/', views.subscribe_view, name='user_subscribe'),
    path('user/verify/otp/', views.verify_otp_view, name='user_verify_otp'),
    path('user/unsubscribe/', views.unsubscribe_view, name='user_unsubscribe'),

    #

    path('user/login/', views.user_login_view, name='user_login'),
    path('user/register/', views.user_register_view, name='user_register'),
    path('user/register/verify/otp/', views.user_register_verify_otp_view, name='user_reg_verify_otp'),
    path('user/register/forgot/pwd/', views.user_forgot_pwd_view, name='user_forgot_pwd'),
    path('user/dashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('user/logout/', views.user_logout_view, name='user_logout'),
    path('user/password/reset/', views.user_pwd_reset_view, name='user_reset_pwd'),
    path('user/account/delete/', views.user_del_ac_view, name='user_del_ac'),

    # 404 Error

    path('user/404/error/', views.user_404_view, name='user_404'),

    # Redirect for old URL format
    re_path(r'^register/verify/$', RedirectView.as_view(url='/user/register/verify/otp/', permanent=True)),
]