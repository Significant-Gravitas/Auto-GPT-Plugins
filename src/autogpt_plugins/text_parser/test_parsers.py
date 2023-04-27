import unittest
import tempfile
from functools import partial
from unittest import TestCase

import docx
import json, yaml
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from pypdf import PdfWriter
from reportlab.pdfgen import canvas
from parser_plugin import parse_text

plain_text_str = "Hello, world!"


def mock_text_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write(plain_text_str)
    return f.name


def mock_csv_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        f.write(plain_text_str)
    return f.name


def mock_pdf_file():
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".pdf") as f:
        c = canvas.Canvas(f.name)
        c.drawString(0, 0, plain_text_str)
        c.save()
    return f.name


def mock_doc_file(is_docx=False):
    with tempfile.NamedTemporaryFile(
        mode="wb", delete=False, suffix=".docx" if is_docx else ".doc"
    ) as f:
        document = docx.Document()
        document.add_paragraph(plain_text_str)
        document.save(f.name)
    return f.name


def mock_json_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        json.dump({"text": plain_text_str}, f)
    return f.name


def mock_xml_file():
    root = ElementTree.Element("root")
    message = ElementTree.SubElement(root, 'message')
    message.text = plain_text_str
    xml_data = ElementTree.tostring(root, encoding='UTF-8', method='xml')
    with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".xml") as f:
        f.write(xml_data)
    return f.name


def mock_yaml_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        yaml.dump({"text": plain_text_str}, f)
    return f.name


def mock_html_file():
    html = BeautifulSoup(
        f"<html><head><title>This is a test</title></head><body><p>{plain_text_str}</p></body></html>",
        "html.parser",
    )
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as f:
        f.write(str(html))
    return f.name


def mock_md_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md") as f:
        f.write(f"# {plain_text_str}!\n")
    return f.name


def mock_latex_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tex") as f:
        latex_str = rf"\documentclass{{article}}\begin{{document}}{plain_text_str}\end{{document}}"
        f.write(latex_str)
    return f.name


respective_file_creation_functions = {
    ".txt": mock_text_file,
    ".csv": mock_csv_file,
    ".pdf": mock_pdf_file,
    ".doc": mock_doc_file,
    ".docx": partial(mock_doc_file, is_docx=True),
    ".json": mock_json_file,
    ".xml": mock_xml_file,
    ".yaml": mock_yaml_file,
    ".html": mock_html_file,
    ".md": mock_md_file,
    ".tex": mock_latex_file,
}


class TestConfig(TestCase):
    def test_parsers(self):
        for (
            file_extension,
            file_creator,
        ) in respective_file_creation_functions.items():
            loaded_text = parse_text(file_creator())
            self.assertIn(plain_text_str, loaded_text)