from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from io import BytesIO
from docx import Document
from PIL import Image, ImageDraw, ImageFont
from .models import ConvertedFile
from django.contrib.auth.decorators import login_required
from . convert import convert_to_pdf_from_text, convert_to_docx_from_text
from . extract import extract_text_from_docx, extract_text_from_pdf
import fitz  # PyMuPDF for PDF text extraction


@login_required
def converter_index_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        format = request.POST.get('format')
        user = request.user  # Get the currently logged-in user

        if file:
            # Handle file conversion based on the selected format
            if format == 'pdf':
                response = convert_to_file(user, file, 'pdf')
            elif format == 'docx':
                response = convert_to_file(user, file, 'docx')
            elif format in ['jpg', 'png']:
                response = convert_to_image(user, file, format)
            else:
                response = HttpResponse("Unsupported format", status=400)
            
            return response
        else:
            return HttpResponse("No file uploaded", status=400)
        
    return render(request, "portal_converter_app/converter_index.html")

# Downloading Converted file

def save_converted_file(user, original_file, converted_file_content, file_type):
    converted_file = ConvertedFile(
        user=user,
        original_file=original_file,
        converted_file=ContentFile(converted_file_content, name=f'converted.{file_type}'),
        file_type=file_type
    )
    converted_file.save()
    return converted_file

#

# File Converter Section PDF/DOCX

def convert_to_file(user, file, format):
    try:
        if format == 'pdf':
            # If converting to PDF, extract text from DOCX or convert a text file directly
            if file.name.lower().endswith('.docx'):
                file.seek(0)
                file_content = extract_text_from_docx(file)
            elif file.name.lower().endswith('.txt'):
                file_content = file.read().decode('utf-8')
            else:
                return HttpResponse("Unsupported file type for PDF conversion.", status=400)
            
            converted_file_content = convert_to_pdf_from_text(file_content)
            file_type = 'pdf'

        elif format == 'docx':
            # If converting to DOCX, extract text from PDF or convert a text file directly
            if file.name.lower().endswith('.pdf'):
                file.seek(0)
                file_content = extract_text_from_pdf(file)
            elif file.name.lower().endswith('.txt'):
                file_content = file.read().decode('utf-8')
            else:
                return HttpResponse("Unsupported file type for DOCX conversion.", status=400)
            
            converted_file_content = convert_to_docx_from_text(file_content)
            file_type = 'docx'
        
        else:
            return HttpResponse("Unsupported format", status=400)

        save_converted_file(user, file, converted_file_content, file_type)

        response = HttpResponse(converted_file_content, content_type=f'application/{file_type}')
        response['Content-Disposition'] = f'attachment; filename="converted.{file_type}"'
        return response

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

# Image Converter Section JPG/PNG

# A4 dimensions in inches and pixels for 300 DPI
A4_WIDTH_INCHES = 8.27
A4_HEIGHT_INCHES = 11.69
DPI = 300
A4_WIDTH_PIXELS = int(A4_WIDTH_INCHES * DPI)
A4_HEIGHT_PIXELS = int(A4_HEIGHT_INCHES * DPI)

# Define padding in pixels
PADDING_TOP = 150
PADDING_BOTTOM = 150
PADDING_LEFT = 150
PADDING_RIGHT = 150

# Define padding in pixels
IMG_PADDING_TOP = 50
IMG_PADDING_BOTTOM = 50
IMG_PADDING_LEFT = 50
IMG_PADDING_RIGHT = 50

# Define paragraph spacing in pixels
PARAGRAPH_SPACING = 50
HEADING_SPACING = 100  # Extra space after headings

#

def convert_to_image(user, file, format):
    try:
        buffer = BytesIO()
        
        format = format.upper()
        if format == 'JPG':
            format = 'JPEG'
        
        # Define font styles (you may need to provide the path to a TTF file)
        try:
            heading_font = ImageFont.truetype("arialbd.ttf", 100)
            subheading_font = ImageFont.truetype("arialbd.ttf", 70)
            body_font = ImageFont.truetype("arial.ttf", 50)
        except IOError:
            heading_font = ImageFont.load_default()
            subheading_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        # Calculate content area dimensions accounting for padding
        content_width = A4_WIDTH_PIXELS - PADDING_LEFT - PADDING_RIGHT
        content_height = A4_HEIGHT_PIXELS - PADDING_TOP - PADDING_BOTTOM

        def draw_text(draw, text, position, font, max_width):
            # Split text into lines that fit within the width
            lines = []
            words = text.split(' ')
            line = words[0]
            for word in words[1:]:
                test_line = f"{line} {word}"
                bbox = draw.textbbox((position[0], position[1]), test_line, font=font)
                width = bbox[2] - bbox[0]
                if width <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            lines.append(line)
            y = position[1]
            for line in lines:
                draw.text((position[0], y), line, font=font, fill=(0, 0, 0))
                bbox = draw.textbbox((position[0], y), line, font=font)
                y += bbox[3] - bbox[1] + 2  # Adding some spacing
                if y > A4_HEIGHT_PIXELS - PADDING_BOTTOM:
                    break
            return y

#

        if file.name.lower().endswith('.pdf'):
            # Convert PDF to image using PyMuPDF
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            first_page = pdf_document.load_page(0)  # Load the first page
            pix = first_page.get_pixmap(matrix=fitz.Matrix(DPI / 72, DPI / 72))  # Adjust for DPI
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Define the stretch factor (e.g., 1.05 for 5% stretch)
            stretch_factor = .9
            
            # Calculate new dimensions
            new_width = int(img.width * stretch_factor)
            new_height = int(img.height * stretch_factor)
            
            # Resize the image to stretch it
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Create an A4 image with white background
            a4_img = Image.new('RGB', (A4_WIDTH_PIXELS, A4_HEIGHT_PIXELS), color='white')
            
            # Calculate the dimensions of the resized image
            img_width, img_height = img.size
            
            # Calculate the position to center the image within the A4 page considering padding
            x_position = (A4_WIDTH_PIXELS - img_width) // 2
            y_position = (A4_HEIGHT_PIXELS - img_height) // 2
            
            # Adjust the position to respect padding boundaries
            x_position = max(IMG_PADDING_LEFT, min(x_position, A4_WIDTH_PIXELS - img_width - IMG_PADDING_RIGHT))
            y_position = max(IMG_PADDING_TOP, min(y_position, A4_HEIGHT_PIXELS - img_height - IMG_PADDING_BOTTOM))
            
            # Paste the image onto the new A4 image at the calculated position
            a4_img.paste(img, (x_position, y_position))
            
            # Save the resulting image to the buffer
            a4_img.save(buffer, format=format)
            buffer.seek(0)
        
        elif file.name.lower().endswith('.docx'):
            # Convert DOCX to image (render as text and convert to image)
            doc = Document(file)
            text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
            
            # Create an A4 image with padding
            img = Image.new('RGB', (A4_WIDTH_PIXELS, A4_HEIGHT_PIXELS), color='white')
            d = ImageDraw.Draw(img)
            
            # Implement text formatting
            y_offset = PADDING_TOP
            paragraphs = text.split('\n')
            for para in paragraphs:
                if para.strip() == "":
                    y_offset += PARAGRAPH_SPACING
                    continue
                if para.startswith('# '):
                    y_offset = draw_text(d, para[2:], (PADDING_LEFT, y_offset), heading_font, content_width)
                    y_offset += HEADING_SPACING  # Extra spacing after headings
                elif para.startswith('## '):
                    y_offset = draw_text(d, para[3:], (PADDING_LEFT, y_offset), subheading_font, content_width)
                else:
                    y_offset = draw_text(d, para, (PADDING_LEFT, y_offset), body_font, content_width)
                y_offset += PARAGRAPH_SPACING  # Add spacing after each paragraph
                if y_offset > A4_HEIGHT_PIXELS - PADDING_BOTTOM:
                    break
            
            img.save(buffer, format=format)
            buffer.seek(0)
        
        else:
            return HttpResponse("Unsupported file type for image conversion", status=400)
        
        converted_file_content = buffer.getvalue()
        save_converted_file(user, file, converted_file_content, format)
        
        response = HttpResponse(converted_file_content, content_type=f'image/{format.lower()}')
        response['Content-Disposition'] = f'attachment; filename="converted.{format.lower()}"'
        return response
    
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)