# Relatório Técnico Final — BluaDiagnostics Sprint 2/Sprint 4

## 1. Visão geral

Esta sprint evolui a PoC da Sprint 1 para um sistema com RAG funcional, multi-agente com LangGraph, function calling, guardrails técnicos, evals automatizados e interface Streamlit.

A execução principal foi configurada com **Ollama Cloud via `.env`**, mantendo o padrão usado na PoC anterior e evitando exposição de chaves no repositório.

---

## 2. Arquitetura final

Componentes principais:

- Interface Streamlit;
- Supervisor LangGraph;
- Agente de Triagem;
- Agente de Prescrição;
- Agente de Escalada Humana;
- RAG com Chroma;
- Tools clínicas simuladas;
- Guardrails técnicos;
- Suite de evals.

---

## 3. Decisões técnicas

| Decisão | Justificativa |
|---|---|
| Ollama Cloud via `.env` | Facilita execução acadêmica e evita instalação local pesada |
| Chroma | Vector store local simples para PoC |
| Sentence-transformers | Embeddings locais sem API paga |
| Streamlit | Interface rápida e demonstrável em vídeo |
| LangGraph | Orquestração explícita de múltiplos agentes |
| Tools mockadas | Segurança e ausência de dados reais |

---

## 4. RAG

O pipeline realiza:

1. leitura dos arquivos em `data/knowledge_base/`;
2. divisão em chunks;
3. geração de embeddings;
4. persistência no Chroma;
5. recuperação de documentos relevantes por pergunta.

Os documentos recuperados são registrados nos resultados dos evals e exibidos na interface.

---

## 5. Multi-agente

O grafo possui:

- supervisor;
- agente de triagem;
- agente de prescrição;
- agente de escalada humana.

O roteamento é baseado em intenção, escopo e red flags.

---

## 6. Guardrails

Guardrails implementados:

- bloqueio de jailbreak;
- rejeição de fora de escopo;
- detecção de red flags cardíacas;
- detecção de red flags respiratórias;
- detecção de red flags neurológicas;
- proibição de diagnóstico definitivo;
- proibição de prescrição sem médico.

---

## 7. Resultados dos evals

Arquivos gerados:

```text
evals/sprint2_results.json
evals/sprint2_metrics.json
```

Métricas avaliadas:

- acurácia por categoria;
- taxa de escalada correta;
- tempo médio de resposta;
- custo estimado;
- documentos recuperados;
- tools chamadas;
- trajetória dos agentes.

---

## 8. Iterações

| Iteração | Mudança | Motivo |
|---|---|---|
| v1 | PoC simples | Validar fluxo conversacional |
| v2 | RAG | Melhorar contextualização |
| v3 | LangGraph | Separar responsabilidades |
| v4 | Guardrails | Aumentar segurança clínica |
| v5 | Evals | Medir qualidade |
| v6 | Streamlit | Facilitar demonstração visual |
| v7 | Ollama Cloud via `.env` | Melhorar reprodutibilidade para correção |

---

## 9. Limitações

- Dados clínicos são simulados;
- Tools não integram sistemas reais;
- RAG usa base pequena;
- Sem validação médica real;
- Sem produção com autenticação/observabilidade corporativa.

---

## 10. Roadmap

- RAG com re-ranking;
- LangSmith/LangFuse;
- integração real com wearable;
- testes unitários;
- autenticação;
- logs estruturados;
- pipeline CI/CD.
