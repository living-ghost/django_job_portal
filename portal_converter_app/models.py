# ================================
#       Models for File Conversion
# ================================

from django.db import models
from portal_user_app.models import User

class ConvertedFile(models.Model):
    """
    Model to store information about files that have been converted.

    Attributes:
    - user: The user who uploaded the file (ForeignKey to User).
    - original_file: The original file that was uploaded (FileField).
    - converted_file: The file after conversion (FileField).
    - file_type: The type of the converted file (e.g., pdf, docx) (CharField).
    - uploaded_at: Timestamp when the file was uploaded (DateTimeField).
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    original_file = models.FileField(upload_to='portal_converter_app/files/uploads/')
    converted_file = models.FileField(upload_to='portal_converter_app/files/converted/')
    file_type = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File conversion record for {self.user.username} - {self.file_type}"