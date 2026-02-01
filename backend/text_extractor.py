import os
import re
from typing import Union, IO

from PyPDF2 import PdfReader
from docx import Document


class UnsupportedFileTypeError(Exception):
    """Raised when an unsupported file type is provided."""
    pass


class TextExtractor:
    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

    def extract(self, file: Union[str, IO]) -> str:
        """
        Extract clean text from a file path or file-like object.
        """
        extension = self._detect_file_type(file)

        if extension == ".pdf":
            text = self._extract_pdf(file)
        elif extension == ".docx":
            text = self._extract_docx(file)
        elif extension == ".txt":
            text = self._extract_txt(file)
        else:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {extension}"
            )

        return self._normalize_text(text)

    # -------------------------------
    # File type detection
    # -------------------------------
    def _detect_file_type(self, file: Union[str, IO]) -> str:
        if isinstance(file, str):
            _, ext = os.path.splitext(file.lower())
        else:
            filename = getattr(file, "name", "")
            _, ext = os.path.splitext(filename.lower())

        if ext not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(f"File type {ext} not supported")

        return ext

    # -------------------------------
    # Extractors
    # -------------------------------
    def _extract_pdf(self, file: Union[str, IO]) -> str:
        reader = PdfReader(file)
        text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return "\n".join(text)

    def _extract_docx(self, file: Union[str, IO]) -> str:
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs if p.text)

    def _extract_txt(self, file: Union[str, IO]) -> str:
        if isinstance(file, str):
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            return file.read().decode("utf-8", errors="ignore")

    # -------------------------------
    # Normalization
    # -------------------------------
    def _normalize_text(self, text: str) -> str:
        text = text.replace("\r", "\n")
        text = re.sub(r"\n+", "\n", text)        # collapse newlines
        text = re.sub(r"[ \t]+", " ", text)      # collapse spaces
        text = re.sub(r"\s+\n", "\n", text)      # trim line endings
        return text.strip()
