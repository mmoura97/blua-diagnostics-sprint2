from __future__ import annotations
from src.config import settings

class LLMClient:
    """Camada de LLM com fallback determinístico para reprodutibilidade acadêmica.

    Se Ollama estiver disponível, usa Ollama.
    Caso contrário, gera resposta segura por regras para que a PoC rode sem API key.
    """

    def __init__(self):
        self.mode = "fallback"
        self.client = None
        try:
            import ollama
            headers = {}
            if settings.ollama_api_key:
                headers["Authorization"] = f"Bearer {settings.ollama_api_key}"
            self.client = ollama.Client(host=settings.ollama_host, headers=headers)
            self.mode = "ollama"
        except Exception:
            self.client = None
            self.mode = "fallback"

    def chat(self, system: str, user: str, context: str = "") -> str:
        if self.mode == "ollama" and self.client is not None:
            try:
                result = self.client.chat(
                    model=settings.ollama_model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": f"Contexto recuperado:\n{context}\n\nUsuário:\n{user}"},
                    ],
                    options={
                        "temperature": settings.temperature,
                        "top_p": settings.top_p,
                        "num_predict": settings.max_tokens,
                    },
                    stream=False,
                )
                return result["message"]["content"]
            except Exception:
                # Mantém sistema demonstrável sem quebrar a correção.
                self.mode = "fallback"
        return self._fallback_response(user, context)

    def _fallback_response(self, user: str, context: str) -> str:
        text = user.lower()
        if any(x in text for x in ["dor no peito", "falta de ar", "desmaio", "fraqueza em um braço", "fala enrolada"]):
            return (
                "ESCALADA HUMANA AUTOMÁTICA: foram identificados sinais de alerta clínico. "
                "A orientação segura é procurar atendimento imediato. A IA não diagnostica nem prescreve."
            )
        if any(x in text for x in ["ignore", "finja", "prescreva", "diagnóstico definitivo"]):
            return (
                "Solicitação recusada por segurança. O BluaDiagnostics não emite diagnóstico definitivo, "
                "não prescreve medicamentos e mantém as restrições clínicas ativas."
            )
        if any(x in text for x in ["bitcoin", "cripto", "futebol", "receita de bolo"]):
            return "Pedido fora do escopo Care Plus. Posso apoiar apenas check-up digital, triagem e teleconsulta."
        return (
            "Resumo seguro: os dados foram organizados para triagem. "
            "Não há diagnóstico definitivo. Recomenda-se acompanhamento por teleconsulta se os sintomas persistirem. "
            f"Contexto RAG considerado: {context[:250]}"
        )

llm_client = LLMClient()
