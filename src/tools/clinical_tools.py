from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

PATIENT_FILE = Path("data/mock/patient_maria.json")


def _load_patient() -> Dict[str, Any]:
    return json.loads(PATIENT_FILE.read_text(encoding="utf-8"))


def consultar_historico_paciente(patient_id: str = "MARIA-34") -> Dict[str, Any]:
    patient = _load_patient()

    if patient_id != patient["patient_id"]:
        return {
            "status": "not_found",
            "message": "Paciente não localizado na base clínica disponível.",
        }

    return {
        "status": "ok",
        "patient": patient,
    }


def verificar_interacoes_medicamentosas(medicamentos: List[str]) -> Dict[str, Any]:
    meds = " ".join(medicamentos).lower()
    alerts = []

    if "losartana" in meds and "ibuprofeno" in meds:
        alerts.append(
            {
                "risco": "moderado",
                "mensagem": (
                    "Losartana associada a ibuprofeno exige cautela em pacientes "
                    "hipertensos. A decisão deve ser validada por profissional de saúde."
                ),
            }
        )

    if "dipirona" in meds:
        alerts.append(
            {
                "risco": "alto",
                "mensagem": "Há registro de alergia à dipirona para esta paciente.",
            }
        )

    if not alerts:
        alerts.append(
            {
                "risco": "baixo",
                "mensagem": "Nenhuma interação medicamentosa relevante foi identificada na base clínica disponível.",
            }
        )

    return {
        "status": "ok",
        "alerts": alerts,
    }


def agendar_teleconsulta(
    patient_id: str,
    especialidade: str,
    prioridade: str,
) -> Dict[str, Any]:
    return {
        "status": "ok",
        "patient_id": patient_id,
        "especialidade": especialidade,
        "prioridade": prioridade,
        "data_hora": "2026-06-03 14:30",
        "observacao": "Teleconsulta registrada para validação humana antes da confirmação final.",
    }


def recuperar_dados_wearable(patient_id: str = "MARIA-34") -> Dict[str, Any]:
    patient = _load_patient()

    return {
        "status": "ok",
        "patient_id": patient_id,
        "wearables": patient.get("wearables", {}),
        "fonte": "Dados recentes de dispositivo vestível disponíveis para o fluxo de check-up digital.",
    }
