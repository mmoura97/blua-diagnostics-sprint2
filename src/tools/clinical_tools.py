from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List

PATIENT_FILE = Path("data/mock/patient_maria.json")

def _load_patient() -> Dict[str, Any]:
    return json.loads(PATIENT_FILE.read_text(encoding="utf-8"))

def consultar_historico_paciente(patient_id: str = "MARIA-34") -> Dict[str, Any]:
    patient = _load_patient()
    if patient_id != patient["patient_id"]:
        return {"status": "not_found", "message": "Paciente não encontrado na base simulada."}
    return {"status": "ok", "patient": patient}

def verificar_interacoes_medicamentosas(medicamentos: List[str]) -> Dict[str, Any]:
    meds = " ".join(medicamentos).lower()
    alerts = []
    if "losartana" in meds and "ibuprofeno" in meds:
        alerts.append({
            "risco": "moderado",
            "mensagem": "Losartana + ibuprofeno pode exigir cautela em paciente hipertenso."
        })
    if "dipirona" in meds:
        alerts.append({
            "risco": "alto",
            "mensagem": "Paciente Maria possui alergia simulada a dipirona."
        })
    if not alerts:
        alerts.append({"risco": "baixo", "mensagem": "Nenhuma interação relevante encontrada na base simulada."})
    return {"status": "ok", "alerts": alerts}

def agendar_teleconsulta(patient_id: str, especialidade: str, prioridade: str) -> Dict[str, Any]:
    return {
        "status": "agendamento_simulado",
        "patient_id": patient_id,
        "especialidade": especialidade,
        "prioridade": prioridade,
        "data_hora": "2026-06-03 14:30",
        "observacao": "Agendamento simulado. Requer confirmação humana."
    }

def recuperar_dados_wearable(patient_id: str = "MARIA-34") -> Dict[str, Any]:
    patient = _load_patient()
    return {
        "status": "ok",
        "patient_id": patient_id,
        "wearables": patient.get("wearables", {}),
        "fonte": "Apple Health / Google Fit mockado"
    }
