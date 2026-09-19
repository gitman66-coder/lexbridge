from langgraph.graph import StateGraph, START, END

from knowledge.case_state import CaseState

from agents.classification_agent import classification_agent
from agents.intake_agent import intake_agent
from agents.research_agent import research_agent
from agents.triage_agent import triage_agent
from agents.casebrief_agent import casebrief_agent

graph = StateGraph(CaseState)

graph.add_node("intake_agent", intake_agent)
graph.add_node("classification_agent", classification_agent)
graph.add_node("research_agent", research_agent)
graph.add_node("triage_agent", triage_agent)
graph.add_node("casebrief_agent", casebrief_agent)

graph.add_edge(START, "intake_agent")

def intake_router(state: CaseState):
    if state.get("intake_complete", False):
        return "classification_agent"

    return END


graph.add_conditional_edges(
    "intake_agent",
    intake_router,
    {
        "classification_agent": "classification_agent",
        END: END
    }
)
  
graph.add_edge("classification_agent", "research_agent")
graph.add_edge("research_agent", "triage_agent")
graph.add_edge("triage_agent", "casebrief_agent")
graph.add_edge("casebrief_agent", END)

case_pipeline = graph.compile()

