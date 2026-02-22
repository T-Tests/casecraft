
import os
from typing import List, Optional
from jinja2 import Environment, FileSystemLoader

# Define the path to templates
# Assuming templates are in "prompts/templates" relative to the project root
# or a specific configured path.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "prompts", "templates")

# Initialize Jinja2 Environment
try:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
except Exception as e:
    # Fallback or error logging if needed, essentially hard to recov if templates missing
    print(f"Error loading templates from {TEMPLATES_DIR}: {e}")
    env = None

def render_template(template_name: str, **kwargs) -> str:
    """Helper to render a template safely."""
    if not env:
        raise RuntimeError(f"Template environment not initialized. Checked {TEMPLATES_DIR}")
    try:
        template = env.get_template(template_name)
        return template.render(**kwargs)
    except Exception as e:
        raise RuntimeError(f"Failed to render template {template_name}: {e}")

def build_generation_prompt(
    feature_chunks: List[str], 
    product_context: str,
    app_type: str = "web"
) -> str:
    """
    Constructs the main prompt for test case generation.
    """
    joined_feature_text = "\n\n".join(feature_chunks)
    
    context_section = ""
    if product_context:
        context_section = f"""
Product context (from existing product documentation):
{product_context}

Use this context to:
- Identify cross feature interactions
- Cover integration scenarios
- Avoid contradicting existing behavior
"""

    return render_template(
        "generation.j2",
        feature_text=joined_feature_text,
        context_section=context_section,
        app_type=app_type
    )

def build_cross_reference_prompt(existing_tests_json: str, checklist_text: str) -> str:
    """
    Prompt for reviewing an existing test suite against a required checklist
    and generating only the missing scenarios.
    """
    return render_template(
        "checklist_cross_reference.j2", 
        existing_tests_json=existing_tests_json, 
        checklist_text=checklist_text
    )

def build_condensation_prompt(chunk: str) -> str:
    """
    Prompt for condensing document chunks into test-relevant bullet points.
    """
    return render_template("condensation.j2", chunk=chunk)

def build_reviewer_prompt(current_json: str) -> str:
    """
    Prompt for reviewing and improving test suite quality.
    """
    return render_template("reviewer.j2", current_json=current_json)
