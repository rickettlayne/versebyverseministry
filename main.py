"""
Main script to run the complete pipeline: scrape PDFs and start the chatbot
"""

import argparse
import sys
from pdf_scraper import PDFScraper
from chatbot import VBVMChatbot


def main():
    parser = argparse.ArgumentParser(
        description="Verse by Verse Ministry PDF Scraper and Chatbot"
    )
    
    parser.add_argument(
        '--scrape',
        action='store_true',
        help='Scrape PDFs from the website'
    )
    
    parser.add_argument(
        '--depth',
        type=int,
        default=2,
        help='Maximum depth to crawl website (default: 2)'
    )
    
    parser.add_argument(
        '--chat',
        action='store_true',
        help='Start the chatbot'
    )
    
    parser.add_argument(
        '--reindex',
        action='store_true',
        help='Re-index all PDFs (use with --chat)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        help='OpenAI API key (can also be set in .env file)'
    )
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not args.scrape and not args.chat:
        parser.print_help()
        sys.exit(0)
    
    # Scrape PDFs
    if args.scrape:
        print("\n" + "="*60)
        print("STEP 1: Scraping PDFs from website")
        print("="*60 + "\n")
        
        scraper = PDFScraper()
        downloaded_files = scraper.scrape(max_depth=args.depth)
        
        if downloaded_files:
            print(f"\n✓ Successfully downloaded {len(downloaded_files)} PDFs")
        else:
            print("\n✗ No PDFs were downloaded")
            if not args.chat:
                sys.exit(1)
    
    # Start chatbot
    if args.chat:
        print("\n" + "="*60)
        print("STEP 2: Starting Chatbot")
        print("="*60 + "\n")
        
        try:
            chatbot = VBVMChatbot(openai_api_key=args.api_key)
            chatbot.load_pdfs(reindex=args.reindex)
            chatbot.chat()
        except ValueError as e:
            print(f"Error: {e}")
            print("\nPlease ensure:")
            print("1. You have run the scraper to download PDFs (--scrape)")
            print("2. You have set your OpenAI API key:")
            print("   - Create a .env file with: OPENAI_API_KEY=your_key_here")
            print("   - Or use --api-key parameter")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
