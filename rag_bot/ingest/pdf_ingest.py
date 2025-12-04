from dotenv import load_dotenv
load_dotenv()

import os
import io
from typing import List

from pypdf import PdfReader
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from .config import CHROMA_PATH, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from .db import log_event


# ---------------------------------------------------------------------
# 1. Load OpenAI embedding function using API key from .env
# ---------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in your .env file")


embedder = OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)


# ---------------------------------------------------------------------
# 2. Initialize persistent chroma client + collection
# ---------------------------------------------------------------------
client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedder,
)


# ---------------------------------------------------------------------
# 3. Utility: clear/reset the vector store
# ---------------------------------------------------------------------
def clear_vector_store():
    collections = client.list_collections()
    for col in collections:
        client.delete_collection(name=col.name)
    print("Vector store cleared.")


# ---------------------------------------------------------------------
# 4. Extract text from PDF
# ---------------------------------------------------------------------
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        pages.append(txt)
    return "\n".join(pages)


# ---------------------------------------------------------------------
# 5. Chunk text into overlapping windows
# ---------------------------------------------------------------------
def chunk_text(text: str, size: int, overlap: int) -> List[str]:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += size - overlap

    return chunks


# ---------------------------------------------------------------------
# 6. Ingest a single PDF
# ---------------------------------------------------------------------
def ingest_pdf(url: str, pdf_bytes: bytes):
    log_event(url, "start_ingest")

    # Extract text
    text = extract_text_from_pdf(pdf_bytes)

    # Chunk text
    chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

    # Build ids + metadata
    ids = []
    metadatas = []

    for idx, chunk in enumerate(chunks):
        ids.append(f"{url}#chunk{idx}")
        metadatas.append({"source": url, "chunk_index": idx})

    # Insert into vector database
    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    log_event(url, f"ingested_chunks_{len(chunks)}")
    print(f"Ingested {len(chunks)} chunks from: {url}")
