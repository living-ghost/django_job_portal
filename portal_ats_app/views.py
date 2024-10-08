from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ResumeUploadForm
from .models import Resume
import docx
from pdfminer.high_level import extract_text

def ats_home_view(request):
    return render(request, 'portal_ats_app/ats_index.html')

def ats_upload_view(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            return redirect('portal_ats_app:ats_check', resume_id=resume.id)
    else:
        form = ResumeUploadForm()
    return render(request, 'portal_ats_app/ats_upload.html', {'form': form})

def ats_check_view(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    file_path = resume.resume_file.path
    text = ""

    if file_path.endswith('.pdf'):
        text = extract_text(file_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
    else:
        text = "Unsupported file format."

    # Implement your ATS checking logic here
    # For demonstration, let's assume we check for keywords
    keywords = ['Python', 'Django', 'REST', 'API', 'SQL']
    found_keywords = [word for word in keywords if word.lower() in text.lower()]
    missing_keywords = [word for word in keywords if word.lower() not in text.lower()]
    score = len(found_keywords) / len(keywords) * 100

    context = {
        'resume': resume,
        'found_keywords': found_keywords,
        'missing_keywords': missing_keywords,
        'score': score,
    }

    return render(request, 'portal_ats_app/ats_result.html', context)