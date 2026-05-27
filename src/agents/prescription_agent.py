from src.agents.prompts import SYSTEM_PROMPT
from src.llm import llm_client
from src.tools.clinical_tools import consultar_historico_paciente, verificar_interacoes_medicamentosas, agendar_teleconsulta

def run_prescription_agent(state):
    state.setdefault("agent_path", []).append("prescricao")
    state.setdefault("tool_calls", [])

    patient_resp = consultar_historico_paciente("MARIA-34")
    patient = patient_resp.get("patient", {})
    meds = list(patient.get("medicamentos_uso_continuo", []))
    user_text = state["user_input"].lower()
    if "ibuprofeno" in user_text:
        meds.append("ibuprofeno")
    if "dipirona" in user_text:
        meds.append("dipirona")

    interactions = verificar_interacoes_medicamentosas(meds)
    schedule = agendar_teleconsulta("MARIA-34", "Clínico Geral", "moderada")
    state["patient"] = patient
    state["tool_calls"].extend([
        "consultar_historico_paciente",
        "verificar_interacoes_medicamentosas",
        "agendar_teleconsulta",
    ])

    rag_context = "\n\n".join([f"[{d['doc_id']}] {d['content']}" for d in state.get("rag_documents", [])])
    prompt = (
        f"Apoie validação pós-teleconsulta sem prescrever. Usuário: {state['user_input']}\n"
        f"Paciente: {patient}\nInterações: {interactions}\nAgendamento: {schedule}"
    )
    state["response"] = llm_client.chat(SYSTEM_PROMPT, prompt, rag_context)
    return state
