from typing import Dict, Any

class PromptRegistry:
    """
    Central registry for managing and versioning prompts.
    """
    _prompts: Dict[str, Dict[str, str]] = {
        "medical_extraction": {
            "v1": """
            You are an expert clinical data abstractor. Extract the following medical entities from the provided text chunk.
            
            Chunk Content: {chunk_text}
            
            Return strictly valid JSON matching the provided schema.
            """
        },
        "ontology_mapping": {
            "v1": """
            You are a medical ontology expert. Map the following clinical term to its standard SNOMED CT or ICD-10 equivalent.
            
            Clinical Term: {term}
            
            Return strictly valid JSON.
            """
        }
    }

    @classmethod
    def get_prompt(cls, prompt_name: str, version: str = "v1") -> str:
        if prompt_name not in cls._prompts:
            raise ValueError(f"Prompt {prompt_name} not found in registry.")
        if version not in cls._prompts[prompt_name]:
            raise ValueError(f"Version {version} for prompt {prompt_name} not found.")
            
        return cls._prompts[prompt_name][version]
