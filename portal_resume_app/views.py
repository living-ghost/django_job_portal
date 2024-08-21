from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from io import BytesIO
from django.core.files.base import ContentFile
from . models import *
from . utils import get_user_data
import imgkit
import pdfkit
import json

#

@login_required(login_url='portal_user_app:user_login')
def resume_index_view(request):
    if request.method == 'POST':
        response_data = {}
        try:
            if 'name' in request.POST:
                name = request.POST.get('name')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                address = request.POST.get('address')
                user = get_object_or_404(User, id=request.user.id)
                PersonalInfo.objects.update_or_create(user=user, defaults={
                    'name': name, 'email': email, 'phone': phone, 'address': address
                })
                response_data['message'] = 'Personal Information updated successfully!'
            
            elif 'degree1' in request.POST:
                degree = request.POST.get('degree1')
                college = request.POST.get('college1')
                year = request.POST.get('year1')
                cgpa = request.POST.get('cgpa1')
                user = get_object_or_404(User, id=request.user.id)
                Education.objects.create(user=user, degree=degree, college=college, year=year, cgpa=cgpa)

                response_data['message'] = 'Education Information updated successfully!'

            elif 'role1' in request.POST:
                role = request.POST.get('role1')
                company = request.POST.get('company1')
                year = request.POST.get('year1')
                location = request.POST.get('location1')
                description = request.POST.get('description1')
                user = get_object_or_404(User, id=request.user.id)
                Experience.objects.create(user=user, role=role, company=company, year=year)

                response_data['message'] = 'Experience Information updated successfully!'
            
            elif 'language1' in request.POST:
                language = request.POST.get('language1')
                proficiency = request.POST.get('proficiency1')
                user = get_object_or_404(User, id=request.user.id)
                Language.objects.create(user=user, language=language, proficiency=proficiency)

                response_data['message'] = 'Language Information updated successfully!'
            
            elif 'project1' in request.POST:
                project_title = request.POST.get('project1')
                description = request.POST.get('project_description1')
                year = request.POST.get('project_year1')
                user = get_object_or_404(User, id=request.user.id)
                Project.objects.create(user=user, title=project_title, description=description, year=year)

                response_data['message'] = 'Project Information updated successfully!'
            
            elif 'certificate1' in request.POST:
                certificate = request.POST.get('certificate1')
                year = request.POST.get('certificateyear1')
                user = get_object_or_404(User, id=request.user.id)
                Certificate.objects.create(user=user, certificate=certificate, year=year)

                response_data['message'] = 'Certificate Information updated successfully!'
            
            elif 'skill1' in request.POST:
                skill = request.POST.get('skill1')
                proficiency = request.POST.get('proficiency_skill1')
                user = get_object_or_404(User, id=request.user.id)
                Skill.objects.create(user=user, skill=skill, proficiency=proficiency)

                response_data['message'] = 'Skill Information updated successfully!'

            elif 'hobbies1' in request.POST:
                hobbie = request.POST.get('hobbies1')
                user = get_object_or_404(User, id=request.user.id)
                Hobbie.objects.create(user=user, hobbie=hobbie)

                response_data['message'] = 'Hobbie Information updated successfully!'
            
            elif 'description2' in request.POST:
                description2 = request.POST.get('description2')
                user = get_object_or_404(User, id=request.user.id)
                Summary.objects.update_or_create(user=user, defaults={
                    'description': description2,
                })

                response_data['message'] = 'Summary Information updated successfully!'

            return JsonResponse({'success': True, 'message': response_data.get('message', 'Data saved successfully!')})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    # Fetch all the data to render the template
    personal_data, education_data, experience_data, language_data, project_data, certificate_data, hobbie_data, skill_data, summary_data = get_user_data(request.user)
    
    return render(request, "portal_resume_app/resume_index.html", {
         'personal_data': personal_data,
         'education_data': education_data,
         'experience_data': experience_data,
         'language_data': language_data,
         'project_data': project_data,
         'certificate_data': certificate_data,
         'hobbie_data': hobbie_data,
         'skill_data': skill_data,
         'summary_data': summary_data
    })

#

def resume_list_view(request):
     resumes = Resume.objects.filter(user=request.user)

     return render(request, "portal_resume_app/resume_list.html", {'resumes' : resumes})

#

def resume_download_view(request, resume_id):
    try:
        # Retrieve the resume object
        resume_download = Resume.objects.get(id=resume_id)

        # Configure pdfkit with path to wkhtmltopdf executable
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=settings.PDFKIT_CONFIG['wkhtmltopdf'])

        # Options to set paper size and other settings
        options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'zoom': '1.05',
            'print-media-type': '',
            'orientation': 'Portrait',
            'enable-local-file-access': '',
            'dpi': 300,
            'image-dpi': 300,
            'image-quality': 100,
        }

        # Convert HTML to PDF with the specified options
        pdf = pdfkit.from_string(resume_download.html_content, False, configuration=pdfkit_config, options=options)

        # Create HTTP response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
        return response

    except Resume.DoesNotExist:
        return HttpResponse("Resume not found.", status=404)

#
    
