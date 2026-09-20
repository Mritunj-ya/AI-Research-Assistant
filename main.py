from app.services.paper_service import PaperService
from app.services.pdf_service import PDFService
from app.services.text_extractor import TextExtractor
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.services.assistant.research_assistant import ResearchAssistant
from app.services.summary_service import SummaryService
from app.services.research_gap_service import ResearchGapService
from app.services.fact_service import FactService
from app.services.fact_verification_service import FactVerificationService
from app.services.comparison_service import COmparisonService
def main():
    
    paper_service=PaperService()
    pdf_service = PDFService()
    text_extractor = TextExtractor()
    chunk_service = ChunkService()
    embedding_service = EmbeddingService()
    vector_store = VectorStore()
    prompt_service = PromptService()
    llm_service = LLMService()
    fact_service=FactService(llm_service,prompt_service)
    fact_verification_service=FactVerificationService(
        llm_service,
        prompt_service,
        embedding_service,
        vector_store 
    )
    summary_service = SummaryService(
        llm_service,
        prompt_service,
        fact_service,
        fact_verification_service
    )
    research_gap_service=ResearchGapService(llm_service,prompt_service, embedding_service, vector_store)
    comparison_service=COmparisonService(llm_service,prompt_service)
    assistant=ResearchAssistant(paper_service,pdf_service,text_extractor,
                                chunk_service,embedding_service,vector_store,prompt_service,
                                llm_service,summary_service, research_gap_service,comparison_service)
    
    while True:
        query = input("Enter research topic: ").strip()

        if not query:
            print("Research topic cannot be empty.")
            continue

        break
    assistant.load_paper(query)
    while True:
        print("\n")
        print("="*50)
        print("AI Research Assistant")
        print("="*50)
        print("="*50)
        print("1.Ask Question")
        print("2.Summarize Paper")
        print("3.Find Research gap")
        print("4.Compare Papers")
        print("5.Load Another Paper")
        print("6.Exit")
        choice=input("Enter your choice:")
        if choice =="1":
            question=input("Ask Question:")
            answer=assistant.ask(question)
            print(answer)
        elif choice=="2":
            print("\nGenerating paper summary...\n")

            summary = assistant.summarize()

            print("=" * 50)
            print("PAPER SUMMARY")
            print("=" * 50)
            print(summary)
        elif choice=="3":
            print("\nAnalyzing research gaps...\n")
            research_gap=assistant.find_research_gap()
            print("\n")
            print("=" * 50)
            print("Research Gap Analysis")
            print("=" * 50)
            print(research_gap)

        elif choice=="4":
            print("\nComparing selected papers...\n")
            comparison=assistant.compare_papers()
            print("\n")
            print("=" * 50)
            print("PAPER COMPARISON")
            print("=" * 50)
            print(comparison)

        elif choice == "5":
            while True:
                query = input("Enter research topic: ").strip()

                if not query:
                    print("Research topic cannot be empty.")
                    continue

                assistant.load_paper(query)
                break
        elif choice=="6":
            print("Thank you for using AI Research Assitant.")
            break
        else:
            print("Invalid Choice!!!")


        
    

#     paper_service=PaperService()
#     pdf_service=PDFService()
#     papers=paper_service.search_papers("Large Language Models")
#     for index,paper in enumerate(papers,start=1):
#         print("="*60)
#         print(f"Paper{index}")
#         print(f"Title     :{paper['title']}")
#         print(f"Published :{paper['published']}")
#         print(f"Summary   :{paper['summary'][:200]}..")
#         print()
#     first_paper=papers[0]
#     pdf_path=pdf_service.download_pdf(
#         first_paper["pdf_url"],
#         "paper1.pdf"
#     )
#     print("\nDownloaded Successfully!")
#     print(pdf_path)

#     extractor=TextExtractor()
#     extractor.extract_text("data/papers/paper1.pdf")
#     text=extractor.extract_text(pdf_path)
#     print("="*60)
#     print("Extracted Text")
#     print("="*60)
#     print(text[:1000])
#     chunk_service=ChunkService()
#     chunk=chunk_service.chunk_text(text)
    
#     print("="*60)
#     print("First chunks")
#     print(len(chunk))
#     print("="*60)
#     print(chunk[0])

#     print("\n")

#     print("=" * 60)
#     print("Chunk 2")
#     print("=" * 60)
#     print(chunk[1])

#     embedding_service=EmbeddingService()
#     embedding=embedding_service.create_embedding(chunk)
#     print("="*60)
#     print("Embedding Information")
#     print("="*60)
#     print(f"Total Chunks :{len(chunk)}")
#     print(f"Total Embedding :{len(embedding)}")
#     print(f"Embedding Size:{len(embedding[0])}")

#     print("=" * 60)
#     print("First Embedding")
#     print("=" * 60)
#     print(embedding.shape)
#     print(embedding[0].shape)
#     vector_store=VectorStore()
#     vector_store.add_embeddings(embedding)
#     print("=" * 60)
#     print("FAISS Information")
#     print("=" * 60)
#     print(f"Total Vectors in Index: {vector_store.index.ntotal}")
#     query=input("Ask a question")
#     query_embedding=embedding_service.create_embedding([query])
#     distances,indices=vector_store.search(query_embedding)
#     print("="*60)
#     print("Retrieved Chunks")
#     print("="*60)
#     for index in indices[0]:
#         print(chunk[index])
#         print("="*60)
    
#     question=input("Ask your qustion  about the paper:")
#     retrieved_chunks=vector_store.search(question)
#     prompt_service=PromptService()
#     prompt=prompt_service.build_prompt(
#         question,
#         retrieved_chunks
#     )
#     llm_service=LLMService()
#     answer=llm_service.generate_answer(prompt)
#     print("=" * 60)
#     print("Research Assistant")
#     print("=" * 60)
#     print(answer)


if __name__ == "__main__":
    main()