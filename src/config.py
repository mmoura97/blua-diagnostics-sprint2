import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    # Execução principal da Sprint 2:
    # Ollama Cloud com API key via .env
    ollama_host: str = os.getenv("OLLAMA_HOST", "https://ollama.com")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
    ollama_api_key: str | None = os.getenv("OLLAMA_API_KEY")
    use_ollama: bool = os.getenv("USE_OLLAMA", "true").lower() == "true"

    # RAG
    chroma_dir: str = os.getenv("CHROMA_DIR", "chroma_db")


settings = Settings()
