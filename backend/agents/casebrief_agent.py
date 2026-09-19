from knowledge.case_state import CaseState
from knowledge.llm import generate_response

import json

def casebrief_agent(state: CaseState) -> CaseState:
    
    legal_issue = state.get("legal_issue", "")
    jurisdiction = state.get("jurisdiction", "")
    facts = state.get("facts", "")
    legal_area = state.get("legal_area", "")
    classification_reason = state.get("classification_reason", "")

    findings = state.get("findings", "")
    relevant_sections = state.get("relevant_sections", [])
    sources = state.get("sources", [])
    unresolved_questions = state.get("unresolved_questions", [])

    urgency_score = state.get("urgency_score", 0)
    priority = state.get("priority", "")
    triage_reason = state.get("triage_reason", "")

    prompt = f"""
            You are the Case Brief Agent in LexBridge.

            Create a concise, structured case brief for a human lawyer.

            CASE INFORMATION

            Legal area:
            {legal_area}

            Legal issue:
            {legal_issue}

            Jurisdiction:
            {jurisdiction}

            Facts:
            {facts}

            Classification reason:
            {classification_reason}

            LEGAL RESEARCH

            Findings:
            {findings}

            Relevant sections:
            {relevant_sections}

            Sources:
            {sources}

            Unresolved questions:
            {unresolved_questions}

            TRIAGE

            Urgency score:
            {urgency_score}

            Priority:
            {priority}

            Triage reason:
            {triage_reason}

            Instructions:

            - Summarize only information provided in the case state.
            - Do not invent facts, laws, sections, dates, or sources.
            - Clearly distinguish facts from research findings.
            - Include unresolved questions.
            - Include the urgency score and priority.
            - Do not make a final legal decision.
            - Do not claim that the client will win or lose.
            - Do not provide unsupported legal advice.
            - Keep the brief concise and useful to a human lawyer.
            - Return plain text only.
            - Do not use JSON.
            - Do not use markdown code fences.

            Use exactly this structure:

            CASE BRIEF

            Legal Area:
            ...

            Legal Issue:
            ...

            Jurisdiction:
            ...

            Facts:
            ...

            Research Findings:
            ...

            Relevant Legal Sections:
            ...

            Sources:
            ...

            Unresolved Questions:
            ...

            Urgency Score:
            ...

            Priority:
            ...

            Triage Reason:
            ...

            Suggested Next Step:
            ...
            """

    case_brief = generate_response(prompt).strip()

    return {
        **state,
        "case_brief": case_brief
    }


if __name__ == "__main__":

    test_state: CaseState = {

        "case_id": 1,

        "legal_issue": "Residential eviction",

        "jurisdiction": "Hyderabad, Telangana, India",

        "facts": (
            "I have lived in the apartment for two years and have "
            "a rental agreement. The landlord verbally told me to "
            "leave within two weeks."
        ),

        "legal_area": "Property Law",

        "classification_reason": (
            "The case involves residential eviction under a rental "
            "agreement."
        ),

        "findings": (
            "The Telangana Buildings (Lease, Rent and Eviction) "
            "Control Act, 1960 may apply to residential eviction "
            "proceedings in Hyderabad."
        ),

        "relevant_sections": [
            "Section 10 - Eviction of tenants",
            "Section 20 - Appeal process"
        ],

        "sources": [
            "Telangana Buildings (Lease, Rent and Eviction) Control Act, 1960"
        ],

        "unresolved_questions": [
            "What notice requirements apply?",
            "Is verbal notice sufficient?"
        ],

        "urgency_score": 70,

        "priority": "HIGH",

        "triage_reason": (
            "The tenant reports a short timeframe to leave the "
            "property, making the matter potentially time-sensitive."
        )
    }

    result = casebrief_agent(test_state)

    print("\n=== CASE BRIEF RESULT ===\n")

    print(result.get("case_brief", ""))