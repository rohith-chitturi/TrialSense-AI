import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DocumentParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse a document and return extracted text and metadata."""
        pass

class PDFParser(DocumentParser):
    def __init__(self, text_density_threshold: int = 50):
        # If a page has fewer characters than this, trigger OCR
        self.text_density_threshold = text_density_threshold

    def parse(self, file_path: str) -> Dict[str, Any]:
        doc = fitz.open(file_path)
        extracted_text = []
        
        # Extract rich metadata immediately as requested
        metadata = {
            "page_count": doc.page_count,
            "creation_date": doc.metadata.get("creationDate", ""),
            "author": doc.metadata.get("author", ""),
            "producer": doc.metadata.get("producer", ""),
            "format": doc.metadata.get("format", ""),
            "is_encrypted": doc.is_encrypted
        }
        
        if doc.is_encrypted:
            raise ValueError("PDF is encrypted/password protected.")
            
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            
            # Text Density Analysis
            if len(text.strip()) < self.text_density_threshold:
                # OCR Fallback
                text = self._ocr_page(file_path, page_num)
                
            extracted_text.append({
                "page": page_num + 1,
                "text": text
            })
            
        return {
            "metadata": metadata,
            "content": extracted_text
        }
        
    def _ocr_page(self, file_path: str, page_num: int) -> str:
        """Fallback to Tesseract OCR for a specific scanned page."""
        # Note: pdf2image converts the whole pdf by default, but we can specify first_page and last_page
        images = convert_from_path(file_path, first_page=page_num+1, last_page=page_num+1)
        if not images:
            return ""
            
        # OCR the single image
        ocr_text = pytesseract.image_to_string(images[0])
        return ocr_text

# Future parsers
# class WordParser(DocumentParser): ...
# class HL7Parser(DocumentParser): ...
