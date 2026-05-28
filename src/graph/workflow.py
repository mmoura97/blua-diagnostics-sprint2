from __future__ import annotations

import time

from langgraph.graph import END, StateGraph

from src.agents.escalation_agent import run_escalation_agent
from src.agents.prescription_agent import run_prescription_agent
from src.agents.safety_agent import run_safety_agent
from src.agents.triage_agent import run_triage_agent
from src.guardrails import (
    classify_intent,
    detect_jailbreak,
    detect_out_of_scope,
    detect_red_flag,
)
from src.rag.retriever import get_retriever
from src.schemas import AgentState


retriever = get_retriever()


def _public_agent_name(state: AgentState) -> str:
    path = state.get("agent_path", [])
    intent = state.get("intent")

    if "escalada_humana" in path:
        return "Escalada Humana"

    if "prescricao" in path or intent == "prescricao":
        return "Avaliação de Medicamentos"

    if "safety" in path:
        return "Validação de Segurança"

    if "triagem" in path:
        return "Triagem Clínica"

    return "Supervisor Clínico IA"


def _public_intent_name(intent: str | None) -> str:
    labels = {
        "triagem": "Check-up digital",
        "prescricao": "Avaliação de medicamentos",
        "escalada": "Alerta clínico",
        "jailbreak": "Solicitação bloqueada",
        "out_of_scope": "Fora de escopo",
    }

    return labels.get(intent or "", intent or "Não classificado")


def _build_public_trajectory(state: AgentState) -> list[str]:
    intent = state.get("intent")
    path = state.get("agent_path", [])
    docs = state.get("rag_documents", [])
    tools = state.get("tool_calls", [])

    trajectory: list[str] = ["supervisor"]

    if docs:
        trajectory.append("rag_retriever")

    if "triagem" in path:
        trajectory.append("triagem")

    if "prescricao" in path:
        trajectory.append("prescricao")

    if "safety" in path:
        trajectory.append("safety")

    if "escalada_humana" in path:
        trajectory.append("escalada_humana")

    if tools:
        trajectory.append("servicos_clinicos")

    if state.get("red_flag") or intent == "escalada":
        trajectory.append("guardrails_clinicos")

    trajectory.append("final")

    # Remove duplicados preservando ordem
    unique = []
    seen = set()
    for step in trajectory:
        if step not in seen:
            unique.append(step)
            seen.add(step)

    return unique


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

    state["elapsed_ms"] = round(
        (time.time() - state.get("started_at", time.time())) * 1000,
        2,
    )

    state["trajectory"] = _build_public_trajectory(state)
    state["tools_called"] = list(state.get("tool_calls", []))
    state["retrieved_documents"] = list(state.get("rag_documents", []))
    state["agent"] = _public_agent_name(state)
    state["intent_label"] = _public_intent_name(state.get("intent"))
    state["escalation"] = bool(
        state.get("red_flag")
        or state.get("intent") == "escalada"
        or "escalada_humana" in state.get("agent_path", [])
    )

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
        "rag_documents": [],
    }

    return compiled_graph.invoke(initial)
