from __future__ import annotations

from src.agents.llm_client import OllamaLLMClient


class LLMClient:
    """
    Wrapper legado mantido apenas para compatibilidade interna.

    A implementação oficial usa Ollama Cloud via .env.
    """

    def __init__(self):
        self.client = OllamaLLMClient()

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return self.client.generate(system_prompt=system_prompt, user_prompt=user_prompt)
