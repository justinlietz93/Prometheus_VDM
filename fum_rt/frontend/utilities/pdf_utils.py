from __future__ import annotations

"""
PDF -> Text utilities (bounded, best-effort, dependency-optional)

Design:
- Try light, pure extraction first (no OCR) using available libs in this order:
  1) PyMuPDF (fitz)
  2) pdfminer.six
  3) PyPDF2
- If those produce too little text, optionally fallback to OCR if pytesseract + pdf2image are available.
- Write result to an output .txt path and return it along with the method used.
- Bounded IO: operate only on the provided file, no recursion. No scans in core/ or maps/.

Returns:
- (out_path, method) when successful, where method in {"pymupdf", "pdfminer", "pypdf2", "ocr"}
- (None, "") if conversion not possible or failed.

Notes:
- OCR requires poppler (for pdf2image) and Tesseract installed; function degrades gracefully if missing.
- Keep memory and compute usage modest; OCR dpi kept moderate (e.g., 200).
"""

import os
from typing import Tuple, Optional


_MIN_TEXT_CHARS = 64  # minimal payload to consider extraction successful


def _write_text(out_path: str, text: str) -> bool:
    try:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return True
    except Exception:
        return False


def _try_pymupdf(pdf_path: str) -> Optional[str]:
    try:
        import fitz  # PyMuPDF
    except Exception:
        return None
    try:
        text_parts = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text_parts.append(page.get_text() or "")
        text = "\n".join(text_parts)
        return text
    except Exception:
        return None


def _try_pdfminer(pdf_path: str) -> Optional[str]:
    try:
        from pdfminer.high_level import extract_text
    except Exception:
        return None
    try:
        return extract_text(pdf_path) or ""
    except Exception:
        return None


def _try_pypdf2(pdf_path: str) -> Optional[str]:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        return None
    try:
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            try:
                text_parts.append(page.extract_text() or "")
            except Exception:
                continue
        return "\n".join(text_parts)
    except Exception:
        return None


def _try_ocr(pdf_path: str, dpi: int = 200) -> Optional[str]:
    """
    OCR fallback using pdf2image + pytesseract, if both available and system supports them.
    """
    try:
        from pdf2image import convert_from_path
        import pytesseract
    except Exception:
        return None
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        text_parts = []
        for im in images:
            try:
                text_parts.append(pytesseract.image_to_string(im) or "")
            except Exception:
                continue
        return "\n".join(text_parts)
    except Exception:
        return None


def convert_pdf_to_text_file(pdf_path: str, out_dir: str) -> Tuple[Optional[str], str]:
    """
    Convert a PDF to a UTF-8 .txt file.

    Args:
        pdf_path: absolute or relative path to the .pdf file
        out_dir: directory to write the .txt sidecar into

    Returns:
        (out_txt_path, method) on success; (None, "") on failure
    """
    try:
        base = os.path.splitext(os.path.basename(pdf_path))[0] or "document"
        out_txt = os.path.join(out_dir, f"{base}.txt")
    except Exception:
        return None, ""

    # 1) PyMuPDF
    text = _try_pymupdf(pdf_path)
    if text and len(text.strip()) >= _MIN_TEXT_CHARS:
        return (out_txt, "pymupdf") if _write_text(out_txt, text) else (None, "")

    # 2) pdfminer
    text = _try_pdfminer(pdf_path)
    if text and len(text.strip()) >= _MIN_TEXT_CHARS:
        return (out_txt, "pdfminer") if _write_text(out_txt, text) else (None, "")

    # 3) PyPDF2
    text = _try_pypdf2(pdf_path)
    if text and len(text.strip()) >= _MIN_TEXT_CHARS:
        return (out_txt, "pypdf2") if _write_text(out_txt, text) else (None, "")

    # 4) OCR fallback
    text = _try_ocr(pdf_path, dpi=200)
    if text and len(text.strip()) >= _MIN_TEXT_CHARS:
        return (out_txt, "ocr") if _write_text(out_txt, text) else (None, "")

    return None, ""