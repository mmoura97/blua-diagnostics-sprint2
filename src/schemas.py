from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict, total=False):
    user_input: str
    intent: str
    patient_id: str
    patient: Dict[str, Any]
    rag_documents: List[Dict[str, Any]]
    tool_calls: List[str]
    agent_path: List[str]
    response: str
    red_flag: bool
    out_of_scope: bool
    jailbreak: bool
    score: float
    started_at: float
    elapsed_ms: float
