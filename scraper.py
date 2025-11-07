"""
Web scraper for Verse by Verse Ministry website.

This module provides functionality to scrape Bible study materials from
versebyverseministry.org and store them for use in a chatbot.
"""

import os
import json
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


class VBVMScraper:
    """Scraper for Verse by Verse Ministry website."""
    
    def __init__(self, base_url: str = "https://versebyverseministry.org/", 
                 output_dir: str = "scraped_content"):
        """
        Initialize the scraper.
        
        Args:
            base_url: The base URL of the website to scrape (use HTTPS for secure connection)
            output_dir: Directory to store scraped content
        """
        self.base_url = base_url
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.visited_urls = set()
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a page from the website.
        
        Args:
            url: URL to fetch
            
        Returns:
            Page content as string, or None if fetch failed
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_content(self, html: str, url: str) -> Dict:
        """
        Extract relevant content from a page.
        
        Args:
            html: HTML content of the page
            url: URL of the page
            
        Returns:
            Dictionary containing extracted content
        """
        soup = BeautifulSoup(html, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else ""
        
        # Extract main content (adjust selectors based on actual website structure)
        content_selectors = ['article', 'main', '.content', '.post', '#content']
        main_content = ""
        
        for selector in content_selectors:
            if selector.startswith('.'):
                content = soup.find(class_=selector[1:])
            elif selector.startswith('#'):
                content = soup.find(id=selector[1:])
            else:
                content = soup.find(selector)
            
            if content:
                main_content = content.get_text(separator='\n', strip=True)
                break
        
        # If no specific content area found, get body text
        if not main_content:
            body = soup.find('body')
            main_content = body.get_text(separator='\n', strip=True) if body else ""
        
        # Extract links to other study materials
        links = []
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(url, link['href'])
            # Only keep links from the same domain
            if urlparse(absolute_url).netloc == urlparse(self.base_url).netloc:
                links.append({
                    'url': absolute_url,
                    'text': link.get_text(strip=True)
                })
        
        return {
            'url': url,
            'title': title_text,
            'content': main_content,
            'links': links
        }
    
    def scrape_page(self, url: str) -> Optional[Dict]:
        """
        Scrape a single page.
        
        Args:
            url: URL to scrape
            
        Returns:
            Dictionary containing page data, or None if scraping failed
        """
        if url in self.visited_urls:
            return None
        
        print(f"Scraping: {url}")
        self.visited_urls.add(url)
        
        html = self.fetch_page(url)
        if not html:
            return None
        
        data = self.extract_content(html, url)
        
        # Save individual page data
        filename = self._url_to_filename(url)
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved: {filepath}")
        
        # Be respectful to the server
        time.sleep(1)
        
        return data
    
    def scrape_site(self, start_url: Optional[str] = None, max_pages: int = 100):
        """
        Recursively scrape the website starting from a URL.
        
        Args:
            start_url: URL to start scraping from (defaults to base_url)
            max_pages: Maximum number of pages to scrape
        """
        if start_url is None:
            start_url = self.base_url
        
        urls_to_visit = [start_url]
        pages_scraped = 0
        all_data = []
        
        while urls_to_visit and pages_scraped < max_pages:
            url = urls_to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            data = self.scrape_page(url)
            
            if data:
                all_data.append({
                    'url': data['url'],
                    'title': data['title']
                })
                pages_scraped += 1
                
                # Add new URLs to visit
                for link in data['links']:
                    link_url = link['url']
                    if link_url not in self.visited_urls and link_url not in urls_to_visit:
                        # Filter to only include study material pages
                        if self._is_study_material(link_url):
                            urls_to_visit.append(link_url)
        
        # Save index of all scraped pages
        index_path = os.path.join(self.output_dir, 'index.json')
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nScraping complete! Scraped {pages_scraped} pages.")
        print(f"Index saved to: {index_path}")
    
    def _url_to_filename(self, url: str) -> str:
        """Convert URL to a valid filename."""
        # Remove protocol and replace special characters
        filename = url.replace('http://', '').replace('https://', '')
        filename = filename.replace('/', '_').replace(':', '_')
        
        # Ensure it's not too long
        if len(filename) > 200:
            filename = filename[:200]
        
        return f"{filename}.json"
    
    def _is_study_material(self, url: str) -> bool:
        """
        Determine if a URL likely contains study material.
        
        Args:
            url: URL to check
            
        Returns:
            True if URL likely contains study material
        """
        # Common patterns in study material URLs
        study_patterns = [
            'study', 'lesson', 'teaching', 'sermon', 'bible',
            'book', 'chapter', 'verse', 'commentary', 'article'
        ]
        
        url_lower = url.lower()
        return any(pattern in url_lower for pattern in study_patterns)


def main():
    """Main function to run the scraper."""
    scraper = VBVMScraper()
    
    print("Starting Verse by Verse Ministry scraper...")
    print(f"Target URL: {scraper.base_url}")
    print(f"Output directory: {scraper.output_dir}")
    print("-" * 50)
    
    try:
        scraper.scrape_site(max_pages=100)
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"\nError during scraping: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
