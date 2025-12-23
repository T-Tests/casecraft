# CaseCraft

Context aware test case generation from feature documents and product knowledge using retrieval augmented generation.

## Overview

CaseCraft is an open source tool that helps QA and engineering teams generate high quality, structured test cases directly from feature documents and product documentation.

Unlike traditional AI based generators that operate on a single input document, CaseCraft uses retrieval augmented generation (RAG) to ground test case creation in shared product knowledge. This enables richer test coverage, including cross feature and integration scenarios that are often missed during manual test design.

The project is designed to work both locally and as a web based service, making it suitable for individual developers, QA engineers, and teams with privacy or deployment constraints.

## Key Capabilities

* Generate structured test cases from PRDs, user stories, and feature documents
* Learn product context from shared documentation using RAG
* Produce cross feature and integration test scenarios
* Support both local execution and web based usage
* Output test cases in machine readable and human readable formats
* Designed for extensibility and open source collaboration

## How It Works

1. Feature documents are parsed and normalized
2. Product documentation is indexed into a knowledge base
3. Relevant context is retrieved using semantic similarity
4. A language model generates test cases grounded in both the feature and product context
5. Output is validated against a defined test case schema

This approach ensures that generated test cases are not isolated to a single requirement but reflect how features behave within the broader product ecosystem.

## Architecture Overview

```
casecraft/
│
├── core/               # Core engine and shared logic
│   ├── parser.py       # Document parsing
│   ├── generator.py    # Test case generation
│   ├── knowledge.py    # Knowledge base indexing
│   ├── retriever.py    # Context retrieval
│   ├── formatter.py   # Output formatting
│   ├── reviewer.py    # Optional refinement pass
│   └── exceptions.py
│
├── cli/                # Local command line interface
│   └── main.py
│
├── web/                # Web API and UI
│   ├── api.py
│   └── ui.py
│
├── knowledge_base/     # Product documentation
├── prompts/            # Prompt templates
├── examples/           # Sample inputs and outputs
└── docs/               # Project documentation
```

## Test Case Structure

CaseCraft generates test cases using a consistent schema to ensure clarity and reuse.

Example structure:

```json
{
  "id": "TC001",
  "title": "User login with valid credentials",
  "priority": "high",
  "type": "functional",
  "preconditions": [
    "User has a registered account"
  ],
  "steps": [
    "Navigate to the login page",
    "Enter valid username and password",
    "Click the login button"
  ],
  "expected_results": [
    "User is redirected to the dashboard"
  ],
  "test_data": {
    "username": "valid_user",
    "password": "valid_password"
  },
  "tags": ["authentication", "happy-path"]
}
```

## Usage Modes

### Local CLI Mode

CaseCraft can be run locally for offline or privacy sensitive use cases.

Example:

```bash
casecraft generate feature.pdf --model llama3.1 --format markdown
```

This mode is ideal for individual developers, local experimentation, and environments where external API calls are restricted.

### Web Mode

CaseCraft can also be run as a web service.

* FastAPI provides a REST API for integration
* A simple web UI allows uploading documents and viewing generated test cases

This mode is suitable for team usage, demos, and internal deployments.

## Models and Retrieval

* Supports local language models via Ollama
* Supports API based models for higher quality generation
* Uses sentence transformer embeddings for semantic retrieval
* Knowledge retrieval is performed using a local vector database

The architecture allows models and retrieval strategies to be swapped without changing core logic.

## Installation (Development)

Basic setup:

```bash
git clone https://github.com/<your-username>/casecraft.git
cd casecraft
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Further setup instructions will be expanded as features mature.

## Project Status

CaseCraft is under active development.

Current focus areas:

* Core test case generation
* Knowledge base ingestion
* Retrieval quality
* CLI stability
* Web API foundations

Expect breaking changes until the first stable release.

## Roadmap (High Level)

* Improve cross feature reasoning quality
* Add export formats for test management tools
* Enhance knowledge base indexing
* Add validation and review workflows
* Improve documentation and examples

## Contributing

Contributions are welcome.

Please see CONTRIBUTING.md for guidelines on reporting issues, proposing changes, and submitting pull requests.

## License

CaseCraft is licensed under the Apache License, Version 2.0.
You are free to use, modify, and distribute this software in compliance with the license.
See the LICENSE file for full details.
