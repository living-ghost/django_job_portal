from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.urls import reverse
from urllib.parse import urlencode
from datetime import datetime
from . models import Admin, Job
from portal_user_app.models import Subscriber


# Create your views here.


# Admin Section

@login_required(login_url='portal_admin_app:admin_login')
def admin_index_view(request):
    return render(request, "portal_admin_app/index.html")


def admin_login_view(request):
    """
    Handles Admin login.
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
    logout(request)
    return redirect('portal_admin_app:admin_login')


@login_required
def admin_profile_view(request):
    return render(request, "portal_admin_app/profile.html")


# Job Section

@login_required
def jobs_view(request):
    return render(request, "portal_admin_app/jobs.html")


@login_required
def jobs_add_view(request):
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
                subject = f'Freshers Park: {job_heading} Hiring'

                # Generate the unsubscribe URL
                unsubscribe_url = request.build_absolute_uri(
                    reverse('portal_user_app:user_unsubscribe') + '?' + urlencode({'subscriber_email': subscriber.subscriber_email})
                )

                # Render the HTML content with the job details and unsubscribe URL
                html_content = render_to_string('portal_user_app/emails/post_updates.html', {
                    'job': job,
                    'unsubscribe_url': unsubscribe_url,
                    'site_url': request.build_absolute_uri('/'),
                })

                # Strip the HTML tags for plain text content
                text_content = strip_tags(html_content)

                # Create the email
                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[subscriber.subscriber_email]
                )
                email.attach_alternative(html_content, "text/html")

                try:
                    # Send the email
                    email.send(fail_silently=False)
                except Exception as e:
                    # Log or handle the exception
                    print(f"Error sending email to {subscriber.subscriber_email}: {e}")

            return redirect('portal_admin_app:admin_job')

    return render(request, "portal_admin_app/add_job.html")


@login_required
def jobs_list_view(request):
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/view_job.html", {'jobs':jobs})


@login_required
def jobs_delete_view(request, job_id):

    job_id = get_object_or_404(Job, id=job_id)

    job_id.delete()

    return redirect('portal_admin_app:admin_list_job')


@login_required
def jobs_edit_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        job_type = request.POST.get('job_type')
        job_heading = request.POST.get('job_heading')
        job_eligibility = request.POST.get('job_eligibility')
        job_description = request.POST.get('job_description')
        job_details = request.POST.get('job_details')

        if job_type in ['fresher', 'featured', 'experienced']:
            job.job_type=job_type
            job.job_heading=job_heading
            job.job_eligibility=job_eligibility
            job.job_description=job_description
            job.job_details=job_details
            
            job.save()

            return redirect('portal_admin_app:admin_list_job')

    return render(request, "portal_admin_app/edit_job.html", {'job':job})


@login_required
def fresher_list_view(request):
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/fresher.html", {'jobs':jobs})


@login_required
def exp_list_view(request):
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/exp.html", {'jobs':jobs})


@login_required
def feat_list_view(request):
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/feature.html", {'jobs':jobs})


@login_required
def del_list_view(request):
    jobs = Job.objects.all()
    return render(request, "portal_admin_app/deleted.html", {'jobs':jobs})


# User Section

@login_required
def users_view(request):
    return render(request, "portal_admin_app/users.html")


@login_required
def users_list_view(request):
    users = Subscriber.objects.all()
    return render(request, "portal_admin_app/view_user.html", {'users':users})