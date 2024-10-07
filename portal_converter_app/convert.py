import os
import tempfile
import subprocess
from django.conf import settings


def convert_docx_to_pdf(docx_path):
    """
    Convert a DOCX file to PDF using LibreOffice in headless mode.
    Returns the path to the converted PDF file.
    """
    # Ensure the input file exists
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"The file {docx_path} does not exist.")

    # Determine the output directory
    output_dir = tempfile.mkdtemp()

    # Command to convert DOCX to PDF
    # Adjust the path to 'soffice' if necessary
    if os.name == 'nt':  # Windows
        soffice_path = settings.LIBRE_OFFICE
    elif os.name == 'posix':
        soffice_path = "soffice"
    else:
        raise EnvironmentError("Unsupported operating system.")

    command = [
        soffice_path,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', output_dir,
        docx_path
    ]

    # Execute the command
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {process.stderr}")

    # Determine the PDF file path
    base_name = os.path.basename(docx_path)
    pdf_name = os.path.splitext(base_name)[0] + '.pdf'
    pdf_path = os.path.join(output_dir, pdf_name)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Conversion failed. PDF not found at {pdf_path}.")

    return pdf_path
