from django import forms
from django.core.exceptions import ValidationError

class DocumentForm(forms.Form):
    any_file = forms.FileField(label='Select a file')

    CONVERSION_CHOICES = [
        ('docx_to_pdf', 'DOCX to PDF'),
        ('pdf_to_docx', 'PDF to DOCX'),
        ('docx_to_jpg', 'DOCX to JPG'),
        ('docx_to_png', 'DOCX to PNG'),
        ('pdf_to_jpg', 'PDF to JPG'),
        ('pdf_to_png', 'PDF to PNG'),
    ]

    conversion_type = forms.ChoiceField(choices=CONVERSION_CHOICES, label='Select Conversion Type')

    def clean_any_file(self):
        file = self.cleaned_data.get('any_file', False)
        if file:
            files = ['.docx', '.pdf', '.jpg', '.png']
            if not (file.name.endswith(ext) for ext in files):
                raise ValidationError("Only '.docx', '.pdf', '.jpg', '.png' files are supported.")
            if file.size > 5*1024*1024:
                raise ValidationError("File size must be under 5MB.")
            return file
        else:
            raise ValidationError("Couldn't read the uploaded file.")