def save_resume_image(user, resume, html_content):
    # Configure imgkit with path to wkhtmltoimage executable
    imgkit_config = imgkit.config(wkhtmltoimage=settings.IMGKIT_CONFIG['wkhtmltoimage'])
    img_options = {
        'format': 'png',
        'quality': '100',
        'crop-w': '2480',  # Width in pixels (A4 size at 300 DPI)
        'crop-h': '3508',  # Height in pixels (A4 size at 300 DPI)
        'zoom': '1.50',
    }

    try:
        # Convert HTML to image
        image_data = imgkit.from_string(html_content, False, config=imgkit_config, options=img_options)

        # Save image to a file-like object
        image_file = BytesIO(image_data)
        image_file.seek(0)

        # Create a ContentFile for Django
        image_content = ContentFile(image_file.read(), name=f'{resume.name}.png')

        # Save the image to the Resume instance
        resume.image.save(f'{user}_{resume.name}.png', image_content, save=True)

    except Exception as e:
        print(f"Error saving image: {e}")

#

def save_resume_pdf(user, resume, html_content):
    # Convert SafeString to a regular string if needed
    if hasattr(html_content, 'unsafe'):
        html_content_str = str(html_content)
    else:
        html_content_str = html_content

    # Configure pdfkit with path to wkhtmltopdf executable
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=settings.PDFKIT_CONFIG['wkhtmltopdf'])
    pdf_options = {
        'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'zoom': '1.05',
            'print-media-type': '',
            'orientation': 'Portrait',
            'enable-local-file-access': '',
            'dpi': 300,
            'image-dpi': 300,
            'image-quality': 100,
        }

    try:
        # Convert HTML to PDF
        pdf_data = pdfkit.from_string(html_content_str, False, configuration=pdfkit_config, options=pdf_options)

        # Save PDF to a file-like object
        pdf_file = BytesIO(pdf_data)

        # Create a ContentFile for Django
        pdf_content = ContentFile(pdf_file.read(), name=f'{resume.name}.pdf')

        # Save the PDF to the Resume instance
        resume.pdf_file.save(f'{user}_{resume.name}.pdf', pdf_content, save=True)

    except Exception as e:
        print(f"Error saving PDF: {e}")

#

def resume_save_view(request):
    # Fetch user and other data
    user = request.user
    personal_data, education_data, experience_data, language_data, project_data, certificate_data, hobbie_data, skill_data, summary_data = get_user_data(user)

    old_resumes = Resume.objects.filter(user=user)
    if old_resumes:
        for resume in old_resumes:
            resume.delete()

    # List of all available template names
    templates = [
        'template1.html',
        'template2.html',
    ]

    # Loop through each template, render HTML content, and save to the database
    for template_name in templates:
        # Prepare the context for rendering the template
        context = {
            'personal_data': personal_data,
            'education_data': education_data,
            'experience_data': experience_data,
            'language_data': language_data,
            'project_data': project_data,
            'certificate_data': certificate_data,
            'hobbie_data': hobbie_data,
            'skill_data': skill_data,
            'summary_data': summary_data
        }

        # Render the HTML content with the selected template
        html_content = render_to_string(f'portal_resume_app/resumes_list/{template_name}', context)

        # Create a Resume instance and save to the database
        resume = Resume.objects.create(
            user=user,
            name=f'{template_name}',  # You can customize the title as needed
            html_content=html_content
        )

        # Save the PNG image and PDF
        save_resume_image(user, resume, html_content)
        save_resume_pdf(user, resume, html_content)

    return redirect('portal_resume_app:resume_list')

#

def resume_display_view(request, resume_id):
    resume = Resume.objects.get(id=resume_id)
    return render(request, "portal_resume_app/resume_view.html", {'resume' : resume})

#

# Resume Fields Deleting Section

#

@login_required
def delete_hobbie_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            hobbie_id = data.get('hobbie_id')
            hobbie = Hobbie.objects.get(id=hobbie_id)
            hobbie.delete()
            return JsonResponse({'success': True})
        except Hobbie.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Hobby does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

#

@login_required
def delete_skill_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            skill_id = data.get('skill_id')
            skill = Skill.objects.get(id=skill_id)
            skill.delete()
            return JsonResponse({'success': True})
        except Skill.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Skill does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

#

@login_required
def delete_certi_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            certificate_id = data.get('certificate_id')
            certificate = Certificate.objects.get(id=certificate_id)
            certificate.delete()
            return JsonResponse({'success': True})
        except Certificate.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Certificate does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

#

@login_required
def delete_pro_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('project_id')
            project = Project.objects.get(id=project_id)
            project.delete()
            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

#

@login_required
def delete_lang_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            language_id = data.get('language_id')
            language = Language.objects.get(id=language_id)
            language.delete()
            return JsonResponse({'success': True})
        except Language.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Language does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

#

@login_required
def delete_exp_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            experience_id = data.get('experience_id')
            experience = Experience.objects.get(id=experience_id)
            experience.delete()
            return JsonResponse({'success': True})
        except Experience.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Experience does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

#

@login_required
def delete_edu_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            education_id = data.get('education_id')
            education = Education.objects.get(id=education_id)
            education.delete()
            return JsonResponse({'success': True})
        except Education.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Education does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# For TEST

def resume_test_view(request):
    personal_data, education_data, experience_data, language_data, project_data, certificate_data, hobbie_data, skill_data, summary_data = get_user_data(request.user)

    return render(request, "portal_resume_app/resumes_list/template2.html", {
         'personal_data': personal_data,
         'education_data': education_data,
         'experience_data': experience_data,
         'language_data': language_data,
         'project_data': project_data,
         'certificate_data': certificate_data,
         'hobbie_data': hobbie_data,
         'skill_data': skill_data,
         'summary_data': summary_data
    })