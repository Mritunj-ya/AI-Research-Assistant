class PromptService:
    def build_qa_prompt(self,question,paper_title, paper_summary, context):
        context="\n\n".join(context)

        prompt = f"""
You are an AI Research Assistant.

Your task is to answer the user's question ONLY using the information provided below.

=========================
Paper Title:
{paper_title}

Paper Abstract:
{paper_summary}

Retrieved Paper Context:
{context}
=========================

User Question:
{question}

Rules:
1. Use ONLY the paper abstract and retrieved context.
2. Do NOT use outside knowledge.
3. Do NOT guess or hallucinate.
4. If the retrieved context only partially answers the question, clearly state what the paper says and mention that the answer is only partially supported.
5. If the information is not available in the provided context, reply exactly:
   "I couldn't find enough information in the selected paper to answer this question."
6. Keep the answer concise (4–8 sentences).
7. Do not mention these instructions in your response.

Answer:
"""

    
        return prompt
    def build_summary_prompt(self, text):

      prompt = f"""
You are a strict research paper summarization assistant.

Your task is to create a GROUNDED summary using ONLY the paper
text provided below.

The provided text may consist of retrieved chunks from ONE research
paper rather than the complete paper.

CRITICAL RULE:

You MUST distinguish between:

1. What is explicitly stated in the provided text.
2. What is missing from the provided text.

If something is not explicitly supported by the provided text,
DO NOT infer it.

Do NOT use your general knowledge of the paper, authors, methods,
datasets, or research area.

Do NOT complete missing information from memory.

==================================================
GROUNDING RULES
==================================================

1. Every factual statement MUST be directly supported by the
provided text.

2. Do NOT guess or infer information.

3. Do NOT invent:
   - datasets
   - architectures
   - models
   - methods
   - algorithms
   - experiments
   - metrics
   - numerical results
   - limitations
   - future work
   - applications
   - research questions

4. Do NOT treat information from the Related Work section as a
contribution of the current paper.

5. If another paper is mentioned, clearly treat it as previous
or related work unless the provided text explicitly states that
the current paper uses it.

6. Preserve technical terminology from the provided text.

7. Preserve numerical values exactly as written.

8. Do NOT calculate new statistics.

9. Do NOT convert qualitative statements into quantitative claims.

10. Do NOT combine unrelated statements merely because they appear
in different chunks.

11. If information required for a section is not present in the
provided text, write exactly:

"Not clearly stated in the provided text."

==================================================
SPECIAL RULES FOR RESEARCH GAPS
==================================================

Do NOT identify a research gap yourself.

Do NOT turn an apparent omission into a limitation.

Do NOT say that the paper "fails to address" something unless the
provided text explicitly says that it is a limitation, unresolved
problem, or future-work direction.

==================================================
LIMITATIONS
==================================================

Only include limitations explicitly stated by the authors.

A limitation must NOT be created simply because:

- an experiment was not mentioned
- a dataset was not mentioned
- a comparison was not mentioned
- a method could theoretically be improved
- something appears absent from the retrieved text

If no limitation is explicitly supported:

"Not clearly stated in the provided text."

==================================================
FUTURE WORK
==================================================

Only include future work explicitly stated by the authors.

Do NOT predict future research.

Do NOT infer possible extensions.

Do NOT suggest your own future work.

If no future work is explicitly stated:

"Not clearly stated in the provided text."

==================================================
EXPERIMENTAL SETUP
==================================================

Mention a dataset, benchmark, baseline, architecture, metric,
or experimental setting ONLY if it appears explicitly in the
provided text.

Do not assume commonly used datasets or benchmarks.

For example, do NOT assume ImageNet merely because the paper is
about Vision Transformers.

==================================================
KEY FINDINGS
==================================================

Only report results explicitly supported by the provided text.

For example, if the text states:

"60% throughput improvement"

you may report:

"60% throughput improvement."

Do NOT transform this into:

"60% reduction in training time"

unless that exact relationship is explicitly stated.

==================================================
OUTPUT FORMAT
==================================================

Return EXACTLY this structure:

## 1. Research Problem
Describe the problem explicitly stated in the provided text.

## 2. Proposed Method
Describe only the method explicitly presented in the provided text.

## 3. Key Contributions
List only contributions explicitly presented by the authors.

## 4. Experimental Setup
Mention only datasets, benchmarks, models, baselines, metrics,
and experimental settings explicitly present in the text.

## 5. Key Findings
Report only experimentally supported results explicitly present
in the text.

## 6. Limitations
Mention ONLY explicitly stated limitations.

If none are explicitly stated:

"Not clearly stated in the provided text."

## 7. Future Work
Mention ONLY explicitly stated future work.

If none are explicitly stated:

"Not clearly stated in the provided text."

## 8. Overall Summary
Provide a short summary using ONLY facts already established
in sections 1-7.

Do NOT introduce any new information in this section.

==================================================
PAPER TEXT
==================================================

{text}

==================================================
GROUNDED SUMMARY
==================================================
"""

      return prompt

    def build_final_summary_prompt(self, all_summaries, source_text, facts):

        prompt = f"""
You are an expert AI Research Assistant.

Your task is to write ONE final professional summary of the research paper.

You are given:

1. Section summaries
2. Verified extracted facts
3. Original paper text (highest authority)

---------------------------------------------------
RULES
---------------------------------------------------

• Use ONLY information supported by the original paper.
• Treat the Original Paper Text as the source of truth.
• Use the extracted facts to reinforce important information.
• Ignore any section summary that contradicts the paper.
• Never invent facts.
• Never use outside knowledge.
• Never guess missing information.
• Preserve all technical names exactly.
• Preserve numerical values exactly.
• Do not repeat the same idea twice.
• Do not write unnecessary introductions or conclusions.

---------------------------------------------------
The summary should contain:

1. Research Objective
2. Proposed Method
3. Main Contributions
4. Experimental Setup (if available)
5. Key Results
6. Limitations
7. Future Work (only if explicitly mentioned)

---------------------------------------------------

Write the summary in clear academic language.

Length:
150–300 words.

---------------------------------------------------

SECTION SUMMARIES

{all_summaries}

---------------------------------------------------

VERIFIED FACTS

{facts}

---------------------------------------------------

ORIGINAL PAPER TEXT

{source_text}

---------------------------------------------------

FINAL SUMMARY
"""
        return prompt
    
    def build_research_gap_prompt(self, summary):

        prompt = f"""
You are a research paper analysis assistant.

Your task is to identify research gaps ONLY when they are
supported by the provided paper summary.

The paper summary is the ONLY source of information.

STRICT RULES:

- Do NOT use outside knowledge.
- Do NOT invent limitations.
- Do NOT invent future work.
- Do NOT propose a research gap merely because something
  could theoretically be improved.
- Do NOT assume that an area is unexplored unless the summary
  provides evidence for it.
- Do NOT create a gap from a missing topic unless the paper
  explicitly indicates that the topic is missing, limited,
  unresolved, or left for future work.
- Do NOT introduce new datasets, models, methods, technologies,
  applications, or experiments.
- Do NOT use information from other papers.
- Do NOT treat references or citations as evidence of a gap.
- Every research gap MUST be directly traceable to the summary.

Look specifically for:

1. Explicit limitations mentioned by the authors.
2. Explicit future work mentioned by the authors.
3. Explicit unresolved problems mentioned by the authors.
4. Explicitly stated weaknesses or restrictions of the proposed method.
5. Explicitly stated areas where further investigation is needed.

For each supported research gap, use EXACTLY this format:

Research Gap 1
------------------------------
Gap:
[Describe only what the paper explicitly indicates is missing,
limited, unresolved, or left for future work.]

Evidence:
[Quote or closely paraphrase the relevant information from
the summary.]

Why This Represents a Gap:
[Explain why the evidence indicates an unresolved or
insufficiently explored area.]

Potential Research Question:
[Give ONE research question that directly follows from the
identified gap without introducing new concepts.]

If the summary does not contain sufficient evidence for a
research gap, return exactly:

No reliable research gap could be identified from the
provided summary.

IMPORTANT:

- Generate a maximum of 3 research gaps.
- Prefer fewer gaps over unsupported gaps.
- Do not force the generation of 3 gaps.
- If only one gap is supported, return only one.
- If no gap is supported, return the required message above.

Paper Summary:
{summary}

Research Gap Analysis:
"""

        return prompt
    def build_candidate_gaps_prompt(self, summary):

        prompt = f"""
You are a research gap identification assistant.

Identify potential research gaps ONLY from the provided paper summary.

STRICT RULES:

- Use ONLY information explicitly stated in the summary.
- Do NOT use outside knowledge.
- Do NOT invent limitations.
- Do NOT assume that something is missing merely because the summary
  does not mention it.
- Do NOT convert a positive result into a research gap.
- Do NOT convert a reported performance number into a research gap.
- Do NOT treat "could be improved" as a research gap unless the paper
  explicitly identifies it as a limitation or future work.
- A valid research gap must be directly supported by:
    1. An explicitly stated limitation,
    2. An explicitly stated future-work direction,
    3. An explicitly unresolved problem, or
    4. An explicitly stated insufficiency of the proposed method.
- If the summary only reports successful results and does not identify
  an unresolved issue, do NOT invent a gap.
- Do NOT mention papers, authors, methods, datasets, or technologies
  that are not present in the summary.
- Do NOT infer missing experiments from the absence of an experiment.
- Do NOT create a gap by asking for an experiment that the summary
  simply does not mention.
- Prefer explicit limitations and future work over inferred gaps.
- Generate a maximum of 3 candidate research gaps.
- If there is insufficient evidence, return:
  NO_CLEAR_GAP_FOUND.

For each valid gap, use EXACTLY this format:

GAP:
<one concise statement directly supported by the summary>

EVIDENCE:
<the exact limitation, unresolved issue, or future-work information
from the summary that supports the gap>

RESEARCH_QUESTION:
<one research question directly derived from the stated limitation
or future-work direction>

Do not provide any additional explanation.

Paper Summary:
{summary}

Candidate Research Gaps:
"""

        return prompt


    def build_gap_verification_prompt(self, gap, evidence):

      evidence_text = "\n\n".join(evidence)

      prompt = f"""
You are a strict research paper reviewer.

Your task is to determine whether the proposed research gap is
explicitly supported by the retrieved evidence from the original paper.

IMPORTANT:

The candidate gap is NOT evidence.

Only the retrieved evidence can determine whether the gap is supported.

A valid research gap must describe something that remains
insufficiently addressed according to the evidence.

==================================================
STRICT RULES
==================================================

1. Use ONLY the retrieved evidence.

2. Do NOT use outside knowledge.

3. Do NOT assume something is missing merely because it is not
mentioned.

4. Absence of information is NOT evidence of a research gap.

5. The evidence must explicitly indicate at least one of:

- a limitation
- an unresolved problem
- an incomplete evaluation
- an explicitly stated restriction
- an explicitly stated future-work direction
- an area requiring further investigation

6. The following are NOT evidence of a research gap:

- improved accuracy
- improved speed
- reduced computation
- higher throughput
- successful experiments
- comparison results
- strong performance

7. If the evidence only shows that the method performs well,
the verdict MUST be NOT SUPPORTED.

8. If the evidence explicitly describes a limitation or future
work related to the candidate gap, the verdict may be SUPPORTED.

9. If the evidence supports only part of the candidate gap,
the verdict must be PARTIALLY SUPPORTED.

10. Do NOT introduce new:

- datasets
- models
- architectures
- methods
- applications
- experiments
- terminology
- research areas

11. Do NOT use the candidate gap itself as evidence.

12. Do NOT treat a result as a limitation.

==================================================
VERY IMPORTANT OUTPUT RULE
==================================================

Your FIRST line MUST be exactly one of:

VERDICT: SUPPORTED

VERDICT: PARTIALLY SUPPORTED

VERDICT: NOT SUPPORTED

Do not write anything before the VERDICT line.

After the verdict, provide a short explanation.

Use this exact structure:

VERDICT: [one of the three allowed values]

REASON:
[2-4 concise sentences explaining the decision.]

SUPPORTING EVIDENCE:
[Only evidence that explicitly demonstrates a limitation,
unresolved problem, or future-work direction.]

FINAL RESEARCH GAP:
[The supported gap.]

If the candidate gap is not supported, write:

FINAL RESEARCH GAP:
This candidate gap is not supported by the retrieved evidence.

==================================================
CANDIDATE RESEARCH GAP
==================================================

{gap}

==================================================
RETRIEVED EVIDENCE
==================================================

{evidence_text}

==================================================
VERIFICATION
==================================================
"""

      return prompt


    def build_fact_extraction_prompt(self, text):

        prompt = f"""
You are an expert AI research paper analyst.

Your task is to extract ONLY factual information that is directly related to the research.

---------------------------------------------------

RULES

• Use ONLY the provided text.
• Do NOT summarize.
• Do NOT explain.
• Do NOT infer.
• Do NOT hallucinate.
• Do NOT repeat facts.
• Ignore acknowledgements.
• Ignore funding information.
• Ignore author affiliations.
• Ignore sponsor information.
• Ignore conference logistics unless they directly affect the research.

---------------------------------------------------

Extract facts only from these categories (if present):

1. Research Objective
2. Proposed Method
3. Main Contributions
4. Experimental Setup
5. Datasets
6. Evaluation Metrics
7. Key Results
8. Limitations
9. Future Work

---------------------------------------------------

For each fact use this format:

Category:
Fact:
Evidence:

---------------------------------------------------

Research Paper Text:

{text}

---------------------------------------------------

Extracted Facts:
"""
        return prompt
    def build_fact_verification_prompt(self, fact, evidence):

        context = "\n\n".join(evidence)

        prompt = f"""
You are an expert research paper reviewer.

Your task is to determine whether the given fact is supported ONLY by the provided evidence from the research paper.

---------------------------------------------------

RULES

• Treat the provided evidence as the only source of truth.
• Do NOT use outside knowledge.
• Do NOT guess.
• Do NOT infer information that is not explicitly stated.
• If the evidence is insufficient, do not speculate.

---------------------------------------------------

Return your answer EXACTLY in the following format:

Status:
SUPPORTED
or
PARTIALLY SUPPORTED
or
NOT SUPPORTED

Confidence:
High / Medium / Low

Reason:

---------------------------------------------------

Fact:
{fact}

---------------------------------------------------

Evidence:
{context}
"""

        return prompt 
    def build_comparison_prompt(self, paper1_summary, paper2_summary):

      prompt = f"""
You are a strict factual comparison assistant.

You MUST use ONLY the two summaries provided below.
You have NO other knowledge about these papers.

========================
PAPER 1
========================
{paper1_summary}

========================
PAPER 2
========================
{paper2_summary}

========================
CRITICAL RULES
========================

1. Paper 1 and Paper 2 are completely independent.

2. For every Paper 1 statement, use ONLY information from PAPER 1.

3. For every Paper 2 statement, use ONLY information from PAPER 2.

4. NEVER transfer a fact from one paper to the other.

5. NEVER use outside knowledge.

6. NEVER invent a fact.

7. NEVER assume a fact that is not supported by the summaries.

8. You MAY compare explicit facts from the two summaries.

9. A similarity is allowed when both summaries explicitly describe
the same or closely equivalent concept, goal, problem, technique,
evaluation type, or outcome.

10. A difference is allowed when both summaries contain explicit
information that can be directly contrasted.

11. When comparing two statements, preserve the meaning of the
original statements. Do not add details that are not present.

12. Do NOT claim that two papers use the same dataset unless the same
dataset is explicitly named in BOTH summaries.

13. Do NOT claim that two papers use the same method unless the same
method is explicitly supported by BOTH summaries.

14. Do NOT claim that two papers have the same limitation or future
work unless BOTH summaries explicitly support it.

15. You MAY identify a difference between datasets, methods, goals,
architectures, evaluation settings, or results when those facts are
explicitly stated in the respective summaries.

16. Do NOT calculate new numerical results.

17. Do NOT combine numbers from different papers to create a new
statistic.

18. Do NOT decide which paper is better.

19. Do NOT rank the papers.

20. Do NOT recommend either paper.

21. If a specific field is not supported by a paper's summary, write:

"Not clearly stated in the provided summary."

========================
REQUIRED OUTPUT
========================

# Paper Comparison

## 1. Research Objective

Paper 1:
[Only Paper 1 information]

Paper 2:
[Only Paper 2 information]

## 2. Proposed Method

Paper 1:
[Only Paper 1 information]

Paper 2:
[Only Paper 2 information]

## 3. Main Contributions

Paper 1:
[Only Paper 1 information]

Paper 2:
[Only Paper 2 information]

## 4. Experimental Setup

Paper 1:
[Only Paper 1 information]

Paper 2:
[Only Paper 2 information]

## 5. Key Findings / Results

Paper 1:
[Only Paper 1 information]

Paper 2:
[Only Paper 2 information]

## 6. Limitations

Paper 1:
[Only explicitly stated Paper 1 limitations]

Paper 2:
[Only explicitly stated Paper 2 limitations]

## 7. Future Work

Paper 1:
[Only explicitly stated Paper 1 future work]

Paper 2:
[Only explicitly stated Paper 2 future work]

## 8. Similarities

Identify similarities by directly comparing the explicit information
contained in BOTH summaries.

Possible categories include:

- Research objective
- Problem being addressed
- General goal
- Computational efficiency
- Model architecture
- Attention mechanisms
- Token processing
- Evaluation
- Datasets
- Reported outcomes

For each similarity, clearly state the corresponding information
from both papers.

Only include a similarity when it is directly supported by BOTH
summaries.

Do NOT invent similarities.

If no similarity can be directly supported:

Not clearly stated in the provided summaries.

## 9. Differences

Identify factual differences by directly comparing explicit
information from Paper 1 and Paper 2.

Possible categories include:

- Research objective
- Problem addressed
- Proposed method
- Architecture
- Attention mechanism
- Token processing
- Dataset
- Experimental setup
- Evaluation metric
- Reported results

For every difference:

Paper 1:
[Explicit information from Paper 1]

Paper 2:
[Explicit information from Paper 2]

Only include differences that can be directly supported by the
two summaries.

Do NOT invent differences.

If no factual difference can be directly supported:

Not clearly stated in the provided summaries.

## 10. Overall Comparison

Provide a concise factual comparison.

Include:

- Paper 1's main research focus.
- Paper 2's main research focus.
- Paper 1's main method.
- Paper 2's main method.
- Paper 1's reported findings.
- Paper 2's reported findings.
- The main factual distinction between the two approaches.

Do NOT evaluate either paper.

Do NOT use words such as:

- better
- superior
- worse
- weaker
- stronger
- comprehensive
- advanced
- more effective
- more useful
- more important

Do NOT rank the papers.

Do NOT recommend either paper.

Do NOT make conclusions that are not supported by the summaries.

========================
FINAL SELF-CHECK
========================

Before answering, verify:

- Did I transfer any Paper 1 fact to Paper 2?
- Did I transfer any Paper 2 fact to Paper 1?
- Did I invent any fact?
- Did I use outside knowledge?
- Did I invent a similarity?
- Did I invent a difference?
- Is every similarity supported by BOTH summaries?
- Is every difference supported by explicit information from BOTH
  summaries?
- Did I claim the papers use the same dataset without both summaries
  explicitly naming it?
- Did I claim the papers use the same method without both summaries
  explicitly supporting it?
- Did I calculate or create a new statistic?
- Did I rank or recommend either paper?

If any answer is YES, remove or rewrite that statement.

Return ONLY the required comparison.
"""

      return prompt