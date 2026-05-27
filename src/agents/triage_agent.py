from src.agents.prompts import SYSTEM_PROMPT
from src.llm import llm_client
from src.tools.clinical_tools import consultar_historico_paciente, recuperar_dados_wearable

def run_triage_agent(state):
    state.setdefault("agent_path", []).append("triagem")
    state.setdefault("tool_calls", [])

    patient = consultar_historico_paciente("MARIA-34")
    wearable = recuperar_dados_wearable("MARIA-34")
    state["patient"] = patient.get("patient", {})
    state["tool_calls"].extend(["consultar_historico_paciente", "recuperar_dados_wearable"])

    rag_context = "\n\n".join([f"[{d['doc_id']}] {d['content']}" for d in state.get("rag_documents", [])])
    user = state["user_input"]
    prompt = f"Realize triagem segura para: {user}\nPaciente: {state['patient']}\nWearable: {wearable}"

    state["response"] = llm_client.chat(SYSTEM_PROMPT, prompt, rag_context)
    return state
