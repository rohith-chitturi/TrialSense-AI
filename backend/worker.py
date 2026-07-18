import asyncio
import logging
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from app.agents import build_workflow, PatientState

@activity.defn
async def run_langgraph_agent(patient_data: dict) -> dict:
    graph = build_workflow()
    initial_state = PatientState(
        patient_id=patient_data["id"],
        fhir_data=patient_data.get("fhir_data", {}),
        unstructured_documents=patient_data.get("docs", []),
        extracted_conditions=[],
        extracted_medications=[],
        similar_patients=[],
        retrieved_trials=[],
        confidence_scores={},
        eligibility_decisions={},
        messages=[]
    )
    # Execute LangGraph Multi-Agent Workflow
    final_state = graph.invoke(initial_state)
    return final_state

@workflow.defn
class PatientProcessingWorkflow:
    @workflow.run
    async def process_patient(self, patient_data: dict) -> dict:
        # Step 1: Run AI Agents (Extraction, Eligibility, Explainability)
        result = await workflow.execute_activity(
            run_langgraph_agent,
            patient_data,
            start_to_close_timeout=timedelta(minutes=10),
        )
        # Future Step 2: Await Human Approval (Doctor) before final DB write
        return result

async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233")
    logging.info("Connected to Temporal server")
    
    worker = Worker(
        client,
        task_queue="trialsense-task-queue",
        workflows=[PatientProcessingWorkflow],
        activities=[run_langgraph_agent],
    )
    
    logging.info("Starting Temporal Worker for AI Agents...")
    await worker.run()

if __name__ == "__main__":
    from datetime import timedelta
    asyncio.run(main())
