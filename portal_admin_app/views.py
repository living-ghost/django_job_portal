# ================================
#          Django Imports
# ================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import render, redirect

# ================================
#          Local App Imports
# ================================

from .models import Admin, Job
from portal_user_app.models import Subscriber
from .tasks import send_job_email

# ================================
#           Admin Section
# ================================

@login_required(login_url='portal_admin_app:admin_login')
def admin_index_view(request):
    """
    Render the admin index page.
    """
    return render(request, "portal_admin_app/index.html")

def admin_login_view(request):
    """
    Handle the admin login process.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request, username=username, password=password)
        if admin is not None and isinstance(admin, Admin):
            login(request, admin)
            return redirect('portal_admin_app:admin_index')
        
        messages.error(request, "Unable to login due to error")
        return redirect('portal_admin_app:admin_login')

    return render(request, "portal_admin_app/login.html")

@login_required
def admin_logout_view(request):
    """
    Handle the admin logout process.
    """
    logout(request)
    return redirect('portal_admin_app:admin_login')

@login_required
def admin_profile_view(request):
    """
    Render the admin profile page.
    """
    return render(request, "portal_admin_app/profile.html")

# ================================
#            Job Section
# ================================

@login_required
def jobs_view(request):
    """
    Render the jobs view page.
    """
    return render(request, "portal_admin_app/jobs.html")

@login_required
def jobs_add_view(request):
    """
    Handle the addition of new job postings and notify subscribers.
    """
    if request.method == 'POST':
        job_type = request.POST.get('job_type')
        job_heading = request.POST.get('job_heading')
        job_eligibility = request.POST.get('job_eligibility')
        job_description = request.POST.get('job_description')
        job_details = request.POST.get('job_details')

        if job_type in ['fresher', 'featured', 'experienced']:
            job = Job(
                job_type=job_type,
                job_heading=job_heading,
                job_eligibility=job_eligibility,
                job_description=job_description,
                job_details=job_details,
                job_added_by=request.user
            )
            job.save()

            # Fetch all subscribers
            subscribers = Subscriber.objects.all()
            for subscriber in subscribers:
                # Generate the unsubscribe URL
                unsubscribe_url = request.build_absolute_uri(
                    reverse('portal_user_app:user_unsubscribe') + '?' + urlencode({'subscriber_email': subscriber.subscriber_email})
                )

                # Call the Celery task
                send_job_email.delay(
                    subscriber_email=subscriber.subscriber_email,
                    job_heading=job_heading,
                    job_eligibility=job_eligibility,
                    job_created_at=job.job_created_at,
                    unsubscribe_url=unsubscribe_url,
                    site_url=request.build_absolute_uri('/')
                )

            return redirect('portal_admin_app:admin_job')

    return render(request, "portal_admin_app/add_job.html")

@login_required
def jobs_list_view(request):
    """
    Render a list of all jobs.
    """
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/view_job.html", {'jobs': jobs})

@login_required
def jobs_delete_view(request, job_id):
    """
    Handle the deletion of a job posting.
    """
    job = get_object_or_404(Job, id=job_id)
    job.delete()
    return redirect('portal_admin_app:admin_list_job')

@login_required
def jobs_edit_view(request, job_id):
    """
    Handle the editing of a job posting.
    """
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        job_type = request.POST.get('job_type')
        job_heading = request.POST.get('job_heading')
        job_eligibility = request.POST.get('job_eligibility')
        job_description = request.POST.get('job_description')
        job_details = request.POST.get('job_details')

        if job_type in ['fresher', 'featured', 'experienced']:
            job.job_type = job_type
            job.job_heading = job_heading
            job.job_eligibility = job_eligibility
            job.job_description = job_description
            job.job_details = job_details
            
            job.save()

            return redirect('portal_admin_app:admin_list_job')

    return render(request, "portal_admin_app/edit_job.html", {'job': job})

@login_required
def fresher_list_view(request):
    """
    Render a list of fresher jobs.
    """
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/fresher.html", {'jobs': jobs})

@login_required
def exp_list_view(request):
    """
    Render a list of experienced jobs.
    """
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/exp.html", {'jobs': jobs})

@login_required
def feat_list_view(request):
    """
    Render a list of featured jobs.
    """
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/feature.html", {'jobs': jobs})

@login_required
def del_list_view(request):
    """
    Render a list of deleted jobs.
    """
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/deleted.html", {'jobs': jobs})

# ================================
#           User Section
# ================================

@login_required
def users_view(request):
    """
    Render the users view page.
    """
    return render(request, "portal_admin_app/users.html")

@login_required
def users_list_view(request):
    """
    Render a list of all users (subscribers).
    """
    users = Subscriber.objects.all()
    return render(request, "portal_admin_app/view_user.html", {'users': users})