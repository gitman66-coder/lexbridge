from knowledge.case_state import CaseState
from knowledge.llm import generate_response

import json

def triage_agent(state: CaseState) -> CaseState:
    legal_issue = state.get("legal_issue", "")
    jurisdiction = state.get("jurisdiction", "")
    facts = state.get("facts", "")
    legal_area = state.get("legal_area", "")
    findings = state.get("findings", "")
    unresolved_questions = state.get("unresolved_questions", [])

    prompt = f"""
            You are the Triage Agent in LexBridge, a legal assistance system.

            Your job is to assess the urgency of a legal case so that it can be
            prioritized for human lawyer review.

            Case information:

            Legal area:
            {legal_area}

            Legal issue:
            {legal_issue}

            Jurisdiction:
            {jurisdiction}

            Facts:
            {facts}

            Research findings:
            {findings}

            Unresolved questions:
            {unresolved_questions}

            Instructions:

            - Assess urgency using only the information provided.
            - Consider immediate harm, deadlines, eviction, detention,
            violence, loss of rights, or other time-sensitive circumstances.
            - Do not invent facts.
            - Do not provide legal advice.
            - Do not make a final legal conclusion.
            - Do not determine whether the user will win or lose.
            - Give an urgency score from 0 to 100.
            - Assign exactly one priority:
            LOW, MEDIUM, HIGH, or CRITICAL.
            - Explain the reason briefly.
            - Return ONLY valid JSON.
            - Do not use markdown or code fences.

            Return exactly:

            {{
                "urgency_score": 0,
                "priority": "LOW",
                "triage_reason": "Brief explanation"
            }}
            """

    response = generate_response(prompt).strip()

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("The response from the LLM is not valid JSON.")

    return {
        **state,
        "urgency_score": int(data.get("urgency_score", 0)),
        "priority": data.get("priority", "LOW"),
        "triage_reason": data.get("triage_reason", "")
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

        "findings": (
            "The Telangana Buildings (Lease, Rent and Eviction) "
            "Control Act, 1960 may apply to residential eviction "
            "proceedings in Hyderabad."
        ),

        "unresolved_questions": [
            "What notice requirements apply?",
            "Is verbal notice sufficient?"
        ]
    }

    result = triage_agent(test_state)

    print("\n=== TRIAGE RESULT ===")
    print(result)

    print("\nUrgency Score:", result.get("urgency_score", ""))
    print("Priority:", result.get("priority", ""))
    print("Reason:", result.get("triage_reason", ""))
