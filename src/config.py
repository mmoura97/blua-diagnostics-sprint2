import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    # Execução oficial da Sprint 2:
    # Ollama Cloud com API key via .env
    ollama_host: str = os.getenv("OLLAMA_HOST", "https://ollama.com")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
    ollama_api_key: str | None = os.getenv("OLLAMA_API_KEY")

    # RAG
    chroma_dir: str = os.getenv("CHROMA_DIR", "chroma_db")


settings = Settings()
