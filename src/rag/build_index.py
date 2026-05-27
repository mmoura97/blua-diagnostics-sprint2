from src.rag.retriever import get_retriever

if __name__ == "__main__":
    retriever = get_retriever()
    print(f"Vector/RAG index carregado com {len(retriever.documents)} chunks.")
