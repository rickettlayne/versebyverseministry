"""
PDF processor to extract text from downloaded PDF files
"""

import os
from typing import List, Dict
from PyPDF2 import PdfReader
import config


class PDFProcessor:
    """Extract and process text from PDF files"""
    
    def __init__(self, pdf_dir: str = config.PDF_SAVE_DIR):
        self.pdf_dir = pdf_dir
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a single PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def process_all_pdfs(self) -> List[Dict[str, str]]:
        """
        Process all PDF files in the directory
        
        Returns:
            List of dictionaries containing filename and extracted text
        """
        documents = []
        
        if not os.path.exists(self.pdf_dir):
            print(f"Directory {self.pdf_dir} does not exist")
            return documents
        
        pdf_files = [f for f in os.listdir(self.pdf_dir) if f.endswith('.pdf')]
        
        print(f"Processing {len(pdf_files)} PDF files...")
        
        for filename in pdf_files:
            pdf_path = os.path.join(self.pdf_dir, filename)
            print(f"Processing: {filename}")
            
            text = self.extract_text_from_pdf(pdf_path)
            
            if text:
                documents.append({
                    'filename': filename,
                    'filepath': pdf_path,
                    'content': text
                })
        
        print(f"Successfully processed {len(documents)} documents")
        return documents


if __name__ == "__main__":
    processor = PDFProcessor()
    docs = processor.process_all_pdfs()
    
    for doc in docs:
        print(f"\n{doc['filename']}: {len(doc['content'])} characters")
