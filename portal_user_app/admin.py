# ================================
#          Django Imports
# ================================

from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from urllib.parse import urlencode

# ================================
#          App Imports
# ================================

from portal_admin_app.models import Admin, Job
from .models import Subscriber

# ================================
#          Admin Models
# ================================

class JobAdmin(admin.ModelAdmin):
    """
    Admin interface for the Job model, including custom save behavior.
    """
    list_display = ('job_heading', 'job_created_at')
    search_fields = ('job_heading',)

    def save_model(self, request, obj, form, change):
        """
        Save the Job model instance and notify subscribers if the job is newly created.

        Args:
            request (HttpRequest): The request object.
            obj (Job): The Job model instance.
            form (ModelForm): The form used to create/update the Job instance.
            change (bool): True if the object is being changed, False if being created.

        """
        # Check if the job is being created (not updated)
        if not change:
            # Save the new job instance
            super().save_model(request, obj, form, change)

            # Notify all subscribers about the new job posting
            subscribers = Subscriber.objects.all()
            for subscriber in subscribers:
                subject = 'Freshers Park: ' + obj.job_heading + ' Hiring'

                # Generate the unsubscribe URL
                unsubscribe_url = request.build_absolute_uri(
                    reverse('unsubscribe') + '?' + urlencode({'subscriber_email': subscriber.subscriber_email})
                )
                # Render HTML content with the unsubscribe URL
                html_content = render_to_string('emails/post_updates.html', {'job': obj, 'unsubscribe_url': unsubscribe_url})
                # Strip the HTML tags for plain text content
                text_content = strip_tags(html_content)

                # Create the email
                email = EmailMultiAlternatives(
                    subject, text_content, 'akhiiltkaniiparampiil@gmail.com', [subscriber.subscriber_email]
                )
                email.attach_alternative(html_content, "text/html")

                try:
                    # Send the email
                    email.send()
                except Exception as e:
                    # Log or handle the exception
                    print(f"Error sending email to {subscriber.subscriber_email}: {e}")

        else:
            # Save the job instance if it is being updated
            super().save_model(request, obj, form, change)

# Register the admin classes with the Django admin site
admin.site.register(Job, JobAdmin)
admin.site.register(Subscriber)
admin.site.register(Admin)