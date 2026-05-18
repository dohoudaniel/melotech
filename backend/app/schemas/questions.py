"""
Pydantic schemas for the /questions endpoint.

Defines the shape of the incoming request and the outgoing response
so that validation happens automatically before any business logic runs.
"""

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """
    The payload the frontend sends when requesting interview questions.

    Contains a single field: the job title the user typed.
    """

    job_title: str = Field(
        ...,                    # ... (Ellipsis) = required, no default value
        min_length=1,           # FastAPI returns 422 automatically if violated
        max_length=100,         # Secondary cap; frontend enforces 80 chars first
        description="The job title to generate interview questions for.",
        examples=["Customer Success Manager"],
    )


class QuestionItem(BaseModel):
    """
    A single interview question with its category label and rationale.
    """

    category: str = Field(
        ...,
        description="The type of question (e.g. Behavioral, Situational, Technical).",
    )
    question: str = Field(
        ...,
        description="The text of the interview question.",
    )
    why_it_matters: str = Field(
        ...,
        description="A concise explanation of what the interviewer learns from this question.",
    )


class QuestionsResponse(BaseModel):
    """
    The structured response returned to the frontend.

    Always contains exactly 3 question items.
    """

    questions: list[QuestionItem] = Field(
        ...,
        min_length=3,   # Belt-and-suspenders on top of response_parser.py's own count check
        max_length=3,
        description="Exactly 3 generated interview questions.",
    )
