from __future__ import annotations
import time
from langgraph.graph import StateGraph, END
from src.schemas import AgentState
from src.guardrails import classify_intent, detect_red_flag, detect_jailbreak, detect_out_of_scope
from src.rag.retriever import get_retriever
from src.agents.triage_agent import run_triage_agent
from src.agents.prescription_agent import run_prescription_agent
from src.agents.escalation_agent import run_escalation_agent
from src.agents.safety_agent import run_safety_agent

retriever = get_retriever()

def supervisor_node(state: AgentState) -> AgentState:
    state["started_at"] = state.get("started_at", time.time())
    state.setdefault("agent_path", []).append("supervisor")
    user_input = state["user_input"]
    state["intent"] = classify_intent(user_input)
    state["red_flag"] = detect_red_flag(user_input)
    state["jailbreak"] = detect_jailbreak(user_input)
    state["out_of_scope"] = detect_out_of_scope(user_input)
    state["rag_documents"] = retriever.retrieve(user_input, top_k=3)
    return state

def route_from_supervisor(state: AgentState) -> str:
    if state.get("jailbreak") or state.get("out_of_scope"):
        return "safety"
    if state.get("red_flag") or state.get("intent") == "escalada":
        return "escalada"
    if state.get("intent") == "prescricao":
        return "prescricao"
    return "triagem"

def finish_node(state: AgentState) -> AgentState:
    state.setdefault("agent_path", []).append("final")
    state["elapsed_ms"] = round((time.time() - state.get("started_at", time.time())) * 1000, 2)
    return state

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("triagem", run_triage_agent)
    graph.add_node("prescricao", run_prescription_agent)
    graph.add_node("escalada", run_escalation_agent)
    graph.add_node("safety", run_safety_agent)
    graph.add_node("final", finish_node)

    graph.set_entry_point("supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "triagem": "triagem",
            "prescricao": "prescricao",
            "escalada": "escalada",
            "safety": "safety",
        },
    )

    graph.add_edge("triagem", "final")
    graph.add_edge("prescricao", "final")
    graph.add_edge("escalada", "final")
    graph.add_edge("safety", "final")
    graph.add_edge("final", END)
    return graph.compile()

compiled_graph = build_graph()

def run_blua(user_input: str) -> AgentState:
    initial: AgentState = {
        "user_input": user_input,
        "patient_id": "MARIA-34",
        "tool_calls": [],
        "agent_path": [],
    }
    return compiled_graph.invoke(initial)
