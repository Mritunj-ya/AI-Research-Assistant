from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
class FactService:
    def __init__(self,llm_service:LLMService, prompt_service:PromptService):
        self.llm_service=llm_service
        self.prompt_service=prompt_service
    def extract_facts(self,text):
        prompt=self.prompt_service.build_fact_extraction_prompt(text)
        facts=self.llm_service.generate_answer(prompt)
        return facts
    
