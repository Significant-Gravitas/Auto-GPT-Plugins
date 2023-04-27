import docx
import ebooklib
import json
import yaml
import markdown
from abc import abstractmethod
from bs4 import BeautifulSoup
from ebooklib import epub
from pypdf import PdfReader
from pylatexenc.latex2text import LatexNodes2Text

class Parser:
    @abstractmethod
    def parse(self, filepath) -> str:
        pass

class TxtParser(Parser):
    def parse(self, filepath) -> str:
        with open(filepath, "r") as f:
            text = f.read()
        return text
    
class PDFParser(Parser):
    def parse(self, filepath) -> str:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
class DOCXParser(Parser):
    def parse(self, filepath) -> str:
        doc_file = docx.Document(filepath)
        text = ""
        for para in doc_file.paragraphs:
            text += para.text
        return text
    
class JSONParser(Parser):
    def parse(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
            text = str(data)
        return text   

class XMLParser(Parser):
    def parse(self, filepath):
        with open(filepath, "r") as f:
            soup = BeautifulSoup(f, "xml")
            text = soup.get_text()
        return text
    
class YAMLParser(Parser):
    def parse(self, filepath):
        with open(filepath, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            text = str(data)
        return text
    
class HTMLParser(Parser):
    def parse(self, filepath):
        with open(filepath, "r") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text()
        return text
    
class MarkdownParser(Parser):
    def parse(self, filepath):
        with open(filepath, "r") as f:
            html = markdown.markdown(f.read())
            text = "".join(BeautifulSoup(html, "html.parser").findAll(string=True))
        return text
    
class LaTeXParser(Parser):
    def parse(self, filepath):
        with open(filepath, "r") as f:
            latex = f.read()
        text = LatexNodes2Text().latex_to_text(latex)
        return text
    
class LaTeXParser(Parser):
    def parse(self, filepath):
        with open(filepath, "r") as f:
            latex = f.read()
        text = LatexNodes2Text().latex_to_text(latex)
        return text
    
class EPUBParser(Parser):
    # Only read text in <p> tags for now.
    def chapter_to_str(self, chapter):
        soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
        text = [para.get_text() for para in soup.find_all('p')]
        return ' '.join(text)

    def parse(self, filepath):
        with open(filepath, "r") as f:  
            text = ""
            book = epub.read_epub(filepath)
            for chapter in book.get_items_of_type(ebooklib.ITEM_DOCUMENT) :
                text += self.chapter_to_str(chapter)
        print(text)
        return text
    
parser_map = {
    ".txt": TxtParser(),
    ".csv": TxtParser(),
    ".pdf": PDFParser(),
    ".docx": DOCXParser(),
    ".json": JSONParser(),
    ".xml": XMLParser(),
    ".yaml": YAMLParser(),
    ".html": HTMLParser(),
    ".md": MarkdownParser(),
    ".tex": LaTeXParser(),
    ".epub": EPUBParser()
}