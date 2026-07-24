import uuid
from typing import List, Dict, Any
from app.services.llm import llm_provider
from app.services.prompt_registry import PromptRegistry
from app.schemas.fhir_extraction import DocumentExtractionResult
from app.services.ontology import ontology_mapper
from datetime import datetime

class ExtractionAgent:
    """
    Coordinates the extraction of structured medical data from document chunks.
    Implements Pydantic validation and Ontology Mapping.
    """
    
    async def extract_from_chunk(self, chunk_text: str, chunk_metadata: Dict[str, Any], document_id: str) -> DocumentExtractionResult:
        """
        Extracts medical entities from a single text chunk.
        """
        prompt_version = "v1"
        prompt_template = PromptRegistry.get_prompt("medical_extraction", prompt_version)
        
        # 1. LLM Extraction & Pydantic Validation
        # The LLMProvider will automatically inject format instructions and parse the result
        inputs = {"chunk_text": chunk_text}
        
        try:
            # Pydantic validation happens automatically inside generate_structured
            extracted_result: DocumentExtractionResult = await llm_provider.generate_structured(
                prompt_template=prompt_template,
                pydantic_schema=DocumentExtractionResult,
                inputs=inputs
            )
        except Exception as e:
            # In a production setting, this would trigger the Retry Strategy
            print(f"Extraction failed for chunk {chunk_metadata.get('chunk_index')}: {e}")
            return DocumentExtractionResult()

        # 2. Add Provenance & Metadata
        metadata = {
            "llm_provider": llm_provider.__class__.__name__,
            "llm_model": getattr(llm_provider, "model", type("Mock", (), {"model_name": "unknown"})).model_name if hasattr(llm_provider, "model") else "unknown",
            "prompt_version": prompt_version,
            "ontology_version": "hybrid_v1",
            "embedding_model": "none",
            "extraction_timestamp": datetime.utcnow()
        }
        
        evidence = {
            "document_id": document_id,
            "page_number": chunk_metadata.get("page_number", 0),
            "chunk_id": chunk_metadata.get("chunk_index", 0),
            "character_start": None,
            "character_end": None,
            "text": chunk_text
        }

        # 3. Ontology Mapping & Field Injection
        # For each condition, map it and inject the evidence/metadata
        for condition in extracted_result.conditions:
            condition.evidence = evidence
            condition.metadata = metadata
            
            system, code = await ontology_mapper.resolve_term(condition.condition_name)
            if system == "ICD-10":
                condition.icd10_code = code
            elif system == "SNOMED":
                condition.snomed_code = code

        for obs in extracted_result.observations:
            obs.evidence = evidence
            obs.metadata = metadata
            system, code = await ontology_mapper.resolve_term(obs.observation_name)
            if system == "LOINC":
                obs.loinc_code = code

        for med in extracted_result.medications:
            med.evidence = evidence
            med.metadata = metadata
            system, code = await ontology_mapper.resolve_term(med.medication_name)
            if system == "RxNorm":
                med.rxnorm_code = code
                
        for proc in extracted_result.procedures:
            proc.evidence = evidence
            proc.metadata = metadata
            
        for alg in extracted_result.allergies:
            alg.evidence = evidence
            alg.metadata = metadata

        if extracted_result.patient:
            extracted_result.patient.evidence = evidence
            extracted_result.patient.metadata = metadata

        return extracted_result

extraction_agent = ExtractionAgent()
