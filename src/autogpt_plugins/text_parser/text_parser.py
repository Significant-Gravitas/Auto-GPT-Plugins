from abc import abstractmethod
from pypdf import PdfReader

parser_map = {
    ".txt": TxtParser(),
    ".pdf": PDFParser()
}

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
            text += page.extract_text() + "\\n"
        return text