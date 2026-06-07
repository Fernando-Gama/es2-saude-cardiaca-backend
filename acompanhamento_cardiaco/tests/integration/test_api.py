from collections.abc import AsyncGenerator, Generator

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from acompanhamento_cardiaco.database import Base, get_db
from acompanhamento_cardiaco.main import app


@pytest.fixture
def anyio_backend() -> str:
    """Define o backend assíncrono usado pelos testes de integração."""
    return 'asyncio'


@pytest.fixture
def configurar_banco_teste() -> Generator[None, None, None]:
    """Configura um banco SQLite isolado para os testes da API."""
    engine = create_engine(
        'sqlite://',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)

    async def override_get_db() -> AsyncGenerator:
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def usuario_payload() -> dict[str, str]:
    """Retorna payload válido para criação de usuário."""
    return {
        'nome': 'Fernando',
        'sobrenome': 'Gama',
        'email': 'fernando@email.com',
        'celular': '21999999999',
        'senha': 'Senha@123',
        'confirmarSenha': 'Senha@123',
        'dataNascimento': '2000-01-01',
        'sexo': 'M',
        'paisResidencia': 'Brasil',
        'naturalidadeUF': 'RJ',
    }


@pytest.fixture
def outro_usuario_payload() -> dict[str, str]:
    """Retorna payload válido para criação de outro usuário."""
    return {
        'nome': 'Maria',
        'sobrenome': 'Silva',
        'email': 'maria@email.com',
        'celular': '21988888888',
        'senha': 'Senha@123',
        'confirmarSenha': 'Senha@123',
        'dataNascimento': '1998-02-02',
        'sexo': 'F',
        'paisResidencia': 'Brasil',
        'naturalidadeUF': 'SP',
    }


@pytest.fixture
def medicao_payload() -> dict[str, str | int | float | bool]:
    """Retorna payload válido para criação de medição."""
    return {
        'pressaoSistolica': 150,
        'pressaoDiastolica': 95,
        'frequenciaCardiaca': 105,
        'nivelOxigenacao': 94.0,
        'pesoCorporal': 76.0,
        'faltaAr': True,
        'dorPeito': True,
        'tontura': False,
        'observacoes': 'Paciente relatou sintomas.',
        'dataMedicao': '2026-06-02',
    }


@pytest.fixture
def segunda_medicao_payload() -> dict[str, str | int | float | bool]:
    """Retorna segundo payload válido para criação de medição."""
    return {
        'pressaoSistolica': 120,
        'pressaoDiastolica': 80,
        'frequenciaCardiaca': 75,
        'nivelOxigenacao': 98.0,
        'pesoCorporal': 74.0,
        'faltaAr': False,
        'dorPeito': False,
        'tontura': True,
        'observacoes': 'Medição de controle.',
        'dataMedicao': '2026-06-01',
    }


async def criar_usuario_e_obter_token(client, payload):
    """Cria um usuário pela API e retorna o token de acesso."""
    resposta_cadastro = await client.post('/v1/users', json=payload)
    assert resposta_cadastro.status_code == 201

    resposta_login = await client.post(
        '/v1/auth/login',
        json={
            'email': payload['email'],
            'senha': payload['senha'],
        },
    )
    assert resposta_login.status_code == 200

    return resposta_login.json()['access_token']


@pytest.mark.anyio
async def test_deve_criar_usuario_fazer_login_e_renovar_token(
    configurar_banco_teste,
    usuario_payload,
):
    """Deve validar o fluxo de cadastro, login e refresh token."""
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        resposta_cadastro = await client.post('/v1/users', json=usuario_payload)

        assert resposta_cadastro.status_code == 201
        assert resposta_cadastro.json()['email'] == 'fernando@email.com'

        resposta_login = await client.post(
            '/v1/auth/login',
            json={
                'email': 'fernando@email.com',
                'senha': 'Senha@123',
            },
        )

        assert resposta_login.status_code == 200
        assert resposta_login.json()['access_token']
        assert resposta_login.json()['refresh_token']
        assert resposta_login.json()['token_type'] == 'bearer'

        resposta_refresh = await client.post(
            '/v1/auth/refresh',
            json={'refresh_token': resposta_login.json()['refresh_token']},
        )

        assert resposta_refresh.status_code == 200
        assert resposta_refresh.json()['access_token']
        assert resposta_refresh.json()['refresh_token']


@pytest.mark.anyio
async def test_deve_exigir_token_para_criar_medicao(
    configurar_banco_teste,
    medicao_payload,
):
    """Deve negar criação de medição sem Bearer token."""
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        resposta = await client.post('/v1/measurements', json=medicao_payload)

        assert resposta.status_code == 401
        assert (
            resposta.json()['detail']['mensagem']
            == 'Token inválido ou expirado'
        )


@pytest.mark.anyio
async def test_deve_criar_listar_atualizar_e_remover_medicao_com_token(
    configurar_banco_teste,
    usuario_payload,
    medicao_payload,
):
    """Deve validar o CRUD de medições com usuário autenticado."""
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        token = await criar_usuario_e_obter_token(client, usuario_payload)
        headers = {'Authorization': f'Bearer {token}'}

        resposta_criacao = await client.post(
            '/v1/measurements',
            json=medicao_payload,
            headers=headers,
        )

        assert resposta_criacao.status_code == 201
        assert resposta_criacao.json()['pressaoSistolica'] == 150

        id_medicao = resposta_criacao.json()['idMedicao']

        resposta_listagem = await client.get('/v1/measurements', headers=headers)

        assert resposta_listagem.status_code == 200
        assert len(resposta_listagem.json()) == 1

        payload_atualizacao = medicao_payload | {
            'pressaoSistolica': 130,
            'pressaoDiastolica': 85,
            'frequenciaCardiaca': 80,
        }
        resposta_atualizacao = await client.put(
            f'/v1/measurements/{id_medicao}',
            json=payload_atualizacao,
            headers=headers,
        )

        assert resposta_atualizacao.status_code == 200
        assert resposta_atualizacao.json()['pressaoSistolica'] == 130

        resposta_remocao = await client.delete(
            f'/v1/measurements/{id_medicao}',
            headers=headers,
        )

        assert resposta_remocao.status_code == 204

        resposta_busca = await client.get(
            f'/v1/measurements/{id_medicao}',
            headers=headers,
        )

        assert resposta_busca.status_code == 404


@pytest.mark.anyio
async def test_deve_impedir_acesso_a_medicao_de_outro_usuario(
    configurar_banco_teste,
    usuario_payload,
    outro_usuario_payload,
    medicao_payload,
):
    """Deve impedir que usuário acesse medição criada por outro usuário."""
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        token_usuario = await criar_usuario_e_obter_token(client, usuario_payload)
        token_outro_usuario = await criar_usuario_e_obter_token(
            client,
            outro_usuario_payload,
        )

        resposta_criacao = await client.post(
            '/v1/measurements',
            json=medicao_payload,
            headers={'Authorization': f'Bearer {token_usuario}'},
        )
        id_medicao = resposta_criacao.json()['idMedicao']

        resposta_busca = await client.get(
            f'/v1/measurements/{id_medicao}',
            headers={'Authorization': f'Bearer {token_outro_usuario}'},
        )

        assert resposta_busca.status_code == 404


@pytest.mark.anyio
async def test_deve_gerar_relatorio_apenas_com_medicoes_do_usuario(
    configurar_banco_teste,
    usuario_payload,
    outro_usuario_payload,
    medicao_payload,
    segunda_medicao_payload,
):
    """Deve gerar relatório usando apenas medições do usuário autenticado."""
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        token_usuario = await criar_usuario_e_obter_token(client, usuario_payload)
        token_outro_usuario = await criar_usuario_e_obter_token(
            client,
            outro_usuario_payload,
        )
        headers_usuario = {'Authorization': f'Bearer {token_usuario}'}
        headers_outro_usuario = {'Authorization': f'Bearer {token_outro_usuario}'}

        await client.post(
            '/v1/measurements',
            json=medicao_payload,
            headers=headers_usuario,
        )
        await client.post(
            '/v1/measurements',
            json=segunda_medicao_payload,
            headers=headers_usuario,
        )
        await client.post(
            '/v1/measurements',
            json=medicao_payload | {'pressaoSistolica': 180},
            headers=headers_outro_usuario,
        )

        resposta = await client.get(
            '/v1/reports/heart-health?dataInicial=2026-06-01&dataFinal=2026-06-30',
            headers=headers_usuario,
        )

        assert resposta.status_code == 200
        assert resposta.json()['resumo']['totalMedicoes'] == 2
        assert resposta.json()['resumo']['mediaPressaoSistolica'] == 135
        assert resposta.json()['resumo']['mediaPressaoDiastolica'] == 87.5
        assert resposta.json()['sintomas']['registrosDorPeito'] == 1
        assert resposta.json()['historico'][0]['dataMedicao'] == '2026-06-01'


@pytest.mark.anyio
async def test_deve_retornar_400_quando_periodo_do_relatorio_for_invalido(
    configurar_banco_teste,
    usuario_payload,
):
    """Deve retornar erro 400 quando período do relatório for inválido."""
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        token = await criar_usuario_e_obter_token(client, usuario_payload)

        resposta = await client.get(
            '/v1/reports/heart-health?dataInicial=2026-06-30&dataFinal=2026-06-01',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert resposta.status_code == 400
        assert resposta.json()['detail']['mensagem'] == 'Período inválido'
