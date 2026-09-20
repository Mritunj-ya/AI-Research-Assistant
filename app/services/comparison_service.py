from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService

class COmparisonService:
    def __init__(self,
                 llm_service:LLMService,
                 prompt_service:PromptService,
                 ):
        self.llm_service=llm_service
        self.prompt_service=prompt_service
    def compare_papers(self,
                      paper1_summary,
                      paper2_summary):
        prompt=self.prompt_service.build_comparison_prompt(
            paper1_summary,
            paper2_summary
        )
        comparison=self.llm_service.generate_answer(prompt)
        return comparison