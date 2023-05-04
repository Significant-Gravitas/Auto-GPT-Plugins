from autogpt.commands.command import command
import autogpt.processing.text as summary
import os
import requests
import magic
from io import BytesIO
import PyPDF2

class InvalidFileFormatException(Exception):
    def __init__(self, message="Invalid file format"):
        super().__init__(message)

@command("read_pdf", "Read PDF", '"filename": "<filename>"')
def read_pdf(filename: str) -> str:
    """Handles the read_pdf command for the plugin.

    Args:
        filename (str): Local or remote URL to pdf file.

    Returns:
        str: The contents of the PDF file.
    """
    try:
        is_local_file = os.path.isfile(filename)
        if not is_local_file and not filename.startswith("http"):
            raise FileNotFoundError("Invalid local or remote URL to pdf file. Please ensure to provide the complete local file path or valid remote URL.")

        if is_local_file:
            with open(filename, "rb") as pdf_file:
                content = pdf_file.read()
        else:
            response = requests.get(filename)
            if response.status_code != 200:
                raise FileNotFoundError("Error downloading the PDF file. Please check the URL and try again.")

            content = response.content

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
        summary_text = summary.summarize_text(filename, pdf_content, "")

        return f"Summary of PDF: {summary_text}"

    except Exception as e:
        return f"Error reading the PDF file: {str(e)}"