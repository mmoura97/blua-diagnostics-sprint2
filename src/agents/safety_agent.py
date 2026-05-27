def run_safety_agent(state):
    state.setdefault("agent_path", []).append("safety")
    state.setdefault("tool_calls", [])
    if state.get("intent") == "jailbreak":
        state["jailbreak"] = True
        state["response"] = (
            "[SEGURANÇA] Solicitação recusada. O BluaDiagnostics não ignora suas regras, "
            "não assume papel de médico, não diagnostica e não prescreve."
        )
    else:
        state["out_of_scope"] = True
        state["response"] = (
            "Pedido fora do escopo. O BluaDiagnostics responde apenas sobre check-up digital, "
            "triagem, teleconsulta e contexto Care Plus."
        )
    return state
