from django.http import HttpResponse
from django.shortcuts import render
from docx import Document
import fitz  # PyMuPDF for PDF text extraction

font_size_thresholds = {
    "heading1": 16,
    "heading2": 14
}

tolerance = 2  # Adjust this tolerance level based on your observations
def extract_text_from_pdf(file):
    text = ""
    try:
        # Open the PDF file from the provided file stream
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        try:
            # Iterate over each page in the PDF
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                blocks = page.get_text("dict")["blocks"]
                
                for block in blocks:
                    # Process each block of text
                    if block['type'] == 0:  # Text block
                        for line in block["lines"]:
                            for span in line["spans"]:
                                # Get the font size
                                font_size = span["size"]
                                text_content = span["text"].strip()
                                
                                if font_size >= (font_size_thresholds["heading1"] - tolerance):
                                    text += f"# {text_content}\n"
                                elif font_size >= (font_size_thresholds["heading2"] - tolerance):
                                    text += f"## {text_content}\n"
                                else:
                                    text += f"{text_content}\n"
            
        finally:
            pdf_document.close()  # Ensure the document is closed properly
    except Exception as e:
        # Handle exceptions and provide an error response
        return HttpResponse(f"An error occurred while extracting text from PDF: {e}", status=500)
    
    return text.strip()  # Return the extracted text, stripped of leading/trailing whitespace

#

def extract_text_from_docx(file):
    text = ""
    try:
        doc = Document(file)  # Load the DOCX file
        
        for paragraph in doc.paragraphs:
            # Access style and font size
            style = paragraph.style.name
            max_font_size = 0
            for run in paragraph.runs:
                font_size = run.font.size
                if font_size:
                    max_font_size = max(max_font_size, font_size.pt)
            
            paragraph_text = paragraph.text.strip()  # Get and strip any extra spaces from the paragraph text
            
            # Determine the formatting based on style and font size
            if style.startswith("Heading 1") or (max_font_size >= 16):
                text += f"# {paragraph_text}\n"  # Markdown syntax for a top-level heading
            elif style.startswith("Heading 2") or (max_font_size >= 14):
                text += f"## {paragraph_text}\n"  # Markdown syntax for a second-level heading
            else:
                text += f"{paragraph_text}\n"  # Regular text without special formatting

    except Exception as e:
        return HttpResponse(f"An error occurred while extracting text from DOCX: {e}", status=500)
    
    return text.strip()  # Return the extracted text with leading and trailing whitespace removed