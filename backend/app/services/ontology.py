from typing import Dict, Optional, Tuple
from app.services.llm import llm_provider
from app.services.prompt_registry import PromptRegistry

class OntologyMapper:
    """
    Hybrid Medical Ontology Resolver
    Translates raw clinical terms to standard vocabularies (ICD-10, SNOMED, LOINC).
    Flow: Exact Dictionary Match -> LLM Normalization -> (Future API Fallback)
    """
    def __init__(self):
        # A simple mocked dictionary for MVP phase (in production this would be Redis/DB)
        self.exact_matches: Dict[str, Tuple[str, str]] = {
            "type 2 diabetes": ("ICD-10", "E11"),
            "high blood pressure": ("ICD-10", "I10"),
            "hypertension": ("ICD-10", "I10"),
            "hbp": ("ICD-10", "I10"),
            "heart attack": ("ICD-10", "I21.9"),
        }

    async def resolve_term(self, raw_term: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Returns (System, Code) e.g., ("ICD-10", "E11")
        """
        term_lower = raw_term.lower().strip()
        
        # 1. Dictionary Lookup
        if term_lower in self.exact_matches:
            return self.exact_matches[term_lower]

        # 2. LLM Fallback Normalization
        # In a real scenario we'd use generate_structured here too to get JSON back.
        # For simplicity we assume it returns a comma-separated format or JSON.
        prompt = PromptRegistry.get_prompt("ontology_mapping", "v1")
        filled_prompt = prompt.format(term=raw_term)
        
        try:
            # We bypass full structured generation for brevity, but a robust pipeline 
            # would use generate_structured with a Pydantic model here.
            llm_response = await llm_provider.generate(filled_prompt)
            
            # Very basic parsing of LLM response for demonstration
            # E.g. {"system": "ICD-10", "code": "E11.9"}
            import json
            # Strip markdown blocks if any
            clean_resp = llm_response.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_resp)
            
            if "system" in data and "code" in data:
                return data["system"], data["code"]
        except Exception as e:
            # Fallback failed
            print(f"Ontology mapping failed for {raw_term}: {e}")
            pass
            
        # 3. (Future) API Fallback to UMLS/RxNorm REST API would go here
        
        return None, None

ontology_mapper = OntologyMapper()
