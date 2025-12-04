from .db import init_db, clear_all
from .crawler import get_pdfs_to_process
from .pdf_ingest import ingest_pdf, clear_vector_store

def run_ingest(full_reset: bool = False):
    init_db()
    if full_reset:
        clear_all()
        clear_vector_store()

    pdfs = get_pdfs_to_process()
    for url, pdf_bytes in pdfs:
        ingest_pdf(url, pdf_bytes)

if __name__ == "__main__":
    # full_reset = True means wipe and rebuild
    run_ingest(full_reset=False)
