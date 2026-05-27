from src.tools.clinical_tools import consultar_historico_paciente, verificar_interacoes_medicamentosas

def test_consultar_historico_paciente():
    result = consultar_historico_paciente("MARIA-34")
    assert result["status"] == "ok"
    assert result["patient"]["nome"] == "Maria"

def test_interacao_losartana_ibuprofeno():
    result = verificar_interacoes_medicamentosas(["Losartana 50mg", "ibuprofeno"])
    assert result["status"] == "ok"
    assert any(a["risco"] == "moderado" for a in result["alerts"])
