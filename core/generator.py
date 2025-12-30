import json
import requests
from typing import List

from core.schema import TestSuite
from core.parser import parse_document


class GenerationError(Exception):
    pass


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.1:8b"


def _build_prompt(chunks: List[str]) -> str:
    """
    Build a strict prompt that forces schema-aligned JSON output.
    """
    joined_text = "\n\n".join(chunks)

    return f"""
You are a QA engineer.

If you cannot generate valid JSON, return an empty JSON object: {{}}.

Generate detailed test cases from the following feature documentation.

STRICT RULES:
- Return ONLY valid JSON
- Do NOT add explanations
- Do NOT add markdown
- Do NOT add extra text
- Follow this exact schema
- Generate at most 8 test cases


Schema:
{{
  "feature_name": "string",
  "source_document": "string",
  "test_cases": [
    {{
      "use_case": "string",
      "test_case": "string",
      "preconditions": ["string"],
      "test_data": {{"key": "value"}},
      "steps": ["string"],
      "priority": "high | medium | low",
      "tags": ["string"],
      "expected_results": ["string"],
      "actual_results": []
    }}
  ]
}}

Feature documentation:
{joined_text}
"""


def _format_validation_error(error: Exception) -> str:
    """
    Convert schema validation errors into a concise string for the LLM.
    """
    return str(error)


def generate_test_suite(
    file_path: str,
    model: str = DEFAULT_MODEL,
    max_retries: int = 2,
) -> TestSuite:
    """
    Generate a TestSuite from a document using a local LLM
    with retry and self-correction.
    """
    chunks = parse_document(file_path)
    base_prompt = _build_prompt(chunks)

    last_error: Exception | None = None
    corrective_feedback: str | None = None

    for attempt in range(max_retries + 1):
        if corrective_feedback:
            prompt = (
                base_prompt
                + "\n\nThe previous output had the following errors:\n"
                + corrective_feedback
                + "\n\nFix the JSON output to strictly match the schema."
            )
        else:
            prompt = base_prompt

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "num_predict": 1200
            },
        }

        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            raise GenerationError(
                f"Ollama request failed: {response.status_code} {response.text}"
            )

        try:
            result = response.json()["response"]
        except Exception as exc:
            last_error = exc
            corrective_feedback = "Missing 'response' field in Ollama output."
            continue

        if isinstance(result, str):
            result = result.strip()
            if not result:
                last_error = GenerationError("Empty output returned by model.")
                corrective_feedback = "The output was empty. Return full valid JSON."
                continue
            try:
                result = json.loads(result)
            except json.JSONDecodeError as exc:
                last_error = exc
                corrective_feedback = (
                    "The output was not valid JSON. "
                    "Return only valid JSON with no extra text."
                )
                continue

        if not isinstance(result, dict):
            last_error = GenerationError(
                f"Expected JSON object, got {type(result).__name__}"
            )
            corrective_feedback = "Top-level output must be a JSON object."
            continue

        try:
            return TestSuite.model_validate(result)
        except Exception as exc:
            last_error = exc
            corrective_feedback = _format_validation_error(exc)
            continue

    raise GenerationError(
        "Failed to generate valid test cases after retries."
    ) from last_error

