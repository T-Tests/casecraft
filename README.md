# CaseCraft

Context aware test case generation from feature documents using schema driven AI generation, with a roadmap toward retrieval augmented generation.

---

## Overview

CaseCraft is an open source tool that helps QA and engineering teams generate high quality, structured test cases directly from feature documents and product documentation.

The current version focuses on **local, schema validated test case generation** using a local large language model. The architecture is intentionally designed to evolve toward retrieval augmented generation (RAG), enabling future support for cross feature and integration test scenarios grounded in shared product knowledge.

CaseCraft is designed to run locally for privacy sensitive environments and is being built with extensibility in mind for future CLI and web based usage.

---

## Current Capabilities

- Parse feature documents (PDF, TXT, Markdown)
- Normalize and chunk large documents
- Generate structured test cases using a local LLM (Ollama)
- Enforce a strict, documented test case schema
- Automatically retry and self correct invalid AI output
- Export test cases to Excel and JSON formats
- Run fully locally without external API dependencies

---

## Planned Capabilities

- Product knowledge ingestion using RAG
- Cross feature and integration test case generation
- CLI interface for local usage
- Web API and UI for team usage
- Additional export formats (CSV, TestRail, Jira)

---

## How It Works (Current)

1. Feature documents are parsed and normalized
2. Large documents are split into manageable chunks
3. A local language model generates structured test cases
4. Output is validated against a defined test case schema
5. Invalid output is corrected automatically through retries
6. Final results are exported to Excel or JSON

This ensures reliable, repeatable test case generation suitable for real QA workflows.

---

## Architecture Overview (Current)

```
casecraft/
│
├── core/
│   ├── parser.py        # Document parsing and chunking
│   ├── schema.py        # Test case schema definition
│   ├── generator.py    # LLM based generation with retries
│   ├── exporter.py     # Excel and JSON exporters
│   ├── output.py       # Output format definitions
│   └── __init__.py
│
├── examples/            # Sample input documents
├── outputs/             # Generated outputs
├── cli/                 # Reserved for future CLI
├── web/                 # Reserved for future web API
└── README.md
```

Directories for CLI, web, and knowledge base are placeholders and will be implemented incrementally.

---

## Test Case Structure

CaseCraft generates test cases using a consistent schema aligned with real QA workflows.

Example structure:

```json
{
  "feature_name": "User Authentication",
  "source_document": "login_feature.pdf",
  "test_cases": [
    {
      "use_case": "User Login",
      "test_case": "Login with valid credentials",
      "preconditions": ["User has a registered account"],
      "test_data": {
        "username": "valid_user",
        "password": "valid_password"
      },
      "steps": [
        "Navigate to the login page",
        "Enter valid username and password",
        "Click the login button"
      ],
      "priority": "high",
      "tags": ["authentication", "happy-path"],
      "expected_results": ["User is successfully logged in"],
      "actual_results": []
    }
  ]
}
```

---

## Usage (Current)

Run the generator and exporter locally.

```bash
python -m core.test_generator
python -m core.test_exporter
```

These commands validate the full pipeline from document parsing to Excel and JSON output.

CLI commands shown in this README are planned and not yet implemented.

---

## Models

- Local language models via Ollama
- Tested with Llama 3.1 8B
- Model selection is configurable in code

Future versions may support API based models and hybrid configurations.

---

## Installation (Development)

```bash
git clone https://github.com/T-Tests/casecraft.git
cd casecraft
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Ensure Ollama is installed and running with a supported model.

---

## Project Status

CaseCraft is under active development.

Current focus areas:

- Generator robustness and correctness
- Chunk wise generation
- Schema evolution
- RAG groundwork

Breaking changes are expected until the first stable release.

---

## Roadmap

- Chunk wise test case generation and merging
- Product knowledge base using RAG
- Cross feature test case generation
- CLI interface
- Web API
- Additional export formats

---

## Contributing

Contributions are welcome.

Please see CONTRIBUTING.md for guidelines on reporting issues, proposing changes, and submitting pull requests.

---

## License

CaseCraft is licensed under the Apache License, Version 2.0.

You are free to use, modify, and distribute this software in compliance with the license.
See the LICENSE file for full details.
