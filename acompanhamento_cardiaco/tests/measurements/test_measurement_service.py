from datetime import date
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, status

from acompanhamento_cardiaco.measurements import (
    measurement_service as measurement_service_module,
)
from acompanhamento_cardiaco.measurements.measurement_service import (
    MeasurementService,
)

MEDICAO_ID = 1
HTTP_NOT_FOUND = status.HTTP_404_NOT_FOUND
DATA_MEDICAO = date(2026, 5, 30)


class FakeMedicao:
    """Fake do model Medicao usado apenas nos testes unitários."""

    def __init__(self, **kwargs):
        """Inicializa o fake com os mesmos campos recebidos pelo model."""
        self.id_medicao = None

        for chave, valor in kwargs.items():
            setattr(self, chave, valor)


class FakeMeasurementRepository:
    """Fake do repository usado apenas nos testes unitários."""

    def __init__(self, db):
        """Inicializa o repository fake."""
        self.db = db
        self.medicao_existente = None
        self.medicoes = []
        self.medicao_salva = None
        self.medicao_atualizada = None
        self.medicao_removida = None
        self.id_buscado = None

    def listar(self):
        """Simula a listagem de medições."""
        return self.medicoes

    def buscar_por_id(self, id_medicao):
        """Simula a busca de medição por ID."""
        self.id_buscado = id_medicao
        return self.medicao_existente

    def salvar(self, medicao):
        """Simula a persistência de uma medição."""
        medicao.id_medicao = MEDICAO_ID
        self.medicao_salva = medicao
        return medicao

    def atualizar(self, medicao):
        """Simula a atualização de uma medição."""
        self.medicao_atualizada = medicao
        return medicao

    def remover(self, medicao):
        """Simula a remoção de uma medição."""
        self.medicao_removida = medicao


@pytest.fixture
def dados_medicao_valida():
    """Retorna dados válidos para cadastro de medição."""
    return SimpleNamespace(
        pressaoSistolica=120,
        pressaoDiastolica=80,
        frequenciaCardiaca=72,
        nivelOxigenacao=98.5,
        pesoCorporal=75.2,
        faltaAr=False,
        dorPeito=False,
        tontura=False,
        observacoes='Medição sem sintomas.',
        dataMedicao=DATA_MEDICAO,
    )


@pytest.fixture
def medicao_existente():
    """Retorna uma medição existente."""
    return FakeMedicao(
        id_medicao=MEDICAO_ID,
        pressao_sistolica=120,
        pressao_diastolica=80,
        frequencia_cardiaca=72,
        nivel_oxigenacao=98.5,
        peso_corporal=75.2,
        falta_ar=False,
        dor_peito=False,
        tontura=False,
        observacoes='Medição sem sintomas.',
        data_medicao=DATA_MEDICAO,
    )


@pytest.fixture
def repository_fake():
    """Retorna uma instância fake do repository."""
    return FakeMeasurementRepository(db=None)


@pytest.fixture
def configurar_dependencias(monkeypatch, repository_fake):
    """Substitui dependências externas do MeasurementService por fakes."""

    def criar_repository_fake(db):
        repository_fake.db = db
        return repository_fake

    monkeypatch.setattr(
        measurement_service_module,
        'MeasurementRepository',
        criar_repository_fake,
    )

    monkeypatch.setattr(
        measurement_service_module,
        'Medicao',
        FakeMedicao,
        raising=False,
    )

    return repository_fake


def test_deve_cadastrar_medicao_com_sucesso(
    dados_medicao_valida,
    configurar_dependencias,
):
    """Deve cadastrar medição quando os dados forem válidos."""
    repository_fake = configurar_dependencias

    service = MeasurementService(db=None)

    resposta = service.cadastrar_medicao(dados_medicao_valida)

    assert resposta.idMedicao == MEDICAO_ID
    assert resposta.pressaoSistolica == 120
    assert resposta.pressaoDiastolica == 80
    assert resposta.frequenciaCardiaca == 72
    assert resposta.nivelOxigenacao == 98.5
    assert resposta.pesoCorporal == 75.2
    assert resposta.faltaAr is False
    assert resposta.dorPeito is False
    assert resposta.tontura is False
    assert resposta.observacoes == 'Medição sem sintomas.'
    assert resposta.dataMedicao == DATA_MEDICAO
    assert resposta.mensagem == 'Medição criada com sucesso'

    medicao_salva = repository_fake.medicao_salva

    assert medicao_salva is not None
    assert medicao_salva.pressao_sistolica == 120
    assert medicao_salva.pressao_diastolica == 80
    assert medicao_salva.frequencia_cardiaca == 72
    assert medicao_salva.nivel_oxigenacao == 98.5
    assert medicao_salva.peso_corporal == 75.2
    assert medicao_salva.falta_ar is False
    assert medicao_salva.dor_peito is False
    assert medicao_salva.tontura is False
    assert medicao_salva.observacoes == 'Medição sem sintomas.'
    assert medicao_salva.data_medicao == DATA_MEDICAO


def test_deve_listar_medicoes(
    medicao_existente,
    configurar_dependencias,
):
    """Deve listar medições cadastradas."""
    repository_fake = configurar_dependencias
    repository_fake.medicoes = [medicao_existente]

    service = MeasurementService(db=None)

    resposta = service.listar_medicoes()

    assert len(resposta) == 1
    assert resposta[0].idMedicao == MEDICAO_ID
    assert resposta[0].pressaoSistolica == 120
    assert resposta[0].pressaoDiastolica == 80
    assert resposta[0].frequenciaCardiaca == 72
    assert resposta[0].nivelOxigenacao == 98.5
    assert resposta[0].pesoCorporal == 75.2
    assert resposta[0].faltaAr is False
    assert resposta[0].dorPeito is False
    assert resposta[0].tontura is False
    assert resposta[0].observacoes == 'Medição sem sintomas.'
    assert resposta[0].dataMedicao == DATA_MEDICAO


