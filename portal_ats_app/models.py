from django.db import models

# Create your models here.

class Resume(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resume_file = models.FileField(upload_to='resumes/')
    
    def __str__(self):
        return f"Resume {self.id} uploaded at {self.uploaded_at}"