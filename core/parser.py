from pathlib import Path
from typing import List, Union
from os import PathLike

from pypdf import PdfReader


class DocumentParseError(Exception):
    pass


def parse_pdf(file_path: Union[str, Path, PathLike]) -> str:
    """
    Extracts text from a PDF file and returns it as a single string.

    Tries `pypdf` first and falls back to `pdfplumber` if no text was extracted.
    Encrypted PDFs (that cannot be decrypted with an empty password) are
    reported as unsupported.
    """
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        reader = PdfReader(str(path))

        # Handle encrypted PDFs
        if getattr(reader, "is_encrypted", False):
            try:
                # try empty-password decryption (common for PDFs with no password)
                reader.decrypt("")
            except Exception:
                raise DocumentParseError("Encrypted PDFs are not supported")

        pages_text: List[str] = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)

        # Fallback to pdfplumber if pypdf extracted nothing
        if not pages_text:
            try:
                import pdfplumber

                with pdfplumber.open(str(path)) as pdf:
                    for p in pdf.pages:
                        text = p.extract_text()
                        if text:
                            pages_text.append(text)
            except Exception:
                # If pdfplumber isn't available or fails, we'll raise below
                pass

        if not pages_text:
            raise DocumentParseError("No extractable text found in PDF")

        return "\n".join(pages_text)

    except DocumentParseError:
        raise
    except Exception as exc:
        raise DocumentParseError(f"Failed to parse PDF: {exc}") from exc


def parse_document(file_path: Union[str, Path, PathLike]) -> str:
    """
    Entry point for document parsing.
    Detects file type and routes to the appropriate parser.
    """
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return parse_pdf(path)

    if suffix in [".txt", ".md"]:
        try:
            return path.read_text(encoding="utf-8")
        except Exception as exc:
            raise DocumentParseError(f"Failed to read text file: {exc}") from exc

    raise DocumentParseError(f"Unsupported file type: {suffix}")
