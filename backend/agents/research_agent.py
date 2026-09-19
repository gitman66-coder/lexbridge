from knowledge.case_state import CaseState
from knowledge.llm import generate_response
from knowledge.retriever import search_legal_documents

import json

from database import SessionLocal


def research_agent(state: CaseState) -> CaseState:

    legal_issue = state.get("legal_issue", "")
    jurisdiction = state.get("jurisdiction", "")
    facts = state.get("facts", "")

    search_query = f"""
        Legal issue: {legal_issue}
        Jurisdiction: {jurisdiction}
        Facts: {facts}
        """.strip()

    db = SessionLocal()

    try:
        chunks = search_legal_documents(
            search_query,
            top_k=5,
            db=db
        )

        retrieved_chunks = []

        for chunk in chunks:
            retrieved_chunks.append({
                "query": search_query,
                "document_id": chunk.document_id,
                "section": chunk.section,
                "content": chunk.content
            })

    finally:
        db.close()

    legal_context = "\n\n".join(
        f"Document: {chunk['document_id']}\n"
        f"Section: {chunk['section']}\n"
        f"Content: {chunk['content']}"
        for chunk in retrieved_chunks
    )

    analysis_prompt = f"""
                    You are the Research Agent in LexBridge, a legal assistance system.

                    Analyze the legal information retrieved from the curated legal
                    knowledge base for the given case.

                    Case:
                    Legal issue: {legal_issue}
                    Jurisdiction: {jurisdiction}
                    Facts: {facts}

                    Retrieved legal information:
                    {legal_context}

                    Instructions:
                    - Base your findings only on the retrieved legal information.
                    - Do not invent laws, sections, or facts.
                    - Identify the relevant legal sections.
                    - Identify the sources used.
                    - Identify important information that is still missing.
                    - Do not make a final legal decision.
                    - Keep the findings concise.
                    - Return ONLY valid JSON.
                    - Do not use markdown or code fences.

                    Return exactly this structure:

                    {{
                        "findings": "string",
                        "relevant_sections": ["string"],
                        "sources": ["string"],
                        "unresolved_questions": ["string"]
                    }}
                    """

    response = generate_response(analysis_prompt).strip()

    try:
        analysis_data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError(
            "The response from the LLM is not valid JSON."
        )

    return {
        **state,
        "research_queries": [search_query],
        "retrieved_chunks": retrieved_chunks,
        "findings": analysis_data.get("findings", ""),
        "relevant_sections": analysis_data.get(
            "relevant_sections", []
        ),
        "sources": analysis_data.get(
            "sources", []
        ),
        "unresolved_questions": analysis_data.get(
            "unresolved_questions", []
        )
    }