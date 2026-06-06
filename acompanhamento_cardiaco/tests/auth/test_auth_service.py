from types import SimpleNamespace

import pytest
from fastapi import HTTPException, status

from acompanhamento_cardiaco.auth import auth_service as auth_service_module
from acompanhamento_cardiaco.auth.auth_service import AuthService

USUARIO_ID = 1


class FakeAuthRepository:
    """Fake do repository usado apenas nos testes unitários de autenticação."""

    def __init__(self, db):
        """Inicializa o repository fake."""
        self.db = db
        self.usuario_existente = None
        self.email_buscado = None

    def buscar_usuario_por_email(self, email):
        """Simula a busca de usuário por e-mail."""
        self.email_buscado = email
        return self.usuario_existente


@pytest.fixture
def repository_fake():
    """Retorna uma instância fake do repository."""
    return FakeAuthRepository(db=None)


@pytest.fixture
def configurar_dependencias(monkeypatch, repository_fake):
    """Substitui dependências externas do AuthService por fakes."""

    def criar_repository_fake(db):
        repository_fake.db = db
        return repository_fake

    monkeypatch.setattr(
        auth_service_module,
        'AuthRepository',
        criar_repository_fake,
    )

    monkeypatch.setattr(
        auth_service_module,
        'verificar_senha',
        lambda senha, senha_hash: senha == 'Senha@123'
        and senha_hash == 'senha_hash_fake',
    )

    monkeypatch.setattr(
        auth_service_module,
        'create_access_token',
        lambda subject: (f'access_token_usuario_{subject}', 1800),
    )

    monkeypatch.setattr(
        auth_service_module,
        'create_refresh_token',
        lambda subject: f'refresh_token_usuario_{subject}',
    )

    return repository_fake


def test_deve_fazer_login_com_sucesso(configurar_dependencias):
    """Deve retornar tokens quando as credenciais forem válidas."""
    repository_fake = configurar_dependencias
    repository_fake.usuario_existente = SimpleNamespace(
        id_usuario=USUARIO_ID,
        email='fernando@email.com',
        senha_hash='senha_hash_fake',
    )

    service = AuthService(db=None)

    resposta = service.login('fernando@email.com', 'Senha@123')

    assert resposta.access_token == 'access_token_usuario_1'
    assert resposta.refresh_token == 'refresh_token_usuario_1'
    assert resposta.token_type == 'bearer'
    assert resposta.expires_in == 1800
    assert repository_fake.email_buscado == 'fernando@email.com'


def test_deve_retornar_erro_401_quando_credenciais_fore_invalidas(
    configurar_dependencias,
):
    """Deve retornar erro 401 quando e-mail ou senha forem inválidos."""
    service = AuthService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.login('fernando@email.com', 'Senha@123')

    assert erro.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert erro.value.detail['codigo'] == status.HTTP_401_UNAUTHORIZED
    assert erro.value.detail['mensagem'] == 'Credenciais inválidas'


def test_deve_renovar_tokens_com_refresh_token_valido(
    configurar_dependencias,
    monkeypatch,
):
    """Deve retornar novos tokens quando o refresh token for válido."""
    monkeypatch.setattr(
        auth_service_module,
        'decode_token',
        lambda token: {'sub': str(USUARIO_ID), 'type': 'refresh'},
    )

    service = AuthService(db=None)

    resposta = service.refresh('refresh_token_valido')

    assert resposta.access_token == 'access_token_usuario_1'
    assert resposta.refresh_token == 'refresh_token_usuario_1'
    assert resposta.expires_in == 1800


def test_deve_retornar_erro_401_quando_refresh_token_for_invalido(
    configurar_dependencias,
    monkeypatch,
):
    """Deve retornar erro 401 quando o refresh token for inválido."""

    def levantar_erro(token):
        raise ValueError('Token inválido')

    monkeypatch.setattr(auth_service_module, 'decode_token', levantar_erro)

    service = AuthService(db=None)

    with pytest.raises(HTTPException) as erro:
        service.refresh('refresh_token_invalido')

    assert erro.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert erro.value.detail['codigo'] == status.HTTP_401_UNAUTHORIZED
    assert erro.value.detail['mensagem'] == 'Refresh token inválido'
