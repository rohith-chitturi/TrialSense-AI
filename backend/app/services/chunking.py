import re
from typing import List, Dict, Any

class SemanticChunker:
    """
    Chunks medical text semantically based on common section headers,
    then by paragraph, then by sentence.
    """
    def __init__(self):
        # Common medical headers to split sections
        self.section_pattern = re.compile(
            r'^(HISTORY|DIAGNOSIS|MEDICATIONS|LAB RESULTS|ASSESSMENT|PLAN|CHIEF COMPLAINT):', 
            re.MULTILINE | re.IGNORECASE
        )
        
    def chunk_document(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []
        
        for page in pages:
            text = page["text"]
            page_num = page["page"]
            
            # 1. Split by section
            # For this MVP, we split by double newlines as a proxy for paragraphs/sections
            # In a production setting, this would use LangChain's RecursiveCharacterTextSplitter 
            # or a custom regex splitter based on self.section_pattern.
            raw_chunks = re.split(r'\n\s*\n', text)
            
            for idx, chunk in enumerate(raw_chunks):
                clean_chunk = chunk.strip()
                if not clean_chunk:
                    continue
                    
                chunks.append({
                    "content": clean_chunk,
                    "metadata": {
                        "page_number": page_num,
                        "chunk_index": idx
                    }
                })
                
        return chunks

semantic_chunker = SemanticChunker()
