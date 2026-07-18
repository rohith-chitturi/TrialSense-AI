from typing import TypedDict, Annotated, Sequence, Any
import operator
from langchain_core.messages import BaseMessage

class PatientState(TypedDict):
    """
    LangGraph state schema for TrialSense Multi-Agent Workflow.
    Tracks memory, decisions, and observations between agents.
    """
    patient_id: str
    fhir_data: dict
    unstructured_documents: list[str]
    
    # State accumulated by agents
    extracted_conditions: list[str]
    extracted_medications: list[str]
    
    # Knowledge Graph & Vector Store Results
    similar_patients: list[str]
    retrieved_trials: list[dict]
    
    # Final AI Outputs
    confidence_scores: dict
    eligibility_decisions: dict
    
    # Message history for agent memory
    messages: Annotated[Sequence[BaseMessage], operator.add]
