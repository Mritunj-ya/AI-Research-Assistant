class ResearchAssistant:

    def __init__(
            self,
            paper_service,
            pdf_service,
            text_extractor,
            chunk_service,
            embedding_service,
            vector_store,
            prompt_service,
            llm_service,
            summary_service,
            research_gap_service,
            comparison_service
    ):
        self.paper_service = paper_service
        self.pdf_service = pdf_service
        self.text_extractor = text_extractor
        self.chunk_service = chunk_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.prompt_service = prompt_service
        self.llm_service = llm_service
        self.summary_service = summary_service
        self.research_gap_service = research_gap_service
        self.comparison_service = comparison_service

        self.current_summary = None
        self.current_paper = None
        self.current_chunks = None
        self.loaded_papers = []

    def load_paper(self, query):

        if not query or not query.strip():
            print("Research topic cannot be empty.")
            return False

        print("Searching papers...")

        try:
            papers = self.paper_service.search_papers(query)
        except Exception as e:
            print(f"Failed to search papers: {e}")
            return False

        if not papers:
            print("No papers found.")
            return False

        print("\nFound Papers")
        print("=" * 50)

        for index, paper in enumerate(papers, start=1):
            print(f"{index}. {paper['title']}")

        print("=" * 50)

        while True:
            try:
                choice = int(
                    input(f"Select a paper (1-{len(papers)}): ")
                )

                if 1 <= choice <= len(papers):
                    break

                print("Invalid choice.")

            except ValueError:
                print("Please enter a number.")

        selected_paper = papers[choice - 1]

        if not selected_paper.get("title"):
            print("Selected paper has no title.")
            return False

        if not selected_paper.get("pdf_url"):
            print("Selected paper does not have a PDF available.")
            return False

        self.current_paper = selected_paper
        self.current_summary = None

        print("\nSelected Paper:")
        print(selected_paper["title"])
        print()
        print("Downloading paper...")

        try:
            pdf_path = self.pdf_service.download_pdf(
                selected_paper["pdf_url"],
                "paper1.pdf"
            )
        except Exception as e:
            print(f"Failed to download paper: {e}")
            self.current_paper = None
            return False

        if not pdf_path:
            print("Failed to download paper.")
            self.current_paper = None
            return False

        print("Extracting text...")

        try:
            text = self.text_extractor.extract_text(pdf_path)
        except Exception as e:
            print(f"Failed to extract text from PDF: {e}")
            self.current_paper = None
            return False

        if not text or not text.strip():
            print("No readable text was found in the PDF.")
            self.current_paper = None
            return False

        print("Creating chunks...")

        try:
            chunks = self.chunk_service.chunk_text(text)
        except Exception as e:
            print(f"Failed to create chunks: {e}")
            self.current_paper = None
            return False

        if not chunks:
            print("No usable text chunks were created.")
            self.current_paper = None
            return False

        print("Generating embeddings...")

        try:
            embeddings = self.embedding_service.create_embedding(chunks)
        except Exception as e:
            print(f"Failed to generate embeddings: {e}")
            self.current_paper = None
            return False

        if embeddings is None or len(embeddings) == 0:
            print("No embeddings were generated.")
            self.current_paper = None
            return False

        print("Building vector database...")

        try:
            self.vector_store.reset()
            self.vector_store.add_embeddings(
                chunks,
                embeddings
            )
        except Exception as e:
            print(f"Failed to build vector database: {e}")
            self.current_paper = None
            return False

        self.current_chunks = chunks

        already_loaded = any(
            paper["title"] == selected_paper["title"]
            for paper in self.loaded_papers
        )

        if not already_loaded:
            self.loaded_papers.append({
                "title": selected_paper["title"],
                "summary": None,
                "chunks": chunks
            })

        print("Paper loaded successfully.")

        return True

    def load_selected_paper(self, selected_paper):

        if not selected_paper.get("title"):
            return False

        if not selected_paper.get("pdf_url"):
            return False

        self.current_paper = selected_paper
        self.current_summary = None

        print("\nSelected Paper:")
        print(selected_paper["title"])
        print()
        print("Downloading paper...")

        try:
            pdf_path = self.pdf_service.download_pdf(
                selected_paper["pdf_url"],
                "paper1.pdf"
            )
        except Exception as e:
            print(f"Failed to download paper: {e}")
            self.current_paper = None
            return False

        if not pdf_path:
            print("Failed to download paper.")
            self.current_paper = None
            return False

        print("Extracting text...")

        try:
            text = self.text_extractor.extract_text(pdf_path)
        except Exception as e:
            print(f"Failed to extract text from PDF: {e}")
            self.current_paper = None
            return False

        if not text or not text.strip():
            print("No readable text was found in the PDF.")
            self.current_paper = None
            return False

        print("Creating chunks...")

        try:
            chunks = self.chunk_service.chunk_text(text)
        except Exception as e:
            print(f"Failed to create chunks: {e}")
            self.current_paper = None
            return False

        if not chunks:
            print("No usable text chunks were created.")
            self.current_paper = None
            return False

        print("Generating embeddings...")

        try:
            embeddings = self.embedding_service.create_embedding(chunks)
        except Exception as e:
            print(f"Failed to generate embeddings: {e}")
            self.current_paper = None
            return False

        if embeddings is None or len(embeddings) == 0:
            print("No embeddings were generated.")
            self.current_paper = None
            return False

        print("Building vector database...")

        try:
            self.vector_store.reset()
            self.vector_store.add_embeddings(
                chunks,
                embeddings
            )
        except Exception as e:
            print(f"Failed to build vector database: {e}")
            self.current_paper = None
            return False

        self.current_chunks = chunks

        already_loaded = any(
            paper["title"] == selected_paper["title"]
            for paper in self.loaded_papers
        )

        if not already_loaded:
            self.loaded_papers.append({
                "title": selected_paper["title"],
                "summary": None,
                "chunks": chunks
            })

        return True

    def ask(self, question):

        if self.current_paper is None:
            return "Please load a paper first."

        if not question or not question.strip():
            return "Question cannot be empty."

        try:
            question_embedding = (
                self.embedding_service.create_embedding([question])
            )

            retrieved_chunks = self.vector_store.search(
                question_embedding
            )

            paper_abstract = self.current_paper.get(
                "abstract",
                "Not provided."
            )

            prompt = self.prompt_service.build_qa_prompt(
                question,
                self.current_paper["title"],
                paper_abstract,
                retrieved_chunks
            )

            answer = self.llm_service.generate_answer(prompt)

            return answer

        except Exception as e:
            return f"Failed to answer question: {e}"

    def summarize(self):

        if self.current_paper is None:
            return "Please load a paper first."

        if not self.current_chunks:
            return "No paper content found."

        try:
            summary = self.summary_service.summarize_paper(
                self.current_chunks
            )

            self.current_summary = summary

            for paper in self.loaded_papers:
                if paper["title"] == self.current_paper["title"]:
                    paper["summary"] = summary
                    break

            return summary

        except Exception as e:
            return f"Failed to summarize paper: {e}"

    def compare_papers(self):

        if len(self.loaded_papers) < 2:
            return "Please load and summarize at least two papers."

        print("\nLoaded Papers")
        print("=" * 50)

        for index, paper in enumerate(
            self.loaded_papers,
            start=1
        ):
            print(f"{index}. {paper['title']}")

        print("=" * 50)

        while True:
            try:
                paper1 = int(
                    input("Select Paper 1: ")
                ) - 1

                if 0 <= paper1 < len(self.loaded_papers):
                    break

                print("Invalid paper number.")

            except ValueError:
                print("Please enter a valid number.")

        while True:
            try:
                paper2 = int(
                    input("Select Paper 2: ")
                ) - 1

                if 0 <= paper2 < len(self.loaded_papers):
                    break

                print("Invalid paper number.")

            except ValueError:
                print("Please enter a valid number.")

        if paper1 == paper2:
            return "Please select two different papers."

        summary1 = self.loaded_papers[paper1]["summary"]
        summary2 = self.loaded_papers[paper2]["summary"]

        if summary1 is None or summary2 is None:
            return "Please summarize both papers before comparing them."

        try:
            comparison = self.comparison_service.compare_papers(
                summary1,
                summary2
            )

            return comparison

        except Exception as e:
            return f"Failed to compare papers: {e}"

    def find_research_gap(self):

        if self.current_paper is None:
            return "Please load a paper first."

        if self.current_summary is None:
            return "Please summarize the paper first."

        try:
            return self.research_gap_service.find_research_gap(
                self.current_summary
            )

        except Exception as e:
            return f"Failed to find research gap: {e}"

    def generate_literature_review(self):
        pass