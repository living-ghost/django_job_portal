from django.db import models
from portal_user_app.models import User

# Create your models here

class ConvertedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    original_file = models.FileField(upload_to='portal_converter_app/files/uploads/')
    converted_file = models.FileField(upload_to='portal_converter_app/files/converted/')
    file_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)