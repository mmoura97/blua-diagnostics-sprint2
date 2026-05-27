def run_escalation_agent(state):
    state.setdefault("agent_path", []).append("escalada_humana")
    state.setdefault("tool_calls", [])
    state["red_flag"] = True
    state["response"] = (
        "🔴 ESCALADA HUMANA AUTOMÁTICA — Foram identificados sinais de alerta clínico. "
        "Oriente atendimento imediato/teleconsulta urgente conforme protocolo Care Plus. "
        "A IA não diagnostica, não prescreve e não substitui profissional de saúde."
    )
    return state
