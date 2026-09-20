AI Research Assistant --- Project Documentation
1. Project Overview
The AI Research Assistant is an end-to-end AI application designed to
help users discover, process, analyze, summarize, question, and compare
research papers.
The system combines document processing, semantic embeddings, FAISS
vector retrieval, Retrieval-Augmented Generation (RAG), structured
prompting, and open-source LLM inference.
The application supports both:
Local inference: Ollama + Qwen3 8B
Cloud inference: Hugging Face Inference Providers + Qwen3 8B
The web interface is built with Streamlit and the production application
is deployed on Streamlit Community Cloud.
---
2. Problem Statement
Reading and analyzing research papers manually can require significant
time. Important information such as the research problem, methodology,
contributions, experimental setup, findings, limitations, and potential
research gaps is distributed throughout long documents.
The goal of this project is to provide an AI-assisted workflow that can
retrieve relevant paper content and use it to support research analysis
while reducing unsupported or fabricated responses.
---
3. Project Objectives
The main objectives are:
Search for relevant research papers.
Download and process selected papers.
Extract text from PDF documents.
Split documents into overlapping chunks.
Generate semantic embeddings.
Store embeddings in a FAISS vector index.
Retrieve relevant paper content for user questions.
Generate grounded answers using an LLM.
Produce structured paper summaries.
Identify potential research gaps conservatively.
Compare multiple research papers.
Deploy the complete application to the cloud.
---
4. Main Features
4.1 Research Paper Search
Users can search for research papers by topic and select a paper for
analysis.
4.2 PDF Processing
The selected paper is downloaded and processed using PyMuPDF.
Workflow:
``` text
Paper PDF
   ↓
Text Extraction
   ↓
Text Chunks
   ↓
Semantic Embeddings
   ↓
FAISS Vector Index
```
4.3 RAG-Based Question Answering
For a user question:
``` text
User Question
     ↓
Question Embedding
     ↓
FAISS Similarity Search
     ↓
Relevant Paper Chunks
     ↓
Grounded Prompt
     ↓
Qwen3 8B
     ↓
Answer
```
The prompting layer instructs the model to remain grounded in the
available paper content and to indicate when the requested information
is not supported.
4.4 Structured Paper Summarization
The summary is organized into:
Research Problem
Proposed Method
Key Contributions
Experimental Setup
Key Findings
Limitations
Future Work
Overall Summary
4.5 Research Gap Analysis
The system analyzes available paper information to identify potential
research gaps.
When the available evidence is insufficient, the system can return:
``` text
NO_CLEAR_GAP_FOUND
```
This conservative behavior is intended to reduce unsupported gap
generation.
4.6 Paper Comparison
Multiple loaded papers can be compared across:
Research Objective
Proposed Method
Main Contributions
Experimental Setup
Key Findings / Results
Limitations
Future Work
Similarities
Differences
Overall Comparison
The comparison prompt explicitly separates information belonging to each
paper.
---
5. System Architecture
``` text
                         USER
                           │
                           ▼
                 ┌───────────────────┐
                 │ Streamlit Web UI  │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ ResearchAssistant │
                 └─────────┬─────────┘
                           │
       ┌───────────────────┼────────────────────┐
       │                   │                    │
       ▼                   ▼                    ▼
 PaperService         PDFService        TextExtractor
       │                   │                    │
       ▼                   ▼                    ▼
 Paper Search          PDF Download         PDF → Text
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ ChunkService    │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ EmbeddingService│
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │   VectorStore   │
                                      │      FAISS      │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      Relevant Chunks
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │  PromptService  │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │   LLMService    │
                                      └────────┬────────┘
                                               │
                              ┌────────────────┴────────────────┐
                              │                                 │
                              ▼                                 ▼
                       Ollama + Qwen3                    Hugging Face
                          Local Path                     Cloud Path
                              │                                 │
                              └────────────────┬────────────────┘
                                               ▼
                                            Response
```
---
6. Services
PaperService
Responsible for searching research papers and returning paper metadata
such as:
Title
Abstract / summary
Publication date
PDF URL
PDFService
Downloads selected research-paper PDFs and stores them locally during
processing.
TextExtractor
Uses PyMuPDF to extract text page by page from PDF documents.
ChunkService
Splits extracted text into manageable overlapping chunks.
The overlap helps preserve context between neighboring chunks.
EmbeddingService
Uses:
``` text
sentence-transformers
all-MiniLM-L6-v2
```
to convert text chunks into 384-dimensional semantic vectors.
VectorStore
Uses FAISS `IndexFlatL2` to store and retrieve embeddings using
similarity search.
PromptService
Builds structured prompts for:
Question answering
Summarization
Research-gap analysis
Fact extraction
Fact verification
Paper comparison
The prompts contain grounding instructions intended to reduce
unsupported generation.
LLMService
Provides the LLM abstraction.
Local path:
``` text
Ollama → Qwen3 8B
```
Cloud path:
``` text
Hugging Face Inference → Qwen3 8B
```
The cloud path is selected when `HF_TOKEN` is available.
SummaryService
Coordinates summary generation and the associated fact/verification
workflow.
ResearchGapService
Coordinates research-gap generation and verification.
ComparisonService
Generates structured comparisons between loaded papers.
ResearchAssistant
Acts as the main orchestration layer and connects the individual
services into the application workflow.
---
7. Technology Stack
Category          Technology
---
Language          Python
UI                Streamlit
PDF Processing    PyMuPDF
Embeddings        Sentence Transformers
Embedding Model   all-MiniLM-L6-v2
Vector Database   FAISS
Local LLM         Qwen3 8B through Ollama
Cloud LLM         Qwen3 8B through Hugging Face Inference
Research Source   arXiv API
Version Control   Git
Repository        GitHub
Deployment        Streamlit Community Cloud
---
8. Local vs Cloud Architecture
Local Development
``` text
Streamlit
    │
    ├── Sentence Transformers
    │
    ├── FAISS
    │
    └── Ollama
           │
           ▼
       Qwen3 8B
```
The local version is useful for development and testing without
depending on a cloud LLM.
Cloud Deployment
``` text
Streamlit Community Cloud
          │
          ├── Sentence Transformers
          │
          ├── FAISS
          │
          └── Hugging Face Inference
                    │
                    ▼
                 Qwen3 8B
```
The deployed application cannot access the Ollama instance running on
the development laptop, so the LLM service supports a cloud inference
path.
The Hugging Face token is stored as a deployment secret and is not
included in the repository.
---
9. Deployment
The project was deployed to Streamlit Community Cloud from the GitHub
repository.
Repository:
``` text
Mritunj-ya/AI-Research-Assistant
```
Deployment branch:
``` text
main
```
Main application file:
``` text
app.py
```
The deployment was tested successfully with:
Paper search
Paper loading
PDF processing
Semantic embeddings
FAISS retrieval
Question answering
Unsupported-question handling
Paper summarization
Research-gap analysis
Paper comparison
Cloud LLM inference
The deployed cloud version also showed substantially faster response
generation than the local CPU-based Qwen3 8B workflow during testing.
---
10. Validation and Testing
Supported Question Test
Example:
``` text
What is the main contribution of this paper?
```
The deployed application returned an answer based on the selected paper.
Unsupported Question Test
Example:
``` text
What dataset should the authors use in future work?
```
The deployed system responded conservatively and stated that the paper
did not explicitly specify a future dataset rather than inventing one.
Paper Comparison Test
The system was tested using:
Vicinity Vision Transformer
WiCV 2019: The Sixth Women In Computer Vision Workshop
The comparison kept the technical content of the Vicinity Vision
Transformer separate from the workshop/report content of WiCV 2019.
Where information was unavailable, the system used statements such as:
``` text
Not clearly stated in the provided summary.
```
---
11. Challenges Faced & How We Resolved Them
11.1 arXiv API Rate Limiting
The arXiv API returned HTTP 429 responses during development.
Resolution: Added explicit HTTP status handling and clear rate-limit
error reporting.
11.2 PDF Downloading
Research papers had to be downloaded from their PDF URLs before
processing.
Resolution: Created a dedicated PDF service for downloading and
storing selected papers.
11.3 PDF Text Extraction
PDF documents needed to be converted into usable text.
Resolution: Used PyMuPDF and processed documents page by page.
11.4 Chunking
Large documents could not efficiently be processed as a single context.
Resolution: Implemented configurable chunk size and overlap.
11.5 FAISS Retrieval
The application needed semantic retrieval over paper chunks.
Resolution: Generated embeddings using Sentence Transformers and
indexed them with FAISS.
11.6 Local LLM Setup
Running Qwen3 8B locally introduced model-management and CPU-performance
challenges.
Resolution: Used Ollama for local inference and moved the model
storage to the E: drive to reduce pressure on the system drive.
11.7 Storage Constraints
Large AI models and Python dependencies consumed significant disk space.
Resolution: Moved model and temporary storage to the E: drive.
11.8 Summary Hallucinations
Early summaries sometimes included information that was not clearly
supported by the source paper.
Resolution: Strengthened prompts with explicit grounding rules and
added fact extraction/verification components.
11.9 Research Gap False Positives
The model sometimes generated research gaps without enough supporting
evidence.
Resolution: Added conservative gap-generation and verification
prompts, including `NO_CLEAR_GAP_FOUND`.
11.10 Comparison Contamination
Earlier comparison outputs could mix information from different papers.
Resolution: Strengthened the comparison prompt and separated the
summaries supplied for each paper.
11.11 Streamlit Session State
Removing generated results from Streamlit session state caused
missing-key errors.
Resolution: Changed state access to safely handle keys that may not
exist.
11.12 Local vs Cloud LLM
The cloud application cannot access the local Ollama server.
Resolution: Implemented dual LLM routing:
``` text
HF_TOKEN available
       ↓
Hugging Face inference

HF_TOKEN unavailable
       ↓
Local Ollama inference
```
11.13 Deployment Dependency Issues
The application encountered missing ML dependencies after environment
restart.
Resolution: Installed and verified compatible CPU versions of
PyTorch and Torchvision and verified Sentence Transformers and
Transformers imports.
---
12. Current MVP Weaknesses
The deployed MVP is functional, but several areas can be improved.
Retrieval
FAISS currently performs basic similarity search.
There is no dedicated reranking stage.
Retrieval scores are not currently exposed to the user.
Evidence and Citations
Answers do not yet display the exact source chunks supporting each
claim.
Summary sections do not yet expose direct evidence links to paper
passages.
Research Gap Detection
The system can be conservative when the available evidence does not
clearly support a research gap.
Paper Comparison
Comparison currently relies heavily on generated summaries.
Similarity detection can be limited when summaries do not explicitly
describe shared characteristics.
Structured per-paper evidence would make comparisons more robust.
Scalability
The current architecture is designed primarily for the MVP workflow.
Larger collections of papers would benefit from persistent vector
storage and more scalable document management.
Local Inference
Qwen3 8B inference on CPU is slower than the cloud inference path.
These limitations are known and intentionally remain as future
improvement areas rather than blocking the initial deployment.
---
13. Future Improvements
Potential future versions can add:
Source-chunk citations in answers.
Retrieval-score visibility.
Reranking for retrieved chunks.
Structured evidence extraction.
Stronger multi-paper comparison.
Improved research-gap detection.
Literature-review generation.
Persistent paper collections.
Better metadata management.
User-specific research sessions.
Improved production logging and monitoring.
More scalable document and vector storage.
---
14. Project Outcome
The project progressed from a local research-paper processing prototype
to a deployed AI research workflow.
The final MVP supports:
``` text
Research Topic
      ↓
Paper Search
      ↓
Paper Selection
      ↓
PDF Processing
      ↓
Text Chunking
      ↓
Semantic Embeddings
      ↓
FAISS Retrieval
      ↓
Grounded LLM Analysis
      ↓
 ┌───────────────┬────────────────┬─────────────────┐
 │               │                │                 │
 ▼               ▼                ▼                 ▼
Q&A          Summary       Research Gap       Comparison
```
The application is publicly deployed and the source code is maintained
in GitHub.
---
15. Repository
``` text
https://github.com/Mritunj-ya/AI-Research-Assistant
```
16. Deployment
The application is deployed through Streamlit Community Cloud.
The deployed application URL is available from the project's Streamlit
deployment configuration.
---
17. Resume-Level Project Description
AI Research Assistant | Python, RAG, FAISS, Sentence Transformers,
Qwen3, Streamlit
Built and deployed an end-to-end AI research assistant that searches and
processes research papers, performs semantic retrieval using Sentence
Transformers and FAISS, and uses Qwen3 8B to provide grounded Q&A,
structured summaries, research-gap analysis, and multi-paper comparison.
Implemented modular services for PDF processing, chunking, embeddings,
retrieval, prompting, verification, and LLM inference with local Ollama
and cloud Hugging Face deployment paths.