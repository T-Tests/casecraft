from core.generator import generate_test_suite
from core.exporter import export
from core.output import OutputFormat

suite = generate_test_suite("examples/sample.pdf")

export(
    suite,
    output_format=OutputFormat.excel,
    output_path="outputs/test_cases.xlsx",
)

export(
    suite,
    output_format=OutputFormat.json,
    output_path="outputs/test_cases.json",
)

print("Excel and JSON exports generated.")
