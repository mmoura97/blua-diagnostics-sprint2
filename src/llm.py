from __future__ import annotations

from src.agents.llm_client import OllamaLLMClient


class LLMClient:
    """
    Wrapper oficial do projeto.

    A implementação utiliza Ollama Cloud via .env.
    Mantém os métodos esperados pelos agentes:
    - chat()
    - generate()
    - invoke()
    """

    def __init__(self):
        self.client = OllamaLLMClient()

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        rag_context: str | list | None = None,
    ) -> str:
        if rag_context:
            if isinstance(rag_context, list):
                context_text = "\n".join(str(item) for item in rag_context)
            else:
                context_text = str(rag_context)

            final_prompt = (
                f"Contexto recuperado via RAG:\n{context_text}\n\n"
                f"Mensagem do usuário:\n{user_prompt}"
            )
        else:
            final_prompt = user_prompt

        return self.client.generate(
            system_prompt=system_prompt,
            user_prompt=final_prompt,
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return self.client.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

    def invoke(self, prompt: str) -> str:
        return self.generate(
            system_prompt="Você é o BluaDiagnostics, assistente clínico seguro da Care Plus.",
            user_prompt=prompt,
        )


llm_client = LLMClient()