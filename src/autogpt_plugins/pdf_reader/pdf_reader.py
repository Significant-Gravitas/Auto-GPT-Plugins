from autogpt.commands.command import command
from autogpt.url_utils.validators import is_valid_url, sanitize_url
import autogpt.processing.text as summary
import os
import requests
import magic
from io import BytesIO
import PyPDF2

class InvalidFileFormatException(Exception):
    def __init__(self, message="Invalid file format"):
        super().__init__(message)

def check_read_ingest_pdf_file(location: str, question: str, content: BytesIO) -> str:
    try:
        # Use python-magic to determine the file type based on content
        file_type = magic.from_buffer(content, mime=True)
        if file_type != 'application/pdf':
            raise InvalidFileFormatException("Invalid file format. Only PDF files are supported.")

        # Read PDF content from binary content
        with BytesIO(content) as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_content = ""
            for page_num in range(len(pdf_reader.pages)):
                pdf_content += pdf_reader.pages[page_num].extract_text()

        # Ingest PDF content
        summary_text = summary.summarize_text(location, pdf_content, question)

        return f"Summary of PDF: {summary_text}"

    except Exception as e:
        return f"Error reading the PDF file: {str(e)}"

@command("read_pdf", "Read PDF", {"location": "<location>", "question": "<what_you_want_to_find_on_pdf_file>",},)
def read_pdf(location: str, question: str) -> str:
    """Handles the read_pdf command for the plugin.

    Args:
        location (str): URL or local file path to pdf.
        question (str): The question asked by the user

    Returns:
        str: The summary of the PDF file.
    """
    try:
        # Check PDF location
        is_local_file = os.path.isfile(location)
        if not is_valid_url(location):
            location = sanitize_url(location)
        if not is_local_file and not is_valid_url(location):
            raise FileNotFoundError("Invalid URL or local file path to PDF. Please, ensure to provide a valid URL or the complete local file path to PDF.")

        # Read PDF content
        if is_local_file:
            with open(location, "rb") as pdf_file:
                content = pdf_file.read()
        else:
            response = requests.get(location)
            if response.status_code != 200:
                raise FileNotFoundError("Error downloading the PDF file. Please check the URL and try again.")
            content = response.content

        return check_read_ingest_pdf_file(location, question, content)

    except Exception as e:
        return f"Error reading the PDF file: {str(e)}"