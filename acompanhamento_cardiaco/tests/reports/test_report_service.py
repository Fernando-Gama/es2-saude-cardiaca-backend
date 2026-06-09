from datetime import date
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, status

from acompanhamento_cardiaco.reports import report_service as report_service_module
from acompanhamento_cardiaco.reports.report_service import ReportService

ALERTA_SEM_MEDICOES = 'Nenhuma medição encontrada para o período informado.'
USUARIO_ID = 1


class FakeMeasurementRepository:
    """Fake do repository usado apenas nos testes unitários de relatório."""

    def __init__(self, db):
        """Inicializa o repository fake."""
        self.db = db
        self.medicoes = []
        self.id_usuario_buscado = None
        self.data_inicial_buscada = None
        self.data_final_buscada = None

    def listar_por_usuario_e_periodo(
        self,
        id_usuario,
        data_inicial=None,
        data_final=None,
    ):
        """Simula a listagem de medições por período."""
        self.id_usuario_buscado = id_usuario
        self.data_inicial_buscada = data_inicial
        self.data_final_buscada = data_final
        return self.medicoes


@pytest.fixture
def repository_fake():
    """Retorna uma instância fake do repository."""
    return FakeMeasurementRepository(db=None)


@pytest.fixture
def configurar_dependencias(monkeypatch, repository_fake):
    """Substitui dependências externas do ReportService por fakes."""

    def criar_repository_fake(db):
        repository_fake.db = db
        return repository_fake

    monkeypatch.setattr(
        report_service_module,
        'MeasurementRepository',
        criar_repository_fake,
    )

    return repository_fake


def criar_medicao(data_medicao, **overrides):
    """Cria uma medição fake para os testes."""
    dados = {
        'data_medicao': data_medicao,
        'pressao_sistolica': 120,
        'pressao_diastolica': 80,
        'frequencia_cardiaca': 72,
        'nivel_oxigenacao': 98.0,
        'peso_corporal': 75.0,
        'falta_ar': False,
        'dor_peito': False,
        'tontura': False,
    }
    dados.update(overrides)
    return SimpleNamespace(**dados)


def test_deve_gerar_relatorio_com_medias_historico_e_alertas(
    configurar_dependencias,
):
    """Deve gerar relatório consolidado com médias, histórico e alertas."""
    repository_fake = configurar_dependencias
    repository_fake.medicoes = [
        criar_medicao(
            date(2026, 6, 2),
            pressao_sistolica=150,
            pressao_diastolica=95,
            frequencia_cardiaca=105,
            nivel_oxigenacao=94.0,
            peso_corporal=76.0,
            falta_ar=True,
            dor_peito=True,
        ),
        criar_medicao(
            date(2026, 6, 1),
            pressao_sistolica=120,
            pressao_diastolica=80,
            frequencia_cardiaca=75,
            nivel_oxigenacao=98.0,
            peso_corporal=74.0,
            tontura=True,
        ),
    ]

    service = ReportService(db=None)

    resposta = service.gerar_relatorio_saude_cardiaca(
        id_usuario=USUARIO_ID,
        data_inicial=date(2026, 6, 1),
        data_final=date(2026, 6, 30),
    )

    assert resposta.periodo.dataInicial == date(2026, 6, 1)
    assert resposta.periodo.dataFinal == date(2026, 6, 30)
    assert resposta.resumo.totalMedicoes == 2
    assert resposta.resumo.mediaPressaoSistolica == 135
    assert resposta.resumo.mediaPressaoDiastolica == 87.5
    assert resposta.resumo.mediaFrequenciaCardiaca == 90
    assert resposta.resumo.mediaNivelOxigenacao == 96
    assert resposta.resumo.mediaPesoCorporal == 75
    assert resposta.sintomas.registrosFaltaAr == 1
    assert resposta.sintomas.registrosDorPeito == 1
    assert resposta.sintomas.registrosTontura == 1
    assert resposta.historico[0].dataMedicao == date(2026, 6, 1)
    assert resposta.historico[1].dataMedicao == date(2026, 6, 2)
    assert len(resposta.alertas) == 6
    assert repository_fake.id_usuario_buscado == USUARIO_ID
    assert repository_fake.data_inicial_buscada == date(2026, 6, 1)
    assert repository_fake.data_final_buscada == date(2026, 6, 30)


def test_deve_gerar_relatorio_vazio_quando_nao_houver_medicoes(
    configurar_dependencias,
):
    """Deve gerar relatório vazio quando não houver medições no período."""
    service = ReportService(db=None)

    resposta = service.gerar_relatorio_saude_cardiaca(id_usuario=USUARIO_ID)

    assert resposta.resumo.totalMedicoes == 0
    assert resposta.resumo.mediaPressaoSistolica is None
    assert resposta.sintomas.registrosFaltaAr == 0
    assert resposta.historico == []
    assert resposta.alertas == [ALERTA_SEM_MEDICOES]


def test_deve_retornar_erro_400_quando_periodo_for_invalido(
    configurar_dependencias,
):
    """Deve retornar erro 400 quando data inicial for maior que data final."""
    service = ReportService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.gerar_relatorio_saude_cardiaca(
            id_usuario=USUARIO_ID,
            data_inicial=date(2026, 6, 30),
            data_final=date(2026, 6, 1),
        )

    assert erro.value.status_code == status.HTTP_400_BAD_REQUEST
    assert erro.value.detail['codigo'] == status.HTTP_400_BAD_REQUEST
    assert erro.value.detail['mensagem'] == 'Período inválido'
