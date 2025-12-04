import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .config import BASE_URL
from .db import get_document, upsert_document, log_event

# BASE_URL in config.py:
# BASE_URL = "https://versebyverseministry.org/bible-studies"

def get_study_pages() -> list[str]:
    resp = requests.get(BASE_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    study_urls = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # study URLs contain "/study/" or "/books/" patterns
        if "study" in href or "book" in href:
            full = urljoin(BASE_URL, href)
            study_urls.append(full)

    return sorted(set(study_urls))

def extract_pdfs_from_page(url: str) -> list[str]:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    pdfs = []
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if href.endswith(".pdf"):
            full = urljoin(url, href)
            pdfs.append(full)

    return pdfs

def list_pdf_links() -> list[str]:
    log_event(BASE_URL, "scan_study_index")
    study_pages = get_study_pages()

    pdfs = []
    for study_url in study_pages:
        log_event(study_url, "scan_study_page")
        found = extract_pdfs_from_page(study_url)
        for f in found:
            pdfs.append(f)

    return sorted(set(pdfs))

def download_pdf(url: str) -> bytes:
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    return resp.content

def checksum_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def get_pdfs_to_process() -> list[tuple[str, bytes]]:
    pdf_urls = list_pdf_links()

    results = []
    for url in pdf_urls:
        log_event(url, "found_pdf_url")
        pdf_bytes = download_pdf(url)
        cs = checksum_bytes(pdf_bytes)

        existing = get_document(url)
        if existing and existing[2] == cs:
            log_event(url, "unchanged_skip")
            continue

        log_event(url, "changed_or_new")
        upsert_document(url, cs)
        results.append((url, pdf_bytes))

    return results
