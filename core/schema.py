from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    """
    Represents a single test case.
    """

    id: str = Field(
        ...,
        description="Unique test case identifier, e.g. TC_LOGIN_001"
    )

    title: str = Field(
        ...,
        description="Short, descriptive test case title"
    )

    priority: str = Field(
        ...,
        description="Priority of the test case: high, medium, or low"
    )

    type: str = Field(
        ...,
        description="Type of test case: functional, integration, negative, boundary"
    )

    preconditions: List[str] = Field(
        default_factory=list,
        description="Conditions that must be true before executing the test"
    )

    steps: List[str] = Field(
        ...,
        description="Ordered list of steps to execute the test"
    )

    expected_results: List[str] = Field(
        ...,
        description="Expected outcome for each step or for the test as a whole"
    )

    test_data: Dict[str, str] = Field(
        default_factory=dict,
        description="Input data required to execute the test"
    )

    tags: List[str] = Field(
        default_factory=list,
        description="Labels for grouping or filtering test cases"
    )


class TestSuite(BaseModel):
    """
    Represents a collection of test cases generated from a document.
    """

    feature_name: str = Field(
        ...,
        description="Name of the feature under test"
    )

    source_document: str = Field(
        ...,
        description="Source document used to generate the test cases"
    )

    test_cases: List[TestCase] = Field(
        ...,
        description="List of generated test cases"
    )
