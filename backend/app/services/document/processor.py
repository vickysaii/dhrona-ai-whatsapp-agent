import io
import csv
from typing import List, Dict, Any
import pypdf
import docx
import pandas as pd

class DocumentProcessorService:
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extracts text content from PDF binary bytes.
        """
        text = ""
        pdf_file = io.BytesIO(file_content)
        try:
            reader = pypdf.PdfReader(pdf_file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            raise ValueError(f"Failed to parse PDF file: {str(e)}")
        return text

    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """
        Extracts text content from Microsoft Word DOCX binary bytes.
        """
        text = ""
        docx_file = io.BytesIO(file_content)
        try:
            doc = docx.Document(docx_file)
            for paragraph in doc.paragraphs:
                if paragraph.text:
                    text += paragraph.text + "\n"
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX file: {str(e)}")
        return text

    @staticmethod
    def extract_text_from_csv(file_content: bytes) -> str:
        """
        Extracts tabular text rows from CSV binary bytes.
        """
        text = ""
        try:
            csv_str = file_content.decode('utf-8')
            reader = csv.reader(io.StringIO(csv_str))
            for row in reader:
                # Join columns with space or comma and wrap in text representation
                text += ", ".join(row) + "\n"
        except Exception as e:
            try:
                # Fallback to ISO-8859-1 encoding if UTF-8 fails
                csv_str = file_content.decode('ISO-8859-1')
                reader = csv.reader(io.StringIO(csv_str))
                for row in reader:
                    text += ", ".join(row) + "\n"
            except Exception as inner_e:
                raise ValueError(f"Failed to parse CSV file: {str(inner_e)}")
        return text

    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """
        Extracts text content from plain text file bytes.
        """
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_content.decode('ISO-8859-1')
            except Exception as e:
                raise ValueError(f"Failed to decode text file: {str(e)}")

    @classmethod
    def extract_text(cls, file_content: bytes, filename: str) -> str:
        """
        Detects file type based on extension and extracts text.
        """
        ext = filename.split('.')[-1].lower()
        if ext == 'pdf':
            return cls.extract_text_from_pdf(file_content)
        elif ext in ['doc', 'docx']:
            return cls.extract_text_from_docx(file_content)
        elif ext == 'csv':
            return cls.extract_text_from_csv(file_content)
        elif ext in ['txt', 'md']:
            return cls.extract_text_from_txt(file_content)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Splits clean text into segments of chunk_size with chunk_overlap using a recursive/sliding window method.
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + chunk_size, text_len)
            # Try to align boundaries to natural separators if not at the absolute end
            if end < text_len:
                # Look for last newline or space in the overlap zone to split cleanly
                search_start = max(start, end - chunk_overlap)
                best_split = text.rfind('\n', search_start, end)
                if best_split == -1:
                    best_split = text.rfind(' ', search_start, end)
                
                if best_split != -1 and best_split > start:
                    end = best_split
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - chunk_overlap
            if start >= text_len or end >= text_len:
                break
                
        return chunks
