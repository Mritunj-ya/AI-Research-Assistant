from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
class FactVerificationService:
    def __init__(
            self,
            llm_service:LLMService,
            prompt_service:PromptService,
            embedding_service,
            vector_store
    ):
        self.llm_service=llm_service
        self.prompt_service=prompt_service
        self.embedding_service=embedding_service
        self.vector_store=vector_store
    def retrieve_evidence(self,fact):
        fact_embedding=self.embedding_service.create_embedding([fact])
        evidence=self.vector_store.search(fact_embedding)
        return evidence
    def verify_fact(self,fact):
        evidence=self.retrieve_evidence(fact)
        prompt=self.prompt_service.build_fact_verification_prompt(
            fact,
            evidence
        )
        verification=self.llm_service.generate_answer(prompt)
        return verification 