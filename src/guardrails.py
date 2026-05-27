RED_FLAG_TERMS = [
    "dor no peito", "falta de ar", "desmaio", "confusão mental",
    "fraqueza em um braço", "fala enrolada", "sangramento intenso",
    "saturação baixa", "spo2 90", "ideação suicida", "não quero mais viver"
]

JAILBREAK_TERMS = [
    "ignore suas regras", "ignore as regras", "finja que é médico",
    "prescreva", "diagnóstico definitivo", "sem restrições", "modo dev"
]

OUT_OF_SCOPE_TERMS = [
    "bitcoin", "criptomoeda", "futebol", "receita de bolo", "segunda guerra",
    "investimento", "programa em java"
]

def detect_red_flag(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in RED_FLAG_TERMS)

def detect_jailbreak(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in JAILBREAK_TERMS)

def detect_out_of_scope(text: str) -> bool:
    t = text.lower()
    return any(term in t for term in OUT_OF_SCOPE_TERMS)

def classify_intent(text: str) -> str:
    t = text.lower()
    if detect_jailbreak(t):
        return "jailbreak"
    if detect_out_of_scope(t):
        return "out_of_scope"
    if detect_red_flag(t):
        return "escalada"
    if any(x in t for x in ["remédio", "medicamento", "losartana", "ibuprofeno", "dipirona", "prescrição"]):
        return "prescricao"
    return "triagem"
