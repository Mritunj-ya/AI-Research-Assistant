import streamlit as st

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


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .paper-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 1rem;
    }

    .status-card {
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE SERVICES
# ============================================================

@st.cache_resource
def create_assistant():

    paper_service = PaperService()
    pdf_service = PDFService()
    text_extractor = TextExtractor()
    chunk_service = ChunkService()
    embedding_service = EmbeddingService()
    vector_store = VectorStore()
    prompt_service = PromptService()
    llm_service = LLMService()

    fact_service = FactService(
        llm_service,
        prompt_service
    )

    fact_verification_service = FactVerificationService(
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

    research_gap_service = ResearchGapService(
        llm_service,
        prompt_service,
        embedding_service,
        vector_store
    )

    comparison_service = COmparisonService(
        llm_service,
        prompt_service
    )

    assistant = ResearchAssistant(
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
    )

    return assistant


assistant = create_assistant()


# ============================================================
# SESSION STATE
# ============================================================

if "papers" not in st.session_state:
    st.session_state["papers"] = []

if "paper_loaded" not in st.session_state:
    st.session_state["paper_loaded"] = False

if "summary" not in st.session_state:
    st.session_state["summary"] = None

if "research_gap" not in st.session_state:
    st.session_state["research_gap"] = None

if "comparison" not in st.session_state:
    st.session_state["comparison"] = None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔬 AI Research Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Search, analyze, summarize, and compare research papers '
    'using an AI-powered RAG pipeline.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SEARCH SECTION
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Search Research Papers</div>',
    unsafe_allow_html=True
)

search_col1, search_col2 = st.columns([4, 1])

with search_col1:

    research_topic = st.text_input(
        "Research topic",
        placeholder="e.g. Vision Transformer, Large Language Models",
        label_visibility="collapsed"
    )

with search_col2:

    search_button = st.button(
        "🔎 Search Papers",
        use_container_width=True
    )


if search_button:

    if not research_topic.strip():

        st.warning("Please enter a research topic.")

    else:

        with st.spinner("Searching research papers..."):

            try:

                papers = assistant.paper_service.search_papers(
                    research_topic.strip()
                )

                st.session_state["papers"] = papers

                # Clear previous analysis
                st.session_state["paper_loaded"] = False
                st.session_state["summary"] = None
                st.session_state["research_gap"] = None
                st.session_state["comparison"] = None

            except Exception as e:

                st.error(
                    f"Failed to search papers: {e}"
                )


# ============================================================
# PAPER SELECTION
# ============================================================

if st.session_state["papers"]:

    st.markdown(
        '<div class="section-title">📚 Search Results</div>',
        unsafe_allow_html=True
    )

    papers = st.session_state["papers"]

    paper_titles = [
        paper["title"]
        for paper in papers
    ]

    selected_index = st.selectbox(
        "Select a paper",
        range(len(paper_titles)),
        format_func=lambda x: paper_titles[x],
        key="selected_paper"
    )

    selected_paper = papers[selected_index]

    st.markdown(
        '<div class="paper-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"### {selected_paper['title']}"
    )

    if selected_paper.get("summary"):

        st.write(
            selected_paper["summary"]
        )

    elif selected_paper.get("abstract"):

        st.write(
            selected_paper["abstract"]
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    load_button = st.button(
        "📥 Load Selected Paper",
        use_container_width=True
    )

    if load_button:

        with st.spinner(
            "Loading and processing paper..."
        ):

            try:

                success = assistant.load_selected_paper(
                    selected_paper
                )

                if success:

                    st.session_state["paper_loaded"] = True

                    # Clear analysis results from the previously loaded paper
                    st.session_state.pop("summary", None)
                    st.session_state.pop("research_gap", None)
                    st.session_state.pop("comparison", None)

                    st.success(
                        "Paper loaded successfully."
                    )

                else:

                    st.session_state["paper_loaded"] = False

                    st.error(
                        "Failed to load the selected paper."
                    )

            except Exception as e:

                st.session_state["paper_loaded"] = False

                st.error(
                    f"Failed to load paper: {e}"
                )
# ============================================================
# CURRENT PAPER STATUS
# ============================================================

if st.session_state["paper_loaded"]:

    st.markdown(
        '<div class="section-title">📄 Current Paper</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"Loaded: {assistant.current_paper['title']}"
    )


# ============================================================
# PAPER OPERATIONS
# ============================================================

if st.session_state["paper_loaded"]:

    st.markdown(
        '<div class="section-title">🧠 Research Tools</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    with col1:

        if st.button(
            "📝 Summarize Paper",
            use_container_width=True
        ):

            with st.spinner(
                "Generating paper summary..."
            ):

                try:

                    summary = assistant.summarize()

                    st.session_state["summary"] = summary

                except Exception as e:

                    st.error(
                        f"Failed to generate summary: {e}"
                    )

    # --------------------------------------------------------
    # RESEARCH GAP
    # --------------------------------------------------------

    with col2:

        if st.button(
            "🔎 Find Research Gap",
            use_container_width=True
        ):

            if st.session_state["summary"] is None:

                st.warning(
                    "Please summarize the paper first."
                )

            else:

                with st.spinner(
                    "Analyzing research gaps..."
                ):

                    try:

                        gap = assistant.find_research_gap()

                        st.session_state[
                            "research_gap"
                        ] = gap

                    except Exception as e:

                        st.error(
                            f"Failed to find research gap: {e}"
                        )

    # --------------------------------------------------------
    # RESET ANALYSIS
    # --------------------------------------------------------

    with col3:

        if st.button(
            "🔄 Reset Analysis",
            use_container_width=True
        ):

            st.session_state["summary"] = None
            st.session_state["research_gap"] = None
            st.session_state["comparison"] = None

            st.success(
                "Analysis results cleared."
            )


# ============================================================
# QUESTION & ANSWER
# ============================================================

if st.session_state["paper_loaded"]:

    st.markdown(
        '<div class="section-title">💬 Ask Questions About the Paper</div>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "Your question",
        placeholder="Ask something about the loaded research paper...",
        height=100,
        label_visibility="collapsed"
    )

    if st.button(
        "💬 Ask Question",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching the paper and generating an answer..."
            ):

                try:

                    answer = assistant.ask(
                        question.strip()
                    )

                    st.markdown("### Answer")

                    st.write(answer)

                except Exception as e:

                    st.error(
                        f"Failed to answer question: {e}"
                    )


# ============================================================
# SUMMARY RESULT
# ============================================================

if st.session_state.get("summary"):

    st.markdown(
        '<div class="section-title">📝 Paper Summary</div>',
        unsafe_allow_html=True
    )

    st.write(
        st.session_state["summary"]
    )


# ============================================================
# RESEARCH GAP RESULT
# ============================================================

if st.session_state.get("research_gap"):

    st.markdown(
        '<div class="section-title">🔎 Research Gap</div>',
        unsafe_allow_html=True
    )

    st.write(
        st.session_state["research_gap"]
    )


# ============================================================
# PAPER COMPARISON
# ============================================================

if len(assistant.loaded_papers) >= 2:

    st.markdown(
        '<div class="section-title">📊 Compare Papers</div>',
        unsafe_allow_html=True
    )

    paper_titles = [
        paper["title"]
        for paper in assistant.loaded_papers
    ]

    col1, col2 = st.columns(2)

    with col1:

        paper1_title = st.selectbox(
            "Select Paper 1",
            paper_titles,
            key="comparison_paper1"
        )

    with col2:

        paper2_title = st.selectbox(
            "Select Paper 2",
            paper_titles,
            index=1 if len(paper_titles) > 1 else 0,
            key="comparison_paper2"
        )

    if st.button(
        "📊 Compare Papers",
        use_container_width=True
    ):

        if paper1_title == paper2_title:

            st.warning(
                "Please select two different papers."
            )

        else:

            paper1 = next(
                paper
                for paper in assistant.loaded_papers
                if paper["title"] == paper1_title
            )

            paper2 = next(
                paper
                for paper in assistant.loaded_papers
                if paper["title"] == paper2_title
            )

            if (
                paper1["summary"] is None
                or paper2["summary"] is None
            ):

                st.warning(
                    "Please summarize both papers before comparing them."
                )

            else:

                with st.spinner(
                    "Comparing research papers..."
                ):

                    try:

                        comparison = (
                            assistant.comparison_service.compare_papers(
                                paper1["summary"],
                                paper2["summary"]
                            )
                        )

                        st.session_state[
                            "comparison"
                        ] = comparison

                    except Exception as e:

                        st.error(
                            f"Failed to compare papers: {e}"
                        )


# ============================================================
# COMPARISON RESULT
# ============================================================

if st.session_state.get("comparison"):

    st.markdown(
        '<div class="section-title">📊 Comparison Result</div>',
        unsafe_allow_html=True
    )

    st.write(
        st.session_state["comparison"]
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Research Assistant • RAG-based research paper analysis"
)