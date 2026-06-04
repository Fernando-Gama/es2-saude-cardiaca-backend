from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.database import get_db
from acompanhamento_cardiaco.measurements.measurement_schemas import (
    CreateMeasurementResponse,
    MeasurementRequest,
    MeasurementResponse,
)
from acompanhamento_cardiaco.measurements.measurement_service import (
    MeasurementService,
)
from acompanhamento_cardiaco.users.user_schemas import ErrorResponse

router = APIRouter(
    prefix='/measurements',
    tags=['Medições'],
)


@router.post(
    '',
    response_model=CreateMeasurementResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Criar medição',
    description='Cadastra uma nova medição de saúde cardíaca.',
    responses={
        500: {
            'model': ErrorResponse,
            'description': 'Erro interno no servidor.',
        },
    },
)
def cadastrar_medicao(
    dados_medicao: MeasurementRequest,
    db: Session = Depends(get_db),
) -> CreateMeasurementResponse:
    """Cadastra uma nova medição cardíaca.

    Args:
        dados_medicao: Dados enviados para criação da medição.
        db: Sessão ativa com o banco de dados.

    Returns:
        CreateMeasurementResponse: Dados da medição criada e mensagem de sucesso.
    """
    service = MeasurementService(db)
    return service.cadastrar_medicao(dados_medicao)


@router.get(
    '',
    response_model=list[MeasurementResponse],
    status_code=status.HTTP_200_OK,
    summary='Listar medições',
    description='Lista todas as medições de saúde cardíaca cadastradas.',
    responses={
        500: {
            'model': ErrorResponse,
            'description': 'Erro interno no servidor.',
        },
    },
)
def listar_medicoes(
    db: Session = Depends(get_db),
) -> list[MeasurementResponse]:
    """Lista todas as medições cardíacas cadastradas.

    Args:
        db: Sessão ativa com o banco de dados.

    Returns:
        list[MeasurementResponse]: Lista de medições cadastradas.
    """
    service = MeasurementService(db)
    return service.listar_medicoes()


@router.get(
    '/{id_medicao}',
    response_model=MeasurementResponse,
    status_code=status.HTTP_200_OK,
    summary='Buscar medição',
    description='Busca uma medição de saúde cardíaca pelo identificador.',
    responses={
        404: {
            'model': ErrorResponse,
            'description': 'Medição não encontrada.',
        },
        500: {
            'model': ErrorResponse,
            'description': 'Erro interno no servidor.',
        },
    },
)
def buscar_medicao(
    id_medicao: int,
    db: Session = Depends(get_db),
) -> MeasurementResponse:
    """Busca uma medição cardíaca pelo identificador.

    Args:
        id_medicao: Identificador da medição.
        db: Sessão ativa com o banco de dados.

    Returns:
        MeasurementResponse: Dados da medição encontrada.
    """
    service = MeasurementService(db)
    return service.buscar_medicao(id_medicao)


@router.put(
    '/{id_medicao}',
    response_model=MeasurementResponse,
    status_code=status.HTTP_200_OK,
    summary='Atualizar medição',
    description='Atualiza uma medição de saúde cardíaca existente.',
    responses={
        404: {
            'model': ErrorResponse,
            'description': 'Medição não encontrada.',
        },
        500: {
            'model': ErrorResponse,
            'description': 'Erro interno no servidor.',
        },
    },
)
def atualizar_medicao(
    id_medicao: int,
    dados_medicao: MeasurementRequest,
    db: Session = Depends(get_db),
) -> MeasurementResponse:
    """Atualiza uma medição cardíaca existente.

    Args:
        id_medicao: Identificador da medição.
        dados_medicao: Dados enviados para atualização da medição.
        db: Sessão ativa com o banco de dados.

    Returns:
        MeasurementResponse: Dados da medição atualizada.
    """
    service = MeasurementService(db)
    return service.atualizar_medicao(id_medicao, dados_medicao)


@router.delete(
    '/{id_medicao}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Remover medição',
    description='Remove uma medição de saúde cardíaca existente.',
    responses={
        404: {
            'model': ErrorResponse,
            'description': 'Medição não encontrada.',
        },
        500: {
            'model': ErrorResponse,
            'description': 'Erro interno no servidor.',
        },
    },
)
def remover_medicao(
    id_medicao: int,
    db: Session = Depends(get_db),
) -> Response:
    """Remove uma medição cardíaca existente.

    Args:
        id_medicao: Identificador da medição.
        db: Sessão ativa com o banco de dados.

    Returns:
        Response: Resposta sem conteúdo após remoção.
    """
    service = MeasurementService(db)
    service.remover_medicao(id_medicao)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
