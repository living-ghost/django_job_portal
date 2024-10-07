import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .forms import DocumentForm
from . convert import convert_docx_to_pdf

def converter_index_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            docx_file = request.FILES['docx_file']

            # Validate file type
            if not docx_file.name.endswith('.docx'):
                return render(request, 'portal_converter_app/converter_index.html', {
                    'form': form,
                    'error': 'Invalid file type. Please upload a .docx file.'
                })

            fs = FileSystemStorage()
            filename = fs.save(docx_file.name, docx_file)
            uploaded_file_path = fs.path(filename)

            pdf_file_path = None  # Initialize the variable

            try:
                # Convert DOCX to PDF using LibreOffice
                pdf_file_path = convert_docx_to_pdf(uploaded_file_path)

                # Serve the PDF file as a downloadable response
                with open(pdf_file_path, 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.splitext(filename)[0]}.pdf"'
                    return response

            except Exception as e:
                # Handle conversion errors
                return render(request, 'portal_converter_app/converter_index.html', {
                    'form': form,
                    'error': f'Error during conversion: {str(e)}'
                })

            finally:
                # Clean up temporary files
                if os.path.exists(uploaded_file_path):
                    try:
                        os.remove(uploaded_file_path)
                    except Exception as cleanup_error:
                        print(f"Error deleting uploaded file: {cleanup_error}")

                if pdf_file_path and os.path.exists(pdf_file_path):
                    try:
                        os.remove(pdf_file_path)
                    except Exception as cleanup_error:
                        print(f"Error deleting PDF file: {cleanup_error}")

    else:
        form = DocumentForm()
    return render(request, 'portal_converter_app/converter_index.html', {'form': form})