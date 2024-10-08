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
    if os.name == 'nt':  # Windows
        soffice_path = settings.LIBRE_OFFICE
    elif os.name == 'posix':
        soffice_path = settings.LIBRE_OFFICE
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


def convert_docx_to_jpg(docx_path):
    """Convert DOCX to JPG by converting to PDF first."""
    pdf_path = convert_docx_to_pdf(docx_path)  # Step 1: Convert DOCX to PDF
    jpg_path = convert_pdf_to_jpg(pdf_path)    # Step 2: Convert PDF to JPG
    return jpg_path


def convert_docx_to_png(docx_path):
    """Convert DOCX to JPG by converting to PDF first."""
    pdf_path = convert_docx_to_pdf(docx_path)  # Step 1: Convert DOCX to PDF
    png_path = convert_pdf_to_jpg(pdf_path)    # Step 2: Convert PDF to PNG
    return png_path


def convert_pdf_to_docx(pdf_path):
    # Ensure the input file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")

    # Determine the output directory
    output_dir = tempfile.mkdtemp()
    print(f"Output directory: {output_dir}")

    # Command to convert PDF to DOCX
    if os.name == 'nt':
        soffice_path = settings.LIBRE_OFFICE
    elif os.name == 'posix':
        soffice_path = settings.LIBRE_OFFICE
    else:
        raise EnvironmentError("Unsupported operating system.")

    command = [
        soffice_path,
        "--headless",
        "--infilter=writer_pdf_import",  # Specify the PDF import filter
        "--convert-to", "docx",  # Specify the output format as DOCX
        "--outdir", output_dir,  # Specify the output directory
        pdf_path  # Path to the PDF file
    ]

    # Execute the command
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {process.stderr}")

    # Determine the DOCX file path
    base_name = os.path.basename(pdf_path)
    docx_name = os.path.splitext(base_name)[0] + '.docx'
    docx_path = os.path.join(output_dir, docx_name)

    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"Conversion failed. DOCX not found at {docx_path}.")

    return docx_path


def convert_pdf_to_jpg(pdf_path):
    """Convert PDF to JPG."""
    # Ensure the input file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")

    # Determine the output directory
    output_dir = tempfile.mkdtemp()

    # Command to convert PDF to JPG using LibreOffice
    if os.name == 'nt':
        soffice_path = settings.LIBRE_OFFICE
    elif os.name == 'posix':
        soffice_path = settings.LIBRE_OFFICE
    else:
        raise EnvironmentError("Unsupported operating system.")

    command = [
        soffice_path,
        "--headless",
        "--convert-to", "jpg",  # Specify the output format as JPG
        "--outdir", output_dir,  # Specify the output directory
        pdf_path  # Path to the PDF file
    ]

    # Execute the command
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion to JPG failed: {process.stderr}")

    # Determine the JPG file path
    base_name = os.path.basename(pdf_path)
    jpg_name = os.path.splitext(base_name)[0] + '.jpg'
    jpg_path = os.path.join(output_dir, jpg_name)

    if not os.path.exists(jpg_path):
        raise FileNotFoundError(f"Conversion failed. JPG not found at {jpg_path}.")

    return jpg_path


def convert_pdf_to_png(pdf_path):
    """Convert PDF to PNG."""
    # Ensure the input file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"The file {pdf_path} does not exist.")

    # Determine the output directory
    output_dir = tempfile.mkdtemp()

    # Command to convert PDF to JPG using LibreOffice
    if os.name == 'nt':
        soffice_path = settings.LIBRE_OFFICE
    elif os.name == 'posix':
        soffice_path = settings.LIBRE_OFFICE
    else:
        raise EnvironmentError("Unsupported operating system.")

    command = [
        soffice_path,
        "--headless",
        "--convert-to", "png",  # Specify the output format as JPG
        "--outdir", output_dir,  # Specify the output directory
        pdf_path  # Path to the PDF file
    ]

    # Execute the command
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion to PNG failed: {process.stderr}")

    # Determine the JPG file path
    base_name = os.path.basename(pdf_path)
    png_name = os.path.splitext(base_name)[0] + '.png'
    png_path = os.path.join(output_dir, png_name)

    if not os.path.exists(png_path):
        raise FileNotFoundError(f"Conversion failed. JPG not found at {png_path}.")

    return png_path