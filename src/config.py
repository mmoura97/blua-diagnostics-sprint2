import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    # Ollama Cloud
    ollama_host: str = os.getenv("OLLAMA_HOST", "https://ollama.com")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
    ollama_api_key: str | None = os.getenv("OLLAMA_API_KEY")

    # RAG
    chroma_dir: str = os.getenv("CHROMA_DIR", "chroma_db")
    knowledge_base_dir: str = os.getenv(
        "KNOWLEDGE_BASE_DIR",
        "data/knowledge_base"
    )


settings = Settings()