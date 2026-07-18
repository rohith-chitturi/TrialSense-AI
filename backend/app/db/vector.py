from langchain_community.vectorstores.pgvector import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

# Connect to the PostgreSQL database with pgvector
CONNECTION_STRING = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg2://trialsense_user:trialsense_password@localhost:5432/trialsense"
)

# Multi-Level RAG collections
COLLECTION_TRIALS = "clinical_trials"
COLLECTION_GUIDELINES = "medical_guidelines"
COLLECTION_PAPERS = "research_papers"
COLLECTION_DRUGS = "drug_information"
COLLECTION_CASES = "patient_cases"

def get_embeddings_model():
    # Utilizing Gemini Embeddings
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def get_vector_store(collection_name: str) -> PGVector:
    """Retrieve the pgvector store for a specific multi-level RAG collection."""
    embeddings = get_embeddings_model()
    return PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name=collection_name,
        use_jsonb=True
    )
