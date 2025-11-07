# Verse by Verse Ministry - Web Scraper and Chatbot

A Python-based project to scrape Bible study materials from [versebyverseministry.org](https://versebyverseministry.org/) and provide a chatbot interface to answer Bible-related questions using the collected content.

## Overview

This project consists of two main components:

1. **Web Scraper** (`scraper.py`) - Collects Bible study materials from the Verse by Verse Ministry website
2. **Chatbot** (`chatbot.py`) - Answers Bible questions using the scraped content

## Features

- **Intelligent Web Scraping**: Automatically crawls and extracts Bible study content
- **Content Storage**: Saves scraped content in structured JSON format
- **Search Functionality**: Finds relevant content based on user queries
- **Interactive Chatbot**: Provides answers with source citations
- **Respectful Scraping**: Implements delays to avoid overloading the server

## Installation

1. Clone this repository:
```bash
git clone https://github.com/rickettlayne/versebyverseministry.git
cd versebyverseministry
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Scraper

To scrape content from the website:

```bash
python main.py scrape
```

Optional arguments:
- `--url`: Base URL to scrape (default: https://versebyverseministry.org/)
- `--output`: Output directory (default: scraped_content)
- `--max-pages`: Maximum pages to scrape (default: 100)

Example:
```bash
python main.py scrape --max-pages 50 --output my_content
```

### Running the Chatbot

After scraping content, start the chatbot:

```bash
python main.py chat
```

Optional arguments:
- `--content-dir`: Directory with scraped content (default: scraped_content)

Example:
```bash
python main.py chat --content-dir my_content
```

### Using the Chatbot

Once the chatbot is running:
1. Type your Bible-related question
2. The chatbot will search the scraped content and provide answers with sources
3. Type 'quit' or 'exit' to end the session

Example questions:
- "What does the Bible say about faith?"
- "Explain the book of Romans"
- "What is the meaning of grace?"

## Project Structure

```
versebyverseministry/
├── main.py              # Main entry point with CLI
├── scraper.py           # Web scraper implementation
├── chatbot.py           # Chatbot implementation
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── scraped_content/    # Directory for scraped data (created automatically)
    ├── index.json      # Index of all scraped pages
    └── *.json          # Individual page content files
```

## How It Works

### Scraper

1. Starts at the base URL (versebyverseministry.org)
2. Fetches and parses HTML content
3. Extracts titles, main content, and links
4. Follows links to study materials
5. Saves each page as a JSON file
6. Creates an index of all scraped pages
7. Respects server load with delays between requests

### Chatbot

1. Loads all scraped content from JSON files
2. When user asks a question:
   - Searches for relevant content using keyword matching
   - Scores documents based on relevance
   - Extracts relevant excerpts
   - Presents top results with source citations

## Requirements

- Python 3.7+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0

## Notes

- The scraper respects the target website by implementing delays between requests
- All content is attributed to Verse by Verse Ministry and Stephen Armstrong
- Scraped content is stored locally and not redistributed
- The chatbot only answers questions based on the scraped content

## Future Enhancements

Potential improvements for this project:
- Add support for different Bible translations
- Implement more advanced search algorithms (TF-IDF, semantic search)
- Add a web interface for the chatbot
- Support for exporting content to different formats
- Integration with AI models (OpenAI, etc.) for more sophisticated answers
- Add testing and CI/CD pipeline

## License

This project is intended for educational and personal use. All Bible study content belongs to Verse by Verse Ministry and Stephen Armstrong.

## Author

Created for scraping and analyzing Bible study materials from Verse by Verse Ministry.

## Acknowledgments

- Content source: [Verse by Verse Ministry](http://versebyverseministry.org/)
- Bible teachings by Stephen Armstrong
