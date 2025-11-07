# Verse by Verse Ministry Web Scraper & Chatbot

A Python-based web scraper and AI-powered chatbot that extracts PDF documents from versebyverseministry.org and uses them to answer questions about the ministry's teachings.

## Features

- 🕷️ **Web Scraper**: Automatically discovers and downloads PDF files from the website
- 📄 **PDF Processing**: Extracts text content from downloaded PDFs
- 🤖 **RAG-Based Chatbot**: Uses Retrieval-Augmented Generation to answer questions based only on the PDF content
- 💾 **Vector Database**: Efficiently stores and retrieves document chunks using ChromaDB
- 🔍 **Source Citations**: Shows which documents were used to answer questions

## Requirements

- Python 3.8 or higher
- OpenAI API key (for the chatbot functionality)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rickettlayne/versebyverseministry.git
cd versebyverseministry
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Quick Start (Scrape and Chat)

Run both scraping and chatbot in one command:
```bash
python main.py --scrape --chat
```

### Scrape PDFs Only

To download PDFs from the website:
```bash
python main.py --scrape
```

You can control the crawl depth (default is 2):
```bash
python main.py --scrape --depth 3
```

### Run Chatbot Only

If you've already scraped PDFs:
```bash
python main.py --chat
```

To re-index all PDFs:
```bash
python main.py --chat --reindex
```

### Interactive Mode

Once the chatbot starts, you can ask questions:
```
You: What is the mission of Verse by Verse Ministry?
Assistant: The mission is to provide verse-by-verse Bible teaching...

Sources: example.pdf
```

Type 'quit' or 'exit' to end the conversation.

## Project Structure

```
versebyverseministry/
├── main.py              # Main entry point
├── pdf_scraper.py       # Web scraper for PDFs
├── pdf_processor.py     # PDF text extraction
├── chatbot.py           # RAG-based chatbot
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment file
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## How It Works

1. **Web Scraping**: The scraper crawls versebyverseministry.org to discover PDF links
2. **PDF Download**: All found PDFs are downloaded to the `pdfs/` directory
3. **Text Extraction**: PyPDF2 extracts text content from each PDF
4. **Chunking**: Documents are split into manageable chunks with overlap
5. **Embedding**: Text chunks are converted to embeddings using OpenAI's API
6. **Vector Storage**: Embeddings are stored in ChromaDB for efficient retrieval
7. **Question Answering**: When you ask a question:
   - Your question is embedded
   - Similar document chunks are retrieved
   - An AI model generates an answer based only on those chunks

## Configuration

You can customize the behavior by editing `config.py`:

- `BASE_URL`: Website to scrape
- `PDF_SAVE_DIR`: Directory to save PDFs
- `CHUNK_SIZE`: Size of text chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `MODEL_NAME`: OpenAI model to use (default: gpt-3.5-turbo)
- `TOP_K_RESULTS`: Number of relevant chunks to retrieve (default: 5)

## Individual Module Usage

### Run scraper independently:
```bash
python pdf_scraper.py
```

### Process PDFs independently:
```bash
python pdf_processor.py
```

### Run chatbot independently:
```bash
python chatbot.py
```

## Troubleshooting

### No PDFs found
- Check your internet connection
- Ensure the website is accessible
- Try increasing the crawl depth with `--depth`

### Chatbot errors
- Ensure you have set your OpenAI API key correctly
- Check that PDFs have been downloaded and processed
- Try re-indexing with `--reindex`

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.8 or higher

## Security Note

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or pull requests to improve this project.
