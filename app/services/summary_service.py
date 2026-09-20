from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.services.fact_service import FactService
from app.services.fact_verification_service import FactVerificationService
class SummaryService:
    def __init__(self,llm_service:LLMService,prompt_service:PromptService,fact_service:FactService,fact_verification_service:FactVerificationService):

        self.llm_service=llm_service
        self.prompt_service=prompt_service
        self.fact_service=fact_service
        self.fact_verification_service=fact_verification_service
    def  create_chunk_groups(self,chunks,group_size=10):
        groups=[]
        for i in range(0,len(chunks),group_size):
            group=chunks[i:i+group_size]
            groups.append(group)
        return groups
    def create_section_summary(self,group):
        group_text="\n\n".join(group)
        prompt=self.prompt_service.build_summary_prompt(group_text)
        summary=self.llm_service.generate_answer(prompt)
        return summary 
    def summarize_paper(self, chunks):

    # Use the beginning of the paper for the high-level summary.
    # This normally contains the abstract and introduction.
        overview_chunks = chunks[:6]

        overview_text = "\n\n".join(overview_chunks)

        prompt = self.prompt_service.build_summary_prompt(overview_text)

        print("Generating grounded paper summary...")

        summary = self.llm_service.generate_answer(prompt)

        return summary

#     def summarize_paper(self,chunks):
#         chunk_groups=self.create_chunk_groups(chunks)
        
#         section_summaries=[]
#         all_facts=[]
#         for index,group in enumerate(chunk_groups, start=1):
            
#             summary=self.create_section_summary(group)
#             section_summaries.append(summary)
            
#             facts=self.fact_service.extract_facts("\n\n".join(group))
#             verified_facts=self.fact_verification_service.verify_fact(facts)
#             all_facts.append(verified_facts)
#         all_summaries="\n\n".join(section_summaries)
#         all_facts_text="\n\n".join(all_facts)
#         source_text="\n\n".join(chunks)
        
        
#         prompt = self.prompt_service.build_final_summary_prompt(
#             all_summaries,
#             source_text,
#             all_facts_text
# )
#         final_summary=self.llm_service.generate_answer(prompt)
#         return final_summary 