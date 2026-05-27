from __future__ import annotations

from src.config import settings


class OllamaLLMClient:
    """
    Cliente oficial do projeto.

    Execução principal:
    - Ollama Cloud
    - API key via variável de ambiente OLLAMA_API_KEY
    - Host padrão: https://ollama.com

    O modo acadêmico sem LLM existe apenas para teste local de fluxo quando
    o avaliador/desenvolvedor não possui uma chave configurada. Ele não é o
    modo principal da entrega.
    """

    def __init__(self, model: str | None = None, host: str | None = None):
        self.model = model or settings.ollama_model
        self.host = host or settings.ollama_host

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not settings.use_ollama:
            return self._academic_dev_response(user_prompt)

        if not settings.ollama_api_key:
            raise RuntimeError(
                "OLLAMA_API_KEY não configurada. Crie um arquivo .env com "
                "OLLAMA_API_KEY=sua_chave_ollama ou configure a variável de ambiente."
            )

        try:
            from ollama import Client

            client = Client(
                host=self.host,
                headers={"Authorization": "Bearer " + settings.ollama_api_key},
            )

            response = client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                options={
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "num_predict": 500,
                },
                stream=False,
            )

            return response["message"]["content"]

        except Exception as exc:
            raise RuntimeError(
                "Falha ao chamar Ollama Cloud. Verifique OLLAMA_API_KEY, "
                "OLLAMA_HOST e OLLAMA_MODEL no arquivo .env."
            ) from exc

    def _academic_dev_response(self, user_prompt: str) -> str:
        text = user_prompt.lower()

        if any(term in text for term in ["dor no peito", "falta de ar", "desmaio", "avc", "fraqueza em um braço"]):
            return (
                "ESCALADA_HUMANA: Foram identificados sinais de alerta clínico. "
                "A orientação segura é encaminhar imediatamente para atendimento humano/emergencial. "
                "Esta resposta não constitui diagnóstico ou prescrição."
            )

        if any(term in text for term in ["ignore", "diagnóstico definitivo", "diagnostico definitivo", "prescreva", "finja que é médico", "finja que e medico"]):
            return (
                "Solicitação bloqueada por guardrail. O sistema não fornece diagnóstico definitivo "
                "e não prescreve medicamentos sem validação médica."
            )

        if any(term in text for term in ["bitcoin", "receita de bolo", "clima", "futebol"]):
            return (
                "A solicitação está fora do escopo do BluaDiagnostics. "
                "O sistema atua apenas em apoio a check-up digital e contexto Care Plus."
            )

        return (
            "Resumo: relato compatível com fluxo de check-up digital. "
            "Pontos de atenção: avaliar histórico, sintomas e sinais vitais. "
            "Próxima ação: considerar teleconsulta conforme evolução. "
            "Aviso: esta orientação não substitui profissional de saúde."
        )
