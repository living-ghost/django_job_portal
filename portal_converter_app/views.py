import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .forms import DocumentForm
from .convert import (convert_docx_to_pdf, convert_docx_to_jpg, convert_docx_to_png,
                      convert_pdf_to_docx, convert_pdf_to_jpg, convert_pdf_to_png)
import mimetypes
from django.http import HttpResponse

def converter_index_view(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            any_file = request.FILES['any_file']
            conversion_type = request.POST.get('conversion_type')

            # Validate file type
            files = ['.docx', '.pdf', '.png', '.jpg']
            if not any(any_file.name.endswith(ext) for ext in files):
                return render(request, 'portal_converter_app/converter_index.html', {
                    'form': form,
                    'error': 'Invalid file type. Please upload a file with one of the following extensions: .docx, .pdf, .png, .jpg.'
                })

            fs = FileSystemStorage()
            filename = fs.save(any_file.name, any_file)
            uploaded_file_path = fs.path(filename)

            output_file_path = None  # Initialize the variable for the converted file path

            try:
                # Determine conversion based on file type and conversion type
                if any_file.name.endswith('.docx'):
                    if conversion_type == 'docx_to_pdf':
                        output_file_path = convert_docx_to_pdf(uploaded_file_path)
                    elif conversion_type == 'docx_to_jpg':
                        output_file_path = convert_docx_to_jpg(uploaded_file_path)
                    elif conversion_type == 'docx_to_png':
                        output_file_path = convert_docx_to_png(uploaded_file_path)

                elif any_file.name.endswith('.pdf'):
                    if conversion_type == 'pdf_to_docx':
                        output_file_path = convert_pdf_to_docx(uploaded_file_path)
                    elif conversion_type == 'pdf_to_jpg':
                        output_file_path = convert_pdf_to_jpg(uploaded_file_path)
                    elif conversion_type == 'pdf_to_png':
                        output_file_path = convert_pdf_to_png(uploaded_file_path)

                # Serve the converted file as a downloadable response
                if output_file_path and os.path.exists(output_file_path):
                    try:
                        with open(output_file_path, 'rb') as output_file:
                            # Determine content type using mimetypes
                            content_type, _ = mimetypes.guess_type(output_file_path)
                            content_type = content_type or 'application/octet-stream'  # Fallback if type can't be guessed
                            
                            response = HttpResponse(output_file.read(), content_type=content_type)
                            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_file_path)}"'
                            return response

                    except Exception as e:
                        # Handle exceptions, log the error, and return an appropriate response
                        return HttpResponse(f"Error serving file: {str(e)}", content_type='text/plain')
                else:
                    return HttpResponse("File not found.", content_type='text/plain')

            except Exception as e:
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
                # You can add additional cleanup for the output file if necessary

    else:
        form = DocumentForm()
    return render(request, 'portal_converter_app/converter_index.html', {'form': form})