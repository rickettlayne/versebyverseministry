"""
Example usage of the Verse by Verse Ministry PDF Scraper and Chatbot

This script demonstrates how to use the various components programmatically.
"""

from pdf_scraper import PDFScraper
from pdf_processor import PDFProcessor
from chatbot import VBVMChatbot
import os


def example_scraping():
    """Example: How to scrape PDFs from the website"""
    print("="*60)
    print("Example 1: Scraping PDFs")
    print("="*60)
    
    # Initialize scraper
    scraper = PDFScraper()
    
    # Scrape with custom depth
    downloaded_files = scraper.scrape(max_depth=2)
    
    print(f"\nDownloaded {len(downloaded_files)} PDFs")
    for filepath in downloaded_files[:5]:  # Show first 5
        print(f"  - {filepath}")


def example_processing():
    """Example: How to process PDFs and extract text"""
    print("\n" + "="*60)
    print("Example 2: Processing PDFs")
    print("="*60)
    
    # Initialize processor
    processor = PDFProcessor()
    
    # Process all PDFs
    documents = processor.process_all_pdfs()
    
    print(f"\nProcessed {len(documents)} documents")
    for doc in documents[:3]:  # Show first 3
        print(f"\n{doc['filename']}:")
        print(f"  Characters: {len(doc['content'])}")
        print(f"  Preview: {doc['content'][:100]}...")


def example_chatbot():
    """Example: How to use the chatbot"""
    print("\n" + "="*60)
    print("Example 3: Using the Chatbot")
    print("="*60)
    
    # Make sure API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("\nSkipping chatbot example - OPENAI_API_KEY not set")
        print("Set it in .env file or environment variable to use the chatbot")
        return
    
    # Initialize chatbot
    chatbot = VBVMChatbot()
    
    # Load PDFs (will use cached database if available)
    chatbot.load_pdfs()
    
    # Ask questions programmatically
    questions = [
        "What is the main focus of Verse by Verse Ministry?",
        "What topics are covered in the teachings?",
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        answer = chatbot.ask(question, show_sources=True)
        print(f"A: {answer}")


def example_custom_config():
    """Example: Using custom configuration"""
    print("\n" + "="*60)
    print("Example 4: Custom Configuration")
    print("="*60)
    
    # You can override config values
    import config
    
    # Change chunk size for different granularity
    config.CHUNK_SIZE = 500
    config.CHUNK_OVERLAP = 100
    
    # Change model
    config.MODEL_NAME = "gpt-4"
    
    # Change number of results
    config.TOP_K_RESULTS = 3
    
    print(f"Chunk size: {config.CHUNK_SIZE}")
    print(f"Model: {config.MODEL_NAME}")
    print(f"Top K results: {config.TOP_K_RESULTS}")


if __name__ == "__main__":
    print("\nVerse by Verse Ministry - Example Usage\n")
    
    # Uncomment the examples you want to run:
    
    # Example 1: Scrape PDFs from website
    # WARNING: This will actually download files!
    # example_scraping()
    
    # Example 2: Process existing PDFs
    # example_processing()
    
    # Example 3: Use the chatbot
    # example_chatbot()
    
    # Example 4: Show custom configuration
    example_custom_config()
    
    print("\n" + "="*60)
    print("To run the full application, use main.py:")
    print("  python main.py --scrape --chat")
    print("="*60)
