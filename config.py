"""
Configuration settings for the PDF scraper and chatbot
"""

# Website configuration
BASE_URL = "https://www.versebyverseministry.org"

# Scraper settings
PDF_SAVE_DIR = "pdfs"
MAX_RETRIES = 3
TIMEOUT = 30  # seconds
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Chatbot settings
VECTOR_DB_DIR = "chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COLLECTION_NAME = "vbvm_pdfs"

# OpenAI settings (can be overridden by environment variables)
OPENAI_API_KEY = None  # Set in .env file or environment
MODEL_NAME = "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"  # Updated to newer model
TEMPERATURE = 0.7
MAX_TOKENS = 500

# Search settings
TOP_K_RESULTS = 5  # Number of relevant chunks to retrieve
