from knowledge.case_state import CaseState
from knowledge.llm import generate_response

import json

def classification_agent(state: CaseState) -> CaseState:
    legal_issue = state.get("legal_issue", "")
    jurisdiction = state.get("jurisdiction", "")
    facts = state.get("facts", "")

    prompt = f"""
            You are the Classification Agent in LexBridge, a legal assistance system.

            Your job is to classify the user's legal case into the most appropriate legal area.

            Case information:

            Legal issue:
            {legal_issue}

            Jurisdiction:
            {jurisdiction}

            Facts:
            {facts}

            Instructions:
            - Identify the primary area of law involved.
            - Base your classification only on the information provided.
            - Do not invent facts, laws, legal sections, or jurisdiction.
            - Do not provide legal advice.
            - Do not make a final legal conclusion.
            - If multiple legal areas are involved, choose the primary one.
            - Keep the classification_reason concise and explain why the selected legal area fits the case.
            - Return ONLY valid JSON.
            - Do not use markdown or code fences.

            Return exactly this structure:

            {{
                "legal_area": "Primary area of law",
                "classification_reason": "Brief explanation for the classification"
            }}

            """

    response = generate_response(prompt).strip()

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("The response from the LLM is not valid JSON.")

    return {
        **state,
        "legal_area": data.get("legal_area", ""),
        "classification_reason": data.get("classification_reason", "")
    }
