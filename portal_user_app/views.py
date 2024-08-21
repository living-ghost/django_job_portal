from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q 
from django.utils import timezone
from .models import Subscriber, User
from django.contrib import messages
from portal_admin_app.models import Job
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from . utils import (
    generate_otp, 
    send_account_created_email, send_subscription_email, send_otp_email,
    generate_password, send_reset_email
    )
from django.contrib.auth import update_session_auth_hash

# Create your views here.


''' adding/viewing/searching jobs section '''

# home page listing featured items

def index_view(request):
    featureds = Job.objects.all().order_by('-job_created_at')  # Sort by latest date first
    current_date = timezone.now().date()

    for feature in featureds:
        days_ago = (current_date - feature.job_created_at.date()).days
        
        if days_ago == 0:
            feature.days_ago_display = "Posted today"
        elif days_ago == 1:
            feature.days_ago_display = "1 day ago"
        else:
            feature.days_ago_display = f"{days_ago} days ago"

    return render(request, "portal_user_app/index.html", {'featureds': featureds})

# jobs page listing freshers jobs

def fresher_jobs_view(request):
    jobs = Job.objects.all().order_by('-job_created_at')  # Sort by latest date first
    current_date = timezone.now().date()

    for job in jobs:
        days_ago = (current_date - job.job_created_at.date()).days

        if days_ago == 0:
            job.days_ago_display = "Posted today"
        elif days_ago == 1:
            job.days_ago_display = "1 day ago"
        else:
            job.days_ago_display = f"{days_ago} days ago"

    # Pagination
    paginator = Paginator(jobs, 14)  # Show 10 jobs per page
    page = request.GET.get('page')

    try:
        paginated_jobs = paginator.page(page)
    except PageNotAnInteger:
        paginated_jobs = paginator.page(1)
    except EmptyPage:
        paginated_jobs = paginator.page(paginator.num_pages)

    return render(request, "portal_user_app/fresher_jobs.html", {'jobs': paginated_jobs})

# jobs page listing Experienced jobs

def exp_jobs_view(request):
    jobs = Job.objects.all().order_by('-job_created_at')  # Sort by latest date first
    current_date = timezone.now().date()

    for job in jobs:
        days_ago = (current_date - job.job_created_at.date()).days

        if days_ago == 0:
            job.days_ago_display = "Posted today"
        elif days_ago == 1:
            job.days_ago_display = "1 day ago"
        else:
            job.days_ago_display = f"{days_ago} days ago"

    # Pagination
    paginator = Paginator(jobs, 14)  # Show 10 jobs per page
    page = request.GET.get('page')

    try:
        paginated_jobs = paginator.page(page)
    except PageNotAnInteger:
        paginated_jobs = paginator.page(1)
    except EmptyPage:
        paginated_jobs = paginator.page(paginator.num_pages)

    return render(request, "portal_user_app/exp_jobs.html", {'jobs': paginated_jobs})
    
# job search box handling

def search_jobs_view(request):
    query = request.GET.get('query', '')
    results = Job.objects.filter(Q(job_heading__icontains=query))
    return render(request, "portal_user_app/fresher_jobs.html", {'jobs': results})

# about page

def about_view(request):
    return render(request, "portal_user_app/about.html")


''' Subscribing using otp section '''

# view handling subscriber registration

