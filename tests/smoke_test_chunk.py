from pathlib import Path
import sys

# Ensure project root is on sys.path so this script runs when executed directly
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core import parser

print("Running smoke checks for _chunk_text validations...")

# valid
chunks = parser._chunk_text("x"*2000, chunk_size=800, overlap=100)
print("chunks_ok", len(chunks))

# verify word-boundary behavior
text = ("word " * 50).strip() + " "
chunks = parser._chunk_text(text, chunk_size=30, overlap=5)
print("word-boundary chunks:", len(chunks))
for i, c in enumerate(chunks[:-1]):
    print(f"chunk {i} endswith-space:", c.endswith(" "))

# invalid: overlap == chunk_size
try:
    parser._chunk_text("x", chunk_size=100, overlap=100)
    print("ERROR: expected ValueError for overlap==chunk_size")
except ValueError as e:
    print("caught expected error:", e)

# invalid: chunk_size <= 0
try:
    parser._chunk_text("x", chunk_size=0, overlap=0)
    print("ERROR: expected ValueError for chunk_size==0")
except ValueError as e:
    print("caught expected error:", e)

# invalid: overlap < 0
try:
    parser._chunk_text("x", chunk_size=100, overlap=-1)
    print("ERROR: expected ValueError for negative overlap")
except ValueError as e:
    print("caught expected error:", e)

print("Smoke tests done")
