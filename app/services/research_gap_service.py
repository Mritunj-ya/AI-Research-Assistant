from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService


class ResearchGapService:

    def __init__(
        self,
        llm_service,
        prompt_service,
        embedding_service,
        vector_store
    ):
        self.llm_service = llm_service
        self.prompt_service = prompt_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def find_research_gap(self, summary):

        candidate_gaps = self.generate_candidate_gaps(summary)

        gaps = self.parse_candidate_gaps(candidate_gaps)

        if not gaps:
            return "NO_CLEAR_GAP_FOUND"

        verified_gaps = []

        for item in gaps:

            gap = item["gap"]

            evidence = self.retrieve_evidence(gap)

            verification = self.verify_gap(
                gap,
                evidence
            )

            verified_gaps.append(verification)

        if not verified_gaps:
            return "NO_RELIABLE_RESEARCH_GAP_FOUND"

        return "\n\n".join(verified_gaps)

    def retrieve_evidence(self, gap):

        gap_embedding = self.embedding_service.create_embedding(
            [gap]
        )

        evidence = self.vector_store.search(
            gap_embedding
        )

        return evidence

    def verify_gap(self, gap, evidence):

        prompt = self.prompt_service.build_gap_verification_prompt(
            gap,
            evidence
        )

        verification = self.llm_service.generate_answer(prompt).strip()

        verification_upper = verification.upper()

        # Look ONLY for the explicit VERDICT line
        status = "NOT SUPPORTED"

        for line in verification_upper.splitlines():

            line = line.strip()

            if line.startswith("VERDICT:"):

                verdict = line.replace("VERDICT:", "").strip()

                if verdict == "SUPPORTED":
                    status = "SUPPORTED"

                elif verdict == "PARTIALLY SUPPORTED":
                    status = "PARTIALLY SUPPORTED"

                elif verdict == "NOT SUPPORTED":
                    status = "NOT SUPPORTED"

                break

        # Remove the VERDICT line from the displayed explanation
        reason_lines = []

        for line in verification.splitlines():

            if not line.strip().upper().startswith("VERDICT:"):
                reason_lines.append(line)

        reason = "\n".join(reason_lines).strip()

        return f"""
    Verification:
    {status}

    Reason:
    {reason}
    """
    def generate_candidate_gaps(self, summary):

        prompt = self.prompt_service.build_candidate_gaps_prompt(
            summary
        )

        candidate_gaps = self.llm_service.generate_answer(
            prompt
        )

        return candidate_gaps

    def parse_candidate_gaps(self, candidate_gaps):

        if "NO_CLEAR_GAP_FOUND" in candidate_gaps:
            return []

        gaps = []

        blocks = candidate_gaps.split("GAP:")

        for block in blocks[1:]:

            block = block.strip()

            if not block:
                continue

            parts = block.split("EVIDENCE:", 1)

            if len(parts) < 2:
                continue

            gap = parts[0].strip()

            evidence_parts = parts[1].split(
                "RESEARCH_QUESTION:",
                1
            )

            if len(evidence_parts) < 2:
                continue

            evidence = evidence_parts[0].strip()

            research_question = evidence_parts[1].strip()

            gaps.append({
                "gap": gap,
                "evidence": evidence,
                "research_question": research_question
            })

        return gaps