from knowledge.llm import generate_response
from knowledge.case_state import CaseState

import json


def intake_agent(state: CaseState) -> CaseState:

    conversation = state.get("conversation", [])

    conversation_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in conversation
    )

    prompt = f"""
            You are the Intake Agent for a legal assistance system.

            Your job is to collect the information needed to understand a
            person's legal problem.

            Conversation so far:
            {conversation_text}

            Determine what important information is still missing.

            Focus on:
            - What happened
            - When it happened
            - Where it happened
            - Who is involved
            - Important documents or notices
            - What the person wants to achieve

            If important information is missing, generate ONE clear,
            easy-to-understand question.

            Return ONLY valid JSON.

            If information is still missing, use exactly this structure:

            {{
                "intake_complete": false,
                "missing_information": [
                    "ONE clear question for the user"
                ],
                "legal_issue": "",
                "jurisdiction": "",
                "facts": ""
            }}

            If enough information has been collected, use exactly this structure:

            {{
                "intake_complete": true,
                "missing_information": [],
                "legal_issue": "Main legal issue",
                "jurisdiction": "Relevant jurisdiction",
                "facts": "Concise summary of the important facts"
            }}

            Rules:
            - Return ONLY JSON.
            - Do not use markdown.
            - Do not invent facts.
            - Do not invent jurisdiction.
            - Ask only ONE question at a time.
            """

    response = generate_response(prompt).strip()

    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("The response from the LLM is not valid JSON.")

    if data["intake_complete"]:
        return {
            **state,
            "intake_complete": True,
            "missing_information": [],

            "legal_issue": data.get("legal_issue", ""),
            "jurisdiction": data.get("jurisdiction", ""),
            "facts": data.get("facts", "")
        }

    return {
        **state,
        "intake_complete": False,
        "missing_information": data.get("missing_information", [])
    }