"""
Web scraper to extract PDF links and download PDFs from versebyverseministry.org
"""

import os
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Optional
import config


class PDFScraper:
    """Scrapes and downloads PDF files from the website"""
    
    def __init__(self, base_url: str = config.BASE_URL):
        self.base_url = base_url
        self.pdf_save_dir = config.PDF_SAVE_DIR
        self.visited_urls: Set[str] = set()
        self.pdf_links: Set[str] = set()
        
        # Create directory for PDFs if it doesn't exist
        os.makedirs(self.pdf_save_dir, exist_ok=True)
        
        self.headers = {
            'User-Agent': config.USER_AGENT
        }
    
    def find_pdf_links(self, url: str, max_depth: int = 2, current_depth: int = 0) -> Set[str]:
        """
        Recursively find all PDF links on the website
        
        Args:
            url: URL to scrape
            max_depth: Maximum depth to crawl
            current_depth: Current recursion depth
            
        Returns:
            Set of PDF URLs found
        """
        if current_depth > max_depth or url in self.visited_urls:
            return self.pdf_links
        
        self.visited_urls.add(url)
        
        try:
            print(f"Scanning: {url}")
            response = requests.get(
                url, 
                headers=self.headers, 
                timeout=config.TIMEOUT
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all links
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                # Check if it's a PDF
                if href.lower().endswith('.pdf'):
                    self.pdf_links.add(full_url)
                    print(f"Found PDF: {full_url}")
                
                # Check if it's a page on the same domain to crawl
                elif self._is_same_domain(full_url) and current_depth < max_depth:
                    if full_url not in self.visited_urls:
                        self.find_pdf_links(full_url, max_depth, current_depth + 1)
            
            # Small delay to be respectful to the server
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error scanning {url}: {str(e)}")
        
        return self.pdf_links
    
    def _is_same_domain(self, url: str) -> bool:
        """Check if URL belongs to the same domain"""
        base_domain = urlparse(self.base_url).netloc
        url_domain = urlparse(url).netloc
        return base_domain == url_domain
    
    def download_pdf(self, pdf_url: str) -> Optional[str]:
        """
        Download a single PDF file
        
        Args:
            pdf_url: URL of the PDF to download
            
        Returns:
            Path to the downloaded file, or None if download fails
        """
        filename = os.path.basename(urlparse(pdf_url).path)
        if not filename:
            # Use hashlib for deterministic filename generation
            url_hash = hashlib.md5(pdf_url.encode()).hexdigest()
            filename = f"document_{url_hash}.pdf"
        
        filepath = os.path.join(self.pdf_save_dir, filename)
        
        # Skip if already downloaded
        if os.path.exists(filepath):
            print(f"Already exists: {filename}")
            return filepath
        
        try:
            print(f"Downloading: {filename}")
            response = requests.get(
                pdf_url, 
                headers=self.headers, 
                timeout=config.TIMEOUT
            )
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Saved: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error downloading {pdf_url}: {str(e)}")
            return None
    
    def download_all_pdfs(self, pdf_urls: Set[str] = None) -> List[str]:
        """
        Download all PDF files
        
        Args:
            pdf_urls: Set of PDF URLs to download (uses self.pdf_links if None)
            
        Returns:
            List of paths to downloaded files
        """
        if pdf_urls is None:
            pdf_urls = self.pdf_links
        
        downloaded_files = []
        
        for pdf_url in pdf_urls:
            filepath = self.download_pdf(pdf_url)
            if filepath:
                downloaded_files.append(filepath)
            time.sleep(0.5)  # Be respectful to the server
        
        return downloaded_files
    
    def scrape(self, max_depth: int = 2) -> List[str]:
        """
        Main method to scrape and download all PDFs
        
        Args:
            max_depth: Maximum depth to crawl the website
            
        Returns:
            List of paths to downloaded PDF files
        """
        print(f"Starting scrape of {self.base_url}")
        print(f"Maximum crawl depth: {max_depth}")
        
        # Find all PDF links
        self.find_pdf_links(self.base_url, max_depth)
        
        print(f"\nFound {len(self.pdf_links)} PDF files")
        
        # Download all PDFs
        downloaded_files = self.download_all_pdfs()
        
        print(f"\nDownloaded {len(downloaded_files)} PDF files to {self.pdf_save_dir}/")
        
        return downloaded_files


if __name__ == "__main__":
    scraper = PDFScraper()
    scraper.scrape(max_depth=2)
