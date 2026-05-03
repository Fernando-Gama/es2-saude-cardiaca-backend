from datetime import date
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, status

import acompanhamento_cardiaco.users.user_service as user_service_module
from acompanhamento_cardiaco.users.user_service import UserService

USUARIO_ID = 1
HTTP_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
HTTP_CONFLICT = status.HTTP_409_CONFLICT
DATA_NASCIMENTO = date(2000, 1, 1)


class FakeUser:
    """Fake do model User usado apenas nos testes unitários."""

    def __init__(self, **kwargs):
        """Inicializa o fake com os mesmos campos recebidos pelo model."""
        self.id_usuario = None

        for chave, valor in kwargs.items():
            setattr(self, chave, valor)


class FakeUserRepository:
    """Fake do repository usado apenas nos testes unitários."""

    def __init__(self, db):
        """Inicializa o repository fake."""
        self.db = db
        self.usuario_existente = None
        self.usuario_salvo = None
        self.email_buscado = None

    def buscar_por_email(self, email):
        """Simula a busca de usuário por e-mail."""
        self.email_buscado = email
        return self.usuario_existente

    def salvar(self, usuario):
        """Simula a persistência de um usuário."""
        usuario.id_usuario = USUARIO_ID
        self.usuario_salvo = usuario
        return usuario


@pytest.fixture
def dados_usuario_valido():
    """Retorna dados válidos para cadastro de usuário."""
    return SimpleNamespace(
        nome='Fernando',
        sobrenome='Gama',
        email='fernando@email.com',
        celular='21999999999',
        senha='Senha@123',
        confirmarSenha='Senha@123',
        dataNascimento=DATA_NASCIMENTO,
        sexo=SimpleNamespace(value='M'),
        paisResidencia='Brasil',
        naturalidadeUF='RJ',
    )


@pytest.fixture
def repository_fake():
    """Retorna uma instância fake do repository."""
    return FakeUserRepository(db=None)


@pytest.fixture
def configurar_dependencias(monkeypatch, repository_fake):
    """Substitui dependências externas do UserService por fakes."""

    def criar_repository_fake(db):
        repository_fake.db = db
        return repository_fake

    monkeypatch.setattr(
        user_service_module,
        'UserRepository',
        criar_repository_fake,
    )

    monkeypatch.setattr(
        user_service_module,
        'User',
        FakeUser,
        raising=False,
    )

    monkeypatch.setattr(
        user_service_module,
        'gerar_hash_senha',
        lambda senha: 'senha_hash_fake',
    )

    return repository_fake


def test_deve_cadastrar_usuario_com_sucesso(
    dados_usuario_valido,
    configurar_dependencias,
):
    """Deve cadastrar usuário quando os dados forem válidos."""
    repository_fake = configurar_dependencias

    service = UserService(db=None)

    resposta = service.cadastrar_usuario(dados_usuario_valido)

    assert resposta.idUsuario == USUARIO_ID
    assert resposta.nome == 'Fernando'
    assert resposta.sobrenome == 'Gama'
    assert resposta.email == 'fernando@email.com'
    assert resposta.celular == '21999999999'
    assert resposta.dataNascimento == DATA_NASCIMENTO
    assert resposta.sexo.value == 'M'
    assert resposta.paisResidencia == 'Brasil'
    assert resposta.naturalidadeUF == 'RJ'
    assert resposta.mensagem == 'Conta criada com sucesso'

    usuario_salvo = repository_fake.usuario_salvo

    assert usuario_salvo is not None
    assert usuario_salvo.nome == 'Fernando'
    assert usuario_salvo.email == 'fernando@email.com'
    assert usuario_salvo.sexo == 'M'
    assert usuario_salvo.senha_hash == 'senha_hash_fake'


def test_deve_retornar_erro_400_quando_confirmacao_senha_for_diferente(
    dados_usuario_valido,
    configurar_dependencias,
):
    """Deve retornar erro 400 quando senha e confirmação forem diferentes."""
    dados_usuario_valido.confirmarSenha = 'OutraSenha@123'

    service = UserService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.cadastrar_usuario(dados_usuario_valido)

    assert erro.value.status_code == HTTP_BAD_REQUEST
    assert erro.value.detail['codigo'] == HTTP_BAD_REQUEST
    assert erro.value.detail['detalhes']['campo'] == 'confirmarSenha'


def test_deve_retornar_erro_409_quando_email_ja_estiver_cadastrado(
    dados_usuario_valido,
    configurar_dependencias,
):
    """Deve retornar erro 409 quando o e-mail já existir."""
    repository_fake = configurar_dependencias

    repository_fake.usuario_existente = SimpleNamespace(
        id_usuario=USUARIO_ID,
        email='fernando@email.com',
    )

    service = UserService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.cadastrar_usuario(dados_usuario_valido)

    assert erro.value.status_code == HTTP_CONFLICT
    assert erro.value.detail['codigo'] == HTTP_CONFLICT
    assert erro.value.detail['mensagem'] == 'E-mail já cadastrado'
    assert erro.value.detail['detalhes']['campo'] == 'email'


def test_deve_buscar_email_antes_de_salvar_usuario(
    dados_usuario_valido,
    configurar_dependencias,
):
    """Deve consultar o e-mail antes de salvar o usuário."""
    repository_fake = configurar_dependencias

    service = UserService(db=None)

    service.cadastrar_usuario(dados_usuario_valido)

    assert repository_fake.email_buscado == 'fernando@email.com'
