from langgraph.graph import MessagesState
from pydantic import BaseModel, Field


class State(MessagesState):
    """
        Class that manages and maintains the message state across the workflow execution.
        Stores and updates inputs, intermediate outputs, and metadata required for routing and processing nodes within the workflow.
    """
    experience : str
    skill : str
    complexity : int
    question : str
    answer : str
    correctness : str
    sentiment : str
    grammer_quality : str
    confidence : str
    length_score : str

class EvaluatorFormat(BaseModel):
    """
       Pydantic model for formatting and validating the LLM-generated evaluation of an interview answer.
    """
    correctness: str = Field(
        description="Rate the factual correctness of the answer on a scale of 0 to 10."
    )
    sentiment: str = Field(
        description="Classify the sentiment of the answer as 'positive', 'neutral', or 'negative'."
    )
    grammer_quality: str = Field(
        description="Rate the grammatical quality of the answer on a scale of 0 to 10."
    )
    confidence: str = Field(
        description="Rate the level of confidence expressed in the answer on a scale of 0 to 10."
    )
    length_score : str = Field(
        description="Score the length of the answer on a scale from 0 to 10"
    )
