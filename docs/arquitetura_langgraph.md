# Arquitetura LangGraph — BluaDiagnostics

```mermaid
flowchart TD
    A[Interface Streamlit] --> B[Supervisor LangGraph]
    B --> C{Intent + Guardrails}
    C -->|checkup| D[Agente de Triagem]
    C -->|prescricao| E[Agente de Prescrição]
    C -->|red_flag| F[Agente de Escalada Humana]

    D --> G[RAG Retriever]
    E --> G
    G --> H[Chroma Vector Store]
    H --> I[Knowledge Base]

    D --> J[Tools]
    E --> J
    F --> J

    J --> K[Histórico Paciente]
    J --> L[Interações Medicamentosas]
    J --> M[Agendamento]
    J --> N[Wearables]

    D --> O[Ollama Cloud LLM]
    E --> O
    F --> O

    O --> P[Resposta Final + Trajetória]
```

## Estado compartilhado

O estado do grafo mantém:

- mensagem do usuário;
- paciente atual;
- histórico da conversa;
- documentos recuperados;
- tools chamadas;
- agente acionado;
- resposta final;
- decisão de escalada.

## Roteamento

- sintomas gerais → triagem;
- medicamentos/prescrição → prescrição;
- dor no peito/falta de ar/desmaio/sintomas neurológicos → escalada humana;
- jailbreak/out_of_scope → bloqueio por guardrail.
