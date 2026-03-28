import os
import re
from typing import Union, IO

from PyPDF2 import PdfReader
from docx import Document


class UnsupportedFileTypeError(Exception):
    """Raised when a file with an unsupported extension is provided to :class:`TextExtractor`."""


class TextExtractor:
    """
    Extracts and normalizes plain text from PDF, DOCX, and TXT files.

    Responsibilities (SRP):
        - File-type detection and text extraction only. Does NOT write files,
          manage uploads, or interact with any external service.
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, file: Union[str, IO]) -> str:
        """
        Extract clean text from a file path or file-like object.

        Args:
            file: An absolute file-system path (``str``) or any file-like
                  object that exposes a ``name`` attribute.

        Returns:
            Normalized plain-text string.

        Raises:
            :class:`UnsupportedFileTypeError`: If the file extension is not
            in :attr:`SUPPORTED_EXTENSIONS`.
        """
        extension = self._detect_file_type(file)

        extractors = {
            ".pdf": self._extract_pdf,
            ".docx": self._extract_docx,
            ".txt": self._extract_txt,
        }

        raw_text = extractors[extension](file)
        return self._normalize_text(raw_text)

    # ------------------------------------------------------------------
    # Private — file-type detection
    # ------------------------------------------------------------------

    def _detect_file_type(self, file: Union[str, IO]) -> str:
        """
        Determine the file extension from a path or file object.

        Args:
            file: File path string or file-like object.

        Returns:
            Lowercase extension string (e.g. ``".pdf"``).

        Raises:
            :class:`UnsupportedFileTypeError`: If the extension is unsupported.
        """
        if isinstance(file, str):
            _, ext = os.path.splitext(file.lower())
        else:
            filename = getattr(file, "name", "")
            _, ext = os.path.splitext(filename.lower())

        if ext not in self.SUPPORTED_EXTENSIONS:
            raise UnsupportedFileTypeError(
                f"File type '{ext}' is not supported. Allowed: {self.SUPPORTED_EXTENSIONS}"
            )

        return ext

    # ------------------------------------------------------------------
    # Private — format-specific extractors
    # ------------------------------------------------------------------

    def _extract_pdf(self, file: Union[str, IO]) -> str:
        reader = PdfReader(file)
        return "\n".join(
            page.extract_text() for page in reader.pages if page.extract_text()
        )

    def _extract_docx(self, file: Union[str, IO]) -> str:
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs if p.text)

    def _extract_txt(self, file: Union[str, IO]) -> str:
        if isinstance(file, str):
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        return file.read().decode("utf-8", errors="ignore")

    # ------------------------------------------------------------------
    # Private — text normalization
    # ------------------------------------------------------------------

    def _normalize_text(self, text: str) -> str:
        """Collapses redundant whitespace and normalizes line endings."""
        text = text.replace("\r", "\n")
        text = re.sub(r"\n+", "\n", text)   # collapse consecutive newlines
        text = re.sub(r"[ \t]+", " ", text)  # collapse horizontal whitespace
        text = re.sub(r"\s+\n", "\n", text)  # trim trailing spaces per line
        return text.strip()
