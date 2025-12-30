from core.generator import generate_test_suite

suite = generate_test_suite(
    file_path="examples/sample.pdf",
)

print(suite.model_dump_json(indent=2))
