"""
Parser service for extracting and normalizing text from files.
PDFs use pdfplumber, fallback to text decode.
"""
from fastapi import UploadFile
from typing import Optional, List
import pdfplumber
import re
import unicodedata

async def extract_text(file: UploadFile) -> str:
    if file.content_type == "application/pdf":
        with pdfplumber.open(file.file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return text
    else:
        data = await file.read()
        return data.decode("utf-8", "ignore")

def normalize_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def split_sections(text: str) -> dict:
    # Simple regex for headings
    sections = {}
    for section in ["skills", "experience", "education"]:
        match = re.search(rf"(?i)({section})[:\s]*([\s\S]+?)(?=skills|experience|education|$)", text)
        if match:
            sections[section] = match.group(2).strip()
    return sections
