# 🔬 AI Research Assistant

An end-to-end AI-powered research assistant that helps users search research papers, analyze papers, ask questions, generate grounded summaries, identify potential research gaps, and compare multiple papers.

The project uses Retrieval-Augmented Generation (RAG), semantic embeddings, FAISS vector search, and open-source LLMs.

## 🚀 Features

- 🔎 Search research papers
- 📄 Download and process research papers
- 🧩 Extract and chunk PDF text
- 🧠 Generate semantic embeddings
- 📚 Store and retrieve paper chunks using FAISS
- 💬 Ask questions about a loaded paper using RAG
- 📝 Generate structured paper summaries
- 🔎 Identify potential research gaps
- 📊 Compare multiple research papers
- 🛡️ Ground responses in the available paper content
- ☁️ Deployed using Streamlit Community Cloud
- 🤗 Supports Hugging Face inference for cloud deployment
- 💻 Supports local inference using Ollama

## 🏗️ Architecture

```text
User
 │
 ▼
Streamlit Web Interface
 │
 ▼
ResearchAssistant
 │
 ├── PaperService
 │      └── Research Paper Search
 │
 ├── PDFService
 │      └── PDF Download
 │
 ├── TextExtractor
 │      └── PDF → Text
 │
 ├── ChunkService
 │      └── Text → Chunks
 │
 ├── EmbeddingService
 │      └── Chunks → Embeddings
 │
 ├── VectorStore
 │      └── FAISS Similarity Search
 │
 ├── PromptService
 │      └── Grounded Prompt Construction
 │
 ├── LLMService
 │      ├── Local: Ollama + Qwen3:8B
 │      └── Cloud: Hugging Face Inference
 │
 ├── SummaryService
 │
 ├── ResearchGapService
 │
 └── ComparisonService
