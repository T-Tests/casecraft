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
    joined_text = "\n\n".join(chunks)

    return f"""
Think like a senior QA engineer designing tests for production systems.
Generate test cases from the following feature documentation.

STRICT RULES:
- Return ONLY valid JSON
- Do NOT add explanations
- Do NOT add markdown
- Do NOT add extra text
- Return a JSON ARRAY, not an object
- Include positive, negative, and edge cases where applicable
- Generate at most 3 test cases

Each test case must follow this schema:

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

Feature documentation:
{joined_text}
"""



def _condense_chunk(chunk: str, model: str) -> str:
    """
    Reduce a document chunk to concise, test relevant bullet points.
    """
    prompt = f"""
Summarize the following feature description into concise,
test relevant bullet points.

Rules:
- Focus on behaviors, inputs, outputs, and rules
- Exclude explanations and fluff
- Keep it under 10 bullet points
- Use plain text
- No JSON
- No markdown

Feature text:
{chunk}
"""

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 200,
            "temperature": 0.2,
        },
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        raise GenerationError("Chunk condensation failed")

    condensed = response.json().get("response", "")
    if not condensed or not isinstance(condensed, str):
        raise GenerationError("Empty condensed chunk returned")

    return condensed.strip()


def _generate_single_suite(
    prompt: str,
    model: str,
    max_retries: int,
) -> list:
    last_error: Exception | None = None
    corrective_feedback: str | None = None

    for _ in range(max_retries + 1):
        final_prompt = (
            prompt
            if corrective_feedback is None
            else (
                prompt
                + "\n\nThe previous output was invalid:\n"
                + corrective_feedback
                + "\n\nReturn a complete JSON array only."
            )
        )

        payload = {
            "model": model,
            "prompt": final_prompt,
            "stream": False,
            "format": "json",
            "options": {"num_predict": 300},
        }

        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            last_error = GenerationError(f"Ollama request failed: {response.status_code} {response.text!r}")
            continue

        try:
            response_json = response.json()
        except Exception as exc:
            last_error = exc
            corrective_feedback = "Response was not valid JSON."
            continue

        result = response_json.get("response")

        if isinstance(result, str):
            try:
                import json
                result = json.loads(result)
            except Exception as exc:
                last_error = exc
                corrective_feedback = "JSON array was incomplete or invalid."
                continue

        # Normalize output shapes
        if isinstance(result, list):
            return result

        if isinstance(result, dict):
            # Common explicit fields
            if "test_cases" in result and isinstance(result["test_cases"], list):
                return result["test_cases"]
            if "cases" in result and isinstance(result["cases"], list):
                return result["cases"]

            # If the model returned a single test case object (not wrapped in a list),
            # accept it by wrapping in a list to normalize the shape.
            if any(k in result for k in ("test_case", "use_case")):
                return [result]

            # Fallback: try to find the first list value that looks like test cases
            for key, value in result.items():
                if isinstance(value, list) and value and all(isinstance(i, dict) for i in value):
                    return value

            # Surface model-side error messages if present, otherwise include the raw response
            if "error" in result:
                last_error = GenerationError(f"Model returned an error: {result['error']}")
            else:
                last_error = GenerationError(
                    f"Could not normalize test cases from model output. Response: {result!r}"
                )

            corrective_feedback = (
                "Return test cases as a JSON array, "
                "or inside a 'test_cases' field."
            )
            continue

        # Unknown shape -> retry with corrective feedback
        last_error = GenerationError("Unexpected model output shape")
        corrective_feedback = "Return only a JSON array of test case objects."
        continue

    raise GenerationError(
        "Failed to generate valid test cases after retries."
    ) from last_error


def _generate_from_chunks(
    chunks: List[str],
    model: str,
    max_retries: int,
) -> List[dict]:
    """
    Generate test cases independently for each chunk.
    """
    all_test_cases: List[dict] = []

    for index, chunk in enumerate(chunks):
        condensed = _condense_chunk(chunk, model)
        chunk_prompt = _build_prompt([condensed])

        try:
            test_cases = _generate_single_suite(
                prompt=chunk_prompt,
                model=model,
                max_retries=max_retries,
            )
            all_test_cases.extend(test_cases)
        except GenerationError as exc:
            raise GenerationError(
                f"Failed to generate test cases for chunk {index}"
            ) from exc

    return all_test_cases

def _deduplicate_test_cases(test_cases: list[dict]) -> list[dict]:
    seen = set()
    unique = []

    for tc in test_cases:
        key = (
            str(tc.get("use_case", "")).strip().lower(),
            str(tc.get("test_case", "")).strip().lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(tc)

    return unique


def generate_test_suite(
    file_path: str,
    model: str = DEFAULT_MODEL,
    max_retries: int = 2,
) -> TestSuite:
    """
    Generate a TestSuite using chunk wise generation.
    """
    chunks = parse_document(file_path)

    raw_test_cases = _deduplicate_test_cases(
    _generate_from_chunks(
        chunks=chunks,
        model=model,
        max_retries=max_retries,
    )
)


    merged_suite = {
        "feature_name": "Generated Feature",
        "source_document": file_path,
        "test_cases": raw_test_cases,
    }

    try:
        return TestSuite.model_validate(merged_suite)
    except Exception as exc:
        raise GenerationError(
            "Merged test cases failed schema validation"
        ) from exc
