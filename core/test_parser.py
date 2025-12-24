from pathlib import Path
import sys

# When executing this file directly, make sure the project root is on sys.path
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.parser import parse_document


def main() -> None:
    """Run a simple parse and print diagnostics.

    This script is intended to be executable directly: `python core/test_parser.py`.
    It prints the total number of characters extracted, number of chunks, and a short preview.
    """

    file_path = "examples/sample.pdf"  # change name if needed

    chunks = parse_document(file_path)
    full_text = "".join(chunks)

    print("Characters extracted:", len(full_text))
    print("Number of chunks:", len(chunks))
    print("Preview:")
    print(full_text[:1000])


if __name__ == "__main__":
    main()

