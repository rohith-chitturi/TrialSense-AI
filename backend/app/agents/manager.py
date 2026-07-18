from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from .state import PatientState
import logging

def extraction_agent(state: PatientState):
    logging.info("Extraction Agent running...")
    # In practice: Use LLM to extract from unstructured documents
    # and map to standard Ontology via RAG
    state["extracted_conditions"] = ["E11 - Type 2 Diabetes Mellitus"]
    return state

def eligibility_agent(state: PatientState):
    logging.info("Eligibility Agent running...")
    # In practice: Check criteria against conditions/meds
    state["eligibility_decisions"] = {"Trial_A": "Eligible"}
    state["confidence_scores"] = {"Trial_A": 91}
    return state

def explainability_agent(state: PatientState):
    logging.info("Explainability Agent running...")
    # Calibrate confidence and generate explanation
    return state

def build_workflow():
    workflow = StateGraph(PatientState)
    
    # Add nodes (Agents)
    workflow.add_node("extraction", extraction_agent)
    workflow.add_node("eligibility", eligibility_agent)
    workflow.add_node("explainability", explainability_agent)
    
    # Define edges (Workflow routing)
    workflow.add_edge("extraction", "eligibility")
    workflow.add_edge("eligibility", "explainability")
    workflow.add_edge("explainability", END)
    
    workflow.set_entry_point("extraction")
    
    # Compile the graph
    return workflow.compile()
