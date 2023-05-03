import os
import requests
import magic
from io import BytesIO
import PyPDF2

def read_pdf(pdf_path: str) -> str:
    """Handles the read_pdf command for the plugin.

    Args:
        file (str): URL or full local file path of the PDF file.

    Returns:
        str: The contents of the PDF file.
    """
    try:
        is_local_file = os.path.isfile(pdf_path)

        if not is_local_file and not url.startswith("http"):
            return "Invalid  URL or full local file path of the PDF file. " \
                "Please ensure to provide the complete file path or valid URL."

        if is_local_file:
            with open(pdf_path, "rb") as pdf_content:
                content = pdf_content.read()
        else:
            response = requests.get(pdf_path)

            if response.status_code != 200:
                return "Error downloading the PDF file. Please check the URL and try again."

            content = response.content

        # Use python-magic to determine the file type based on content
        file_type = magic.from_buffer(content, mime=True)

        if file_type != 'application/pdf':
            return "Invalid file format. Only PDF files are supported."

        with BytesIO(content) as pdf_content:
            pdf_reader = PyPDF2.PdfReader(pdf_content)
            pdf_content = ""
            for page_num in range(len(pdf_reader.pages)):
                pdf_content += pdf_reader.pages[page_num].extract_text()

        return pdf_content

    except Exception as e:
        return f"Error reading the PDF file: {str(e)}"