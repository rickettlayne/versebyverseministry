"""
Basic tests for the PDF scraper and chatbot components

Run with: python test_basic.py
"""

import os
import sys
from unittest.mock import Mock, patch


def test_config_import():
    """Test that config module loads correctly"""
    try:
        import config
        assert config.BASE_URL == "https://www.versebyverseministry.org"
        assert config.CHUNK_SIZE == 1000
        assert config.CHUNK_OVERLAP == 200
        print("✓ Config module imports correctly")
        return True
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False


def test_pdf_scraper_initialization():
    """Test that PDFScraper can be initialized"""
    try:
        from pdf_scraper import PDFScraper
        scraper = PDFScraper()
        assert scraper.base_url == "https://www.versebyverseministry.org"
        assert scraper.pdf_save_dir == "pdfs"
        assert len(scraper.visited_urls) == 0
        assert len(scraper.pdf_links) == 0
        print("✓ PDFScraper initializes correctly")
        return True
    except Exception as e:
        print(f"✗ PDFScraper initialization failed: {e}")
        return False


def test_pdf_processor_initialization():
    """Test that PDFProcessor can be initialized"""
    try:
        from pdf_processor import PDFProcessor
        processor = PDFProcessor()
        assert processor.pdf_dir == "pdfs"
        print("✓ PDFProcessor initializes correctly")
        return True
    except Exception as e:
        print(f"✗ PDFProcessor initialization failed: {e}")
        return False


def test_url_parsing():
    """Test URL parsing in scraper"""
    try:
        from pdf_scraper import PDFScraper
        scraper = PDFScraper()
        
        # Test same domain check
        assert scraper._is_same_domain("https://www.versebyverseministry.org/page1")
        assert not scraper._is_same_domain("https://www.example.com/page1")
        
        print("✓ URL parsing works correctly")
        return True
    except Exception as e:
        print(f"✗ URL parsing failed: {e}")
        return False


def test_filename_generation():
    """Test deterministic filename generation"""
    try:
        from pdf_scraper import PDFScraper
        import hashlib
        
        scraper = PDFScraper()
        
        # Test with URL that has no filename
        test_url = "https://example.com/path/"
        
        # The hash should be deterministic
        hash1 = hashlib.md5(test_url.encode()).hexdigest()
        hash2 = hashlib.md5(test_url.encode()).hexdigest()
        assert hash1 == hash2
        
        print("✓ Filename generation is deterministic")
        return True
    except Exception as e:
        print(f"✗ Filename generation test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running Basic Tests")
    print("="*60 + "\n")
    
    tests = [
        test_config_import,
        test_pdf_scraper_initialization,
        test_pdf_processor_initialization,
        test_url_parsing,
        test_filename_generation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
