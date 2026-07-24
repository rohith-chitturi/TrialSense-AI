from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
import os

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def generate_structured(self, prompt_template: str, pydantic_schema: type[BaseModel], inputs: Dict[str, Any]) -> BaseModel:
        pass

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        pass

    @abstractmethod
    def estimate_cost(self) -> float:
        pass


class GeminiProvider(LLMProvider):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            # Fallback for dev environment without crashing immediately
            self.api_key = "MOCK_KEY"
            
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=self.api_key,
            temperature=0.0
        )

    async def generate(self, prompt: str) -> str:
        response = await self.model.ainvoke(prompt)
        return response.content

    async def generate_structured(self, prompt_template: str, pydantic_schema: type[BaseModel], inputs: Dict[str, Any]) -> BaseModel:
        parser = PydanticOutputParser(pydantic_object=pydantic_schema)
        
        # Inject format instructions automatically
        template = prompt_template + "\n\n{format_instructions}"
        prompt = PromptTemplate(
            template=template,
            input_variables=list(inputs.keys()),
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        _input = prompt.format(**inputs)
        response = await self.model.ainvoke(_input)
        
        # Parse into Pydantic model
        return parser.parse(response.content)

    async def embed(self, text: str) -> List[float]:
        # Implementation via GoogleGenerativeAIEmbeddings would go here
        return [0.0] * 768

    async def health_check(self) -> bool:
        try:
            await self.generate("ping")
            return True
        except Exception:
            return False

    def estimate_cost(self) -> float:
        # Placeholder for token tracking logic
        return 0.0

# Singleton provider instance
llm_provider: LLMProvider = GeminiProvider()
