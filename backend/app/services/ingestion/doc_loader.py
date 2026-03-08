from typing import List

from PyPDF2 import PdfReader


def load_pdf(path: str) -> List[str]:
    """Load text content from a PDF file."""
    reader = PdfReader(path)
    texts: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text:
            texts.append(text)
    return texts


def split_text(texts: List[str], chunk_size: int = 500) -> List[str]:
    """Split list of texts into smaller chunks by character length."""
    chunks: List[str] = []
    for text in texts:
        if not text:
            continue
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i : i + chunk_size])
    return chunks

