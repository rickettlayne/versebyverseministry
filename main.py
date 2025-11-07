"""
Main entry point for the Verse by Verse Ministry project.

This module provides a command-line interface to run the scraper
and chatbot.
"""

import argparse
import sys
from scraper import VBVMScraper
from chatbot import VBVMChatbot


def run_scraper(args):
    """Run the web scraper."""
    scraper = VBVMScraper(
        base_url=args.url,
        output_dir=args.output
    )
    
    print(f"Starting scraper...")
    print(f"Target URL: {args.url}")
    print(f"Max pages: {args.max_pages}")
    print(f"Output directory: {args.output}")
    print("-" * 60)
    
    scraper.scrape_site(max_pages=args.max_pages)


def run_chatbot(args):
    """Run the chatbot."""
    chatbot = VBVMChatbot(content_dir=args.content_dir)
    chatbot.chat()


def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Verse by Verse Ministry - Web Scraper and Chatbot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run the scraper
  python main.py scrape
  
  # Run the scraper with custom settings
  python main.py scrape --max-pages 50 --output my_content
  
  # Run the chatbot
  python main.py chat
  
  # Run the chatbot with custom content directory
  python main.py chat --content-dir my_content
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Scraper command
    scraper_parser = subparsers.add_parser('scrape', help='Run the web scraper')
    scraper_parser.add_argument(
        '--url',
        default='http://versebyverseministry.org/',
        help='Base URL to scrape (default: http://versebyverseministry.org/)'
    )
    scraper_parser.add_argument(
        '--output',
        default='scraped_content',
        help='Output directory for scraped content (default: scraped_content)'
    )
    scraper_parser.add_argument(
        '--max-pages',
        type=int,
        default=100,
        help='Maximum number of pages to scrape (default: 100)'
    )
    
    # Chatbot command
    chatbot_parser = subparsers.add_parser('chat', help='Run the chatbot')
    chatbot_parser.add_argument(
        '--content-dir',
        default='scraped_content',
        help='Directory containing scraped content (default: scraped_content)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'scrape':
        run_scraper(args)
    elif args.command == 'chat':
        run_chatbot(args)


if __name__ == "__main__":
    main()