def test_deve_buscar_medicao_por_id(
    medicao_existente,
    configurar_dependencias,
):
    """Deve buscar medição por ID quando ela existir."""
    repository_fake = configurar_dependencias
    repository_fake.medicao_existente = medicao_existente

    service = MeasurementService(db=None)

    resposta = service.buscar_medicao(MEDICAO_ID)

    assert resposta.idMedicao == MEDICAO_ID
    assert resposta.pressaoSistolica == 120
    assert resposta.pressaoDiastolica == 80
    assert resposta.frequenciaCardiaca == 72
    assert resposta.nivelOxigenacao == 98.5
    assert resposta.pesoCorporal == 75.2
    assert resposta.faltaAr is False
    assert resposta.dorPeito is False
    assert resposta.tontura is False
    assert resposta.observacoes == 'Medição sem sintomas.'
    assert resposta.dataMedicao == DATA_MEDICAO
    assert repository_fake.id_buscado == MEDICAO_ID


def test_deve_atualizar_medicao(
    dados_medicao_valida,
    medicao_existente,
    configurar_dependencias,
):
    """Deve atualizar medição quando ela existir."""
    repository_fake = configurar_dependencias
    repository_fake.medicao_existente = medicao_existente
    dados_medicao_valida.pressaoSistolica = 130
    dados_medicao_valida.pressaoDiastolica = 85
    dados_medicao_valida.frequenciaCardiaca = 78
    dados_medicao_valida.nivelOxigenacao = 97.0
    dados_medicao_valida.pesoCorporal = 76.4
    dados_medicao_valida.faltaAr = True
    dados_medicao_valida.dorPeito = True
    dados_medicao_valida.tontura = True
    dados_medicao_valida.observacoes = 'Paciente relatou sintomas.'

    service = MeasurementService(db=None)

    resposta = service.atualizar_medicao(MEDICAO_ID, dados_medicao_valida)

    assert resposta.idMedicao == MEDICAO_ID
    assert resposta.pressaoSistolica == 130
    assert resposta.pressaoDiastolica == 85
    assert resposta.frequenciaCardiaca == 78
    assert resposta.nivelOxigenacao == 97.0
    assert resposta.pesoCorporal == 76.4
    assert resposta.faltaAr is True
    assert resposta.dorPeito is True
    assert resposta.tontura is True
    assert resposta.observacoes == 'Paciente relatou sintomas.'
    assert resposta.dataMedicao == DATA_MEDICAO

    medicao_atualizada = repository_fake.medicao_atualizada

    assert medicao_atualizada is not None
    assert medicao_atualizada.pressao_sistolica == 130
    assert medicao_atualizada.pressao_diastolica == 85
    assert medicao_atualizada.frequencia_cardiaca == 78
    assert medicao_atualizada.nivel_oxigenacao == 97.0
    assert medicao_atualizada.peso_corporal == 76.4
    assert medicao_atualizada.falta_ar is True
    assert medicao_atualizada.dor_peito is True
    assert medicao_atualizada.tontura is True
    assert medicao_atualizada.observacoes == 'Paciente relatou sintomas.'
    assert medicao_atualizada.data_medicao == DATA_MEDICAO


def test_deve_remover_medicao(
    medicao_existente,
    configurar_dependencias,
):
    """Deve remover medição quando ela existir."""
    repository_fake = configurar_dependencias
    repository_fake.medicao_existente = medicao_existente

    service = MeasurementService(db=None)

    resposta = service.remover_medicao(MEDICAO_ID)

    assert resposta is None
    assert repository_fake.medicao_removida == medicao_existente
    assert repository_fake.id_buscado == MEDICAO_ID


def test_deve_retornar_erro_404_quando_medicao_nao_existir_ao_buscar(
    configurar_dependencias,
):
    """Deve retornar erro 404 ao buscar medição inexistente."""
    service = MeasurementService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.buscar_medicao(MEDICAO_ID)

    assert erro.value.status_code == HTTP_NOT_FOUND
    assert erro.value.detail['codigo'] == HTTP_NOT_FOUND
    assert erro.value.detail['mensagem'] == 'Medição não encontrada'
    assert erro.value.detail['detalhes']['campo'] == 'id_medicao'


def test_deve_retornar_erro_404_quando_medicao_nao_existir_ao_atualizar(
    dados_medicao_valida,
    configurar_dependencias,
):
    """Deve retornar erro 404 ao atualizar medição inexistente."""
    service = MeasurementService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.atualizar_medicao(MEDICAO_ID, dados_medicao_valida)

    assert erro.value.status_code == HTTP_NOT_FOUND
    assert erro.value.detail['codigo'] == HTTP_NOT_FOUND
    assert erro.value.detail['mensagem'] == 'Medição não encontrada'
    assert erro.value.detail['detalhes']['campo'] == 'id_medicao'


def test_deve_retornar_erro_404_quando_medicao_nao_existir_ao_remover(
    configurar_dependencias,
):
    """Deve retornar erro 404 ao remover medição inexistente."""
    service = MeasurementService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.remover_medicao(MEDICAO_ID)

    assert erro.value.status_code == HTTP_NOT_FOUND
    assert erro.value.detail['codigo'] == HTTP_NOT_FOUND
    assert erro.value.detail['mensagem'] == 'Medição não encontrada'
    assert erro.value.detail['detalhes']['campo'] == 'id_medicao'
