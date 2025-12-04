import io
from typing import List

from pypdf import PdfReader
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from .config import CHROMA_PATH, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP
from .db import log_event

embedder = OpenAIEmbeddingFunction(
    api_key="YOUR_OPENAI_KEY",  # env variable in real code
    model_name="text-embedding-3-small"
)

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedder
)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        pages.append(txt)
    return "\n".join(pages)

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

def ingest_pdf(url: str, pdf_bytes: bytes):
    log_event(url, "start_ingest")
    text = extract_text_from_pdf(pdf_bytes)
    chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

    ids = []
    metadatas = []
    for idx, chunk in enumerate(chunks):
        ids.append(f"{url}#chunk{idx}")
        metadatas.append({"source": url, "chunk_index": idx})

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )
    log_event(url, f"ingested_chunks_{len(chunks)}")
