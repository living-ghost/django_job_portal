# converter/forms.py

from django import forms
from django.core.exceptions import ValidationError

class DocumentForm(forms.Form):
    docx_file = forms.FileField(label='Select a DOCX file')

    def clean_docx_file(self):
        file = self.cleaned_data.get('docx_file', False)
        if file:
            if not file.name.endswith('.docx'):
                raise ValidationError("Only .docx files are supported.")
            if file.size > 5*1024*1024:
                raise ValidationError("File size must be under 5MB.")
            return file
        else:
            raise ValidationError("Couldn't read the uploaded file.")
