from __future__ import annotations
import json, time
from pathlib import Path
from collections import defaultdict
from src.graph.workflow import run_blua

EVAL_SET = Path("evals/sprint2_eval_set.json")
RESULTS = Path("evals/sprint2_results.json")
SUMMARY = Path("evals/sprint2_metrics.json")

def evaluate_case(case):
    started = time.time()
    result = run_blua(case["entrada_usuario"])
    elapsed = round((time.time() - started) * 1000, 2)

    intent_ok = result.get("intent") == case["expected_intent"]
    escalation_ok = bool(result.get("red_flag", False)) == bool(case["expected_escalation"])
    rag_ok = len(result.get("rag_documents", [])) > 0
    response_ok = bool(result.get("response"))

    score = sum([intent_ok, escalation_ok, rag_ok, response_ok]) / 4
    qualitative = "adequada" if score >= 0.85 else "parcial" if score >= 0.5 else "inadequada"

    return {
        "id": case["id"],
        "categoria": case["categoria"],
        "pergunta": case["entrada_usuario"],
        "resposta_obtida": result.get("response", ""),
        "intent_esperada": case["expected_intent"],
        "intent_obtida": result.get("intent"),
        "trajetoria_agentes": result.get("agent_path", []),
        "tools_chamadas": result.get("tool_calls", []),
        "documentos_recuperados": [
            {"doc_id": d["doc_id"], "chunk_id": d["chunk_id"], "score": d["score"]}
            for d in result.get("rag_documents", [])
        ],
        "avaliacao_qualitativa": qualitative,
        "score_numerico": round(score, 2),
        "tempo_resposta_ms": result.get("elapsed_ms", elapsed),
        "custo_estimado_conversa_usd": 0.0,
        "observacao_custo": "Uso via Ollama/execucao_ollama acadêmico sem custo de API paga."
    }

def main():
    cases = json.loads(EVAL_SET.read_text(encoding="utf-8"))
    results = [evaluate_case(c) for c in cases]
    RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    by_cat = defaultdict(list)
    for r in results:
        by_cat[r["categoria"]].append(r["score_numerico"])

    metrics = {
        "total_casos": len(results),
        "acuracia_geral": round(sum(r["score_numerico"] for r in results) / len(results), 3),
        "acuracia_por_categoria": {
            cat: round(sum(vals) / len(vals), 3)
            for cat, vals in by_cat.items()
        },
        "taxa_escalada_correta": round(
            sum(1 for r in results if (r["intent_esperada"] == "escalada") == ("escalada_humana" in r["trajetoria_agentes"])) / len(results),
            3,
        ),
        "tempo_medio_resposta_ms": round(sum(r["tempo_resposta_ms"] for r in results) / len(results), 2),
        "custo_estimado_total_usd": 0.0,
        "iteracoes_prompt": [
            {
                "versao": "v1",
                "alteracao": "Prompt básico da Sprint 1",
                "resultado": "bom para memória/tools, fraco em red flags explícitas"
            },
            {
                "versao": "v2",
                "alteracao": "Adição de guardrails, categorias de intent e escalada humana",
                "resultado": "melhorou bloqueio de jailbreak e red flags"
            },
            {
                "versao": "v3",
                "alteracao": "RAG e agentes especializados via LangGraph",
                "resultado": "respostas passaram a incluir documentos recuperados e trajetória auditável"
            }
        ]
    }
    SUMMARY.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
