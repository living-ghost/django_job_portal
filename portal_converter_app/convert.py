from io import BytesIO
from docx import Document
from docx.shared import Pt
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

def convert_to_pdf_from_text(text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    # Define styles
    heading_style = ParagraphStyle(
        name='HeadingStyle',
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=9,  # Space after heading
    )
    
    subheading_style = ParagraphStyle(
        name='SubheadingStyle',
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceAfter=5,  # Space after subheading
    )
    
    body_style = ParagraphStyle(
        name='BodyStyle',
        fontName='Helvetica',
        fontSize=10,
        spaceAfter=2,  # Space after body text
    )

    # Process the text and apply styles
    paragraphs = text.split('\n')
    for para in paragraphs:
        para = para.strip()
        if para.startswith('# '):  # Heading
            styled_paragraph = Paragraph(para[2:], heading_style)
        elif para.startswith('## '):  # Subheading
            styled_paragraph = Paragraph(para[3:], subheading_style)
        else:  # Body text
            styled_paragraph = Paragraph(para, body_style)
        
        story.append(styled_paragraph)

    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

#

def convert_to_docx_from_text(text):
    buffer = BytesIO()
    doc = Document()
    
    # Define custom styles for headings and body text
    styles = doc.styles
    
    # Heading style
    if 'HeadingStyle' not in styles:
        heading_style = styles.add_style('HeadingStyle', 1)
        heading_font = heading_style.font
        heading_font.name = 'Arial'
        heading_font.size = Pt(14)
        heading_font.bold = True
        # Add space after heading
        heading_paragraph_format = heading_style.paragraph_format
        heading_paragraph_format.space_after = Pt(12)  # Adjust space after heading to 12 pt
    
    # Subheading style
    if 'SubheadingStyle' not in styles:
        subheading_style = styles.add_style('SubheadingStyle', 1)
        subheading_font = subheading_style.font
        subheading_font.name = 'Arial'
        subheading_font.size = Pt(12)
        subheading_font.bold = True
        # Add space after subheading
        subheading_paragraph_format = subheading_style.paragraph_format
        subheading_paragraph_format.space_after = Pt(12)  # Adjust space after subheading to 8 pt
    
    # Body text style
    if 'BodyStyle' not in styles:
        body_style = styles.add_style('BodyStyle', 1)
        body_font = body_style.font
        body_font.name = 'Arial'
        body_font.size = Pt(10)
        # Set line spacing for body text
        body_paragraph_format = body_style.paragraph_format
        body_paragraph_format.line_spacing = Pt(10)  # Adjust line spacing to 10 pt
        body_paragraph_format.space_after = Pt(4)    # Optional: Adjust space after paragraph
    
    # Process the text and apply styles
    paragraphs = text.split('\n')
    for para in paragraphs:
        para = para.strip()
        if para.startswith('# '):  # Heading
            doc.add_paragraph(para[2:], style='HeadingStyle')
        elif para.startswith('## '):  # Subheading
            doc.add_paragraph(para[3:], style='SubheadingStyle')
        else:  # Body text
            doc.add_paragraph(para, style='BodyStyle')
    
    # Save the document to the BytesIO buffer
    doc.save(buffer)
    buffer.seek(0)  # Move the cursor to the beginning of the buffer
    return buffer.getvalue()  # Return the byte content of the DOCX file