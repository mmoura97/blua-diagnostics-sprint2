from __future__ import annotations

from src.config import settings


class OllamaLLMClient:
    """
    Cliente oficial de LLM da Sprint 2.

    Execução oficial:
    - Ollama Cloud;
    - autenticação via OLLAMA_API_KEY no arquivo .env;
    - host padrão: https://ollama.com.

    Caso a chave não esteja configurada ou o serviço não responda,
    a execução falha explicitamente para evitar resultados simulados
    mascarados como inferência real.
    """

    def __init__(self, model: str | None = None, host: str | None = None):
        self.model = model or settings.ollama_model
        self.host = host or settings.ollama_host

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not settings.ollama_api_key:
            raise RuntimeError(
                "OLLAMA_API_KEY não configurada. Crie um arquivo .env com "
                "OLLAMA_API_KEY=sua_chave_ollama."
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