def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('subscriber_email')
        otp = request.POST.get('otp_code')
        action = request.POST.get('action')

        if action == 'requestOtp':
            if Subscriber.objects.filter(subscriber_email=email).exists():
                return JsonResponse({'error': 'Already Subscribed!'}, status=400)

            otp = generate_otp()
            if otp:
                send_otp_email(email, otp)

            request.session['otp'] = otp
            request.session['otp_created_at'] = make_aware(datetime.now()).isoformat()
            request.session['subscriber_email'] = email

            return JsonResponse({'success': True})

        elif action == 'verifyOtp':
            return verify_otp_view(request)

        elif action == 'resendOtp':
            if Subscriber.objects.filter(subscriber_email=email).exists():
                return JsonResponse({'error': 'Already Subscribed!'}, status=400)

            otp = generate_otp()
            if otp:
                send_otp_email(email, otp)

            request.session['otp'] = otp
            request.session['otp_created_at'] = make_aware(datetime.now()).isoformat()

            return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def verify_otp_view(request):
    if request.method == 'POST':
        otp = request.POST.get('otp_code')
        email = request.POST.get('subscriber_email')

        if not otp or not email:
            return JsonResponse({'error': 'OTP or email not provided'}, status=400)

        session_otp = request.session.get('otp')
        session_otp_created_at = request.session.get('otp_created_at')

        if session_otp and session_otp_created_at:
            otp_created_at = datetime.fromisoformat(session_otp_created_at)
            now = make_aware(datetime.now())

            if otp == session_otp and otp_created_at + timedelta(minutes=5) > now:
                request.session.pop('otp', None)
                request.session.pop('otp_created_at', None)
                request.session.pop('email', None)

                handle_successful_otp_verification(email)

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Invalid or expired OTP'}, status=400)
        else:
            return JsonResponse({'error': 'No OTP session found'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def handle_successful_otp_verification(email):
    Subscriber.objects.create(subscriber_email=email)
    send_subscription_email(email)

# view handling unsubscribing

def unsubscribe_view(request):
    if request.method == "GET":
        subscriber_email = request.GET.get('subscriber_email')
        if subscriber_email:
            # Decode the URL-encoded subscriber_email
            try:
                subscriber = Subscriber.objects.get(subscriber_email=subscriber_email)
                subscriber.delete()
                return render(request, "portal_user_app/emails/confirmation.html", {"subscriber": subscriber})
            except Subscriber.DoesNotExist:
                return HttpResponse("Subscriber not found.")
        else:
            return HttpResponse("Invalid unsubscribe link.")
    else:
        # If it's not a GET request, render the unsubscribe email page
        return render(request, "portal_user_app/emails/unsubscribe.html")
    

''' User Login/Registration Section '''

# User login

def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and isinstance(user, User):
            if user.is_active:
                login(request, user)
                return JsonResponse({'redirect': 'true'})
            else:
                return JsonResponse({'error': 'Your account is inactive, Contact Admin.'})
        
        return JsonResponse({'error': 'Invalid username or password.'})
    
    # Handle GET or other methods
    return JsonResponse({'error': 'false'})
        
# User registration

def user_register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        existing_email = User.objects.filter(email=email).first()
        if existing_email:
            return JsonResponse({'error': 'Email already registered. Please log in.'}, status=400)
        
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            return JsonResponse({'error': 'Username already registered. Please log in.'}, status=400)

        otp = generate_otp()
        send_otp_email(email, otp)

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        # Store OTP and its creation time in the session
        request.session['otp'] = otp
        request.session['otp_created_at'] = make_aware(datetime.now()).isoformat()
        request.session['user_id'] = user.id
        request.session['email'] = email

        return JsonResponse({'success': True})

    return render(request, "portal_user_app/index.html")

def user_register_verify_otp_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        otp = request.POST.get('otp')

        if action == 'verify_otp':
            is_valid = verify_otp(request, otp)
            if is_valid:
                send_account_created_email(request.session.get('email'))
                request.session.pop('email', None)
                return JsonResponse({'valid': True})
            return JsonResponse({'valid': False})

        elif action == 'resend_otp':
            email = request.session.get('email')
            if email:
                otp = generate_otp()
                send_otp_email(email, otp)
                request.session['otp'] = otp
                request.session['otp_created_at'] = make_aware(datetime.now()).isoformat()
                
                return JsonResponse({'resend': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def verify_otp(request, otp):
    session_otp = request.session.get('otp')
    session_otp_created_at = request.session.get('otp_created_at')

    if not otp or not session_otp or not session_otp_created_at:
        return False

    otp_created_at = datetime.fromisoformat(session_otp_created_at)
    now = make_aware(datetime.now())

    if otp == session_otp and otp_created_at + timedelta(minutes=5) > now:
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = User.objects.get(id=int(user_id))
                user.is_active = True
                user.save()

                # Clear the session data after successful activation
                request.session.pop('otp', None)
                request.session.pop('otp_created_at', None)
                request.session.pop('user_id', None)

                return True
            except User.DoesNotExist:
                return False
    return False

def user_forgot_pwd_view(request):
    if request.method == 'POST':
        user_email_or_username = request.POST.get('email')
        user = None

        if '@' in user_email_or_username:
            user = User.objects.filter(email=user_email_or_username).first()
        else:
            user = User.objects.filter(username=user_email_or_username).first()

        if user:
            temp_pwd = generate_password()
            user.set_password(temp_pwd)
            user.save()
            send_reset_email(user.email, temp_pwd)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'User not found'})

    return render(request, "portal_user_app/users/user_forgot_pwd.html")

@login_required
def user_pwd_reset(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        user = request.user

        if user.check_password(current_password):
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                return JsonResponse({'message': 'Password successfully updated!', 'redirect': '/user/dashboard/'})  # Adjust redirect URL as needed
            else:
                return JsonResponse({'error': 'New passwords do not match.'})
        else:
            return JsonResponse({'error': 'Current password is incorrect.'})

    return JsonResponse({'error': 'Invalid request method.'})

@login_required
def user_del_ac(request):
    user = request.user
    user.is_active = False
    user.save()

    return JsonResponse({'success': True, 'message': 'Account deleted successfully!'})

# User Logout

@login_required
def user_logout_view(request):
    logout(request)
    
    return redirect('portal_user_app:user_index')

# User Dashboard

@login_required(login_url='portal_user_app:user_index')
def user_dashboard_view(request):
    username = request.user
    return render(request, "portal_user_app/users/user_dashboard.html", {'username' : username})

# 404 Page

@login_required
def user_404_view(request):
    return render(request, "portal_user_app/users/404.html")