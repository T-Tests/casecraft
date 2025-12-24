from core.parser import parse_document

file_path = "examples/sample.pdf"  # change name if needed

text = parse_document(file_path)

print("Characters extracted:", len(text))
print("Preview:")
print(text[:1000])
