# ================================
#          Django Imports
# ================================

from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    # ================================
    #          Main Pages
    # ================================

    path('', views.index_view, name='user_index'),  # Home page
    path('about/', views.about_view, name='user_about'),  # About page

    # ================================
    #          Job Listings
    # ================================

    path('job/fresher/', views.fresher_jobs_view, name='fresher_jobs'),  # Fresher job listings
    path('job/professionals/', views.exp_jobs_view, name='experienced_jobs'),  # Experienced job listings

    # ================================
    #          Search
    # ================================

    path('search/', views.search_jobs_view, name='user_search'),  # Job search

    # ================================
    #          Contact Us
    # ================================

    path('contact/', views.contact_us_view, name='user_contact'),  # User Contact Us

    # ================================
    #          User Actions
    # ================================

    path('user/subscribe/', views.subscribe_view, name='user_subscribe'),  # Subscribe to updates
    path('user/verify/otp/', views.verify_otp_view, name='user_verify_otp'),  # Verify OTP for subscription
    path('user/unsubscribe/', views.unsubscribe_view, name='user_unsubscribe'),  # Unsubscribe

    path('user/login/', views.user_login_view, name='user_login'),  # User login
    path('user/register/', views.user_register_view, name='user_register'),  # User registration
    path('user/register/verify/otp/', views.user_register_verify_otp_view, name='user_reg_verify_otp'),  # Verify OTP for registration
    path('user/register/forgot/pwd/', views.user_forgot_pwd_view, name='user_forgot_pwd'),  # Forgot password
    path('user/dashboard/', views.user_dashboard_view, name='user_dashboard'),  # User dashboard
    path('user/logout/', views.user_logout_view, name='user_logout'),  # User logout
    path('user/password/reset/', views.user_pwd_reset_view, name='user_reset_pwd'),  # Reset password
    path('user/account/delete/', views.user_del_ac_view, name='user_del_ac'),  # Delete account

    # ================================
    #          Error Handling
    # ================================

    path('user/404/error/', views.user_404_view, name='user_404'),  # 404 error page

    # ================================
    #          Payment
    # ================================

    path('payment/index/', views.user_razorpay_view, name='user_payment_index'),
    path('user/payment/', views.user_payment_view, name='user_payment'),

    # ================================
    #          Redirects
    # ================================

    re_path(r'^register/verify/$', RedirectView.as_view(url='/user/register/verify/otp/', permanent=True)),  # Redirect old URL format
]