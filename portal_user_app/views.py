# ================================
#          Standard Library Imports
# ================================

from datetime import datetime, timedelta

# ================================
#          Third-Party Imports
# ================================

from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# ================================
#          Django App Imports
# ================================

from .models import Subscriber, User, ContactUs
from portal_admin_app.models import Job
from .utils import (
    generate_otp, 
    send_account_created_email, 
    send_otp_email,
    generate_password, 
    send_reset_email,
    send_contactus_email_to_admin
)
from .verify import verify_otp, handle_successful_otp_verification

# ================================
#          Doclib Imports
# ================================

# Add your doclib imports here if needed
# from doclib import SomeDocLibModule

# ================================
#          Home Page View
# ================================

def index_view(request):
    """
    Render the home page with featured jobs sorted by the latest date first.
    """
    featureds = Job.objects.all().order_by('-job_created_at')  # Fetch and sort jobs by creation date
    current_datetime = timezone.now()  # Get current datetime

    for feature in featureds:
        time_diff = current_datetime - feature.job_created_at

        if time_diff < timedelta(days=1):
            feature.days_ago_display = "Posted today"
        elif time_diff < timedelta(days=2):
            feature.days_ago_display = "1 day ago"
        else:
            feature.days_ago_display = f"{time_diff.days} days ago"

    return render(request, "portal_user_app/index.html", {'featureds': featureds})

# ================================
#          Fresher Job Page View
# ================================

def fresher_jobs_view(request):
    """
    Render the fresher job page with jobs sorted by the latest date, with pagination.
    """
    jobs = Job.objects.all().order_by('-job_created_at')  # Fetch and sort jobs by creation date
    current_datetime = timezone.now()  # Get current datetime

    for job in jobs:
        time_diff = current_datetime - job.job_created_at

        if time_diff < timedelta(days=1):
            job.days_ago_display = "Posted today"
        elif time_diff < timedelta(days=2):
            job.days_ago_display = "1 day ago"
        else:
            job.days_ago_display = f"{time_diff.days} days ago"

    # Pagination
    paginator = Paginator(jobs, 14)  # Show 14 jobs per page
    page = request.GET.get('page')

    try:
        paginated_jobs = paginator.page(page)
    except PageNotAnInteger:
        paginated_jobs = paginator.page(1)
    except EmptyPage:
        paginated_jobs = paginator.page(paginator.num_pages)

    return render(request, "portal_user_app/fresher_jobs.html", {'jobs': paginated_jobs})

# ================================
#          Experienced Job Page View
# ================================

def exp_jobs_view(request):
    """
    Render the experienced job page with jobs sorted by the latest date, with pagination.
    """
    jobs = Job.objects.all().order_by('-job_created_at')  # Fetch and sort jobs by creation date
    current_datetime = timezone.now()  # Get current datetime

    for job in jobs:
        time_diff = current_datetime - job.job_created_at

        if time_diff < timedelta(days=1):
            job.days_ago_display = "Posted today"
        elif time_diff < timedelta(days=2):
            job.days_ago_display = "1 day ago"
        else:
            job.days_ago_display = f"{time_diff.days} days ago"

    # Pagination
    paginator = Paginator(jobs, 14)  # Show 14 jobs per page
    page = request.GET.get('page')

    try:
        paginated_jobs = paginator.page(page)
    except PageNotAnInteger:
        paginated_jobs = paginator.page(1)
    except EmptyPage:
        paginated_jobs = paginator.page(paginator.num_pages)

    return render(request, "portal_user_app/exp_jobs.html", {'jobs': paginated_jobs})

# ================================
#          Fresher Job Search
# ================================

def search_jobs_view(request):
    """
    Handle job search requests for both fresher and experienced jobs.
    Use the 'type' parameter to distinguish between fresher and experienced job searches.
    """
    query = request.GET.get('query', '')
    job_type = request.GET.get('type', 'fresher')  # Default to 'fresher' if no type is provided
    
    if job_type == 'experienced':
        # Search experienced jobs
        results = Job.objects.filter(Q(job_heading__icontains=query) & Q(job_type='experienced'))
        template = 'portal_user_app/exp_jobs.html'
    else:
        # Search fresher jobs
        results = Job.objects.filter(Q(job_heading__icontains=query) & Q(job_type='fresher'))
        template = 'portal_user_app/fresher_jobs.html'
    
    return render(request, template, {'jobs': results})

# ================================
#          About Page View
# ================================

def about_view(request):
    """
    Render the about page.
    """
    return render(request, "portal_user_app/about.html")

# ================================
#          Contact Us View
# ================================

def contact_us_view(request):
    """
    Contact us form to collect data from user and trigger email to Admin.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        project_tech = request.POST.get('project_tech')
        description = request.POST.get('description')

        send_contactus_email_to_admin(name, email, project_tech, description)

        messages.success(request, "We received your request, will revert shortly")

        contact_us = ContactUs(
            name=name,
            email=email,
            project_tech=project_tech,
            description=description
        )
        contact_us.save()

        return redirect('portal_user_app:user_index')

# ================================
#          Subscriber Registration
# ================================

def subscribe_view(request):
    """
    Handle subscription requests including OTP verification and resending.
    """
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

# ================================
#          Verify OTP View
# ================================

def verify_otp_view(request):
    """
    Verify the OTP submitted by the user.
    """
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

# ================================
#          Subscriber Unsubscribing
# ================================

def unsubscribe_view(request):
    """
    Handle unsubscribe requests by deleting the subscriber.
    """
    if request.method == "GET":
        subscriber_email = request.GET.get('subscriber_email')
        if subscriber_email:
            try:
                subscriber = Subscriber.objects.get(subscriber_email=subscriber_email)
                subscriber.delete()
                return render(request, "portal_user_app/emails/confirmation.html", {"subscriber": subscriber})
            except Subscriber.DoesNotExist:
                return HttpResponse("Subscriber not found.")
        else:
            return HttpResponse("Invalid unsubscribe link.")
    else:
        return render(request, "portal_user_app/emails/unsubscribe.html")

# ================================
#          User Login
# ================================

def user_login_view(request):
    """
    Handle user login requests.
    """
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
    
    return JsonResponse({'error': 'false'})

# ================================
#          User Register
# ================================

def user_register_view(request):
    """
    Handle user registration including sending OTP for verification.
    """
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

# ================================
#          User Register Verify OTP
# ================================

def user_register_verify_otp_view(request):
    """
    Handle OTP verification for user registration.
    """
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

# ================================
#          User Forgot Password
# ================================

def user_forgot_pwd_view(request):
    """
    Handle forgot password requests by sending a reset password email.
    """
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

# ================================
#          User Password Reset
# ================================

@login_required
def user_pwd_reset_view(request):
    """
    Handle password reset for logged-in users.
    """
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
                return JsonResponse({'message': 'Password successfully updated!', 'redirect': '/user/dashboard/'})
            else:
                return JsonResponse({'error': 'New passwords do not match.'})
        else:
            return JsonResponse({'error': 'Current password is incorrect.'})

    return JsonResponse({'error': 'Invalid request method.'})

# ================================
#          User Account Deletion
# ================================

@login_required
def user_del_ac_view(request):
    """
    Handle user account deletion.
    """
    user = request.user
    user.is_active = False
    user.save()

    return JsonResponse({'success': True, 'message': 'Account deleted successfully!'})

# ================================
#          User Logout
# ================================

@login_required
def user_logout_view(request):
    """
    Log out the user and redirect to the home page.
    """
    logout(request)
    
    return redirect('portal_user_app:user_index')

# ================================
#          User Dashboard
# ================================

@login_required(login_url='portal_user_app:user_index')
def user_dashboard_view(request):
    """
    Render the user dashboard page.
    """
    username = request.user
    return render(request, "portal_user_app/users/user_dashboard.html", {'username': username})

# ================================
#          404 Page
# ================================

@login_required
def user_404_view(request):
    """
    Render the 404 error page for users.
    """
    return render(request, "portal_user_app/users/404.html")


# ================================
#          Razorpay
# ================================

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def user_razorpay_view(request):
    currency = 'INR'
    amount = 10000  # Rs. 100

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    # callback_url = 'user_payment/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    # context['callback_url'] = callback_url

    return render(request, 'portal_user_app/razorpay.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def user_payment_view(request):

    # only accept POST request.
    if request.method == "POST":
        try:
          
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 10000  # Rs. 100
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return redirect('portal_user_app:user_index')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()