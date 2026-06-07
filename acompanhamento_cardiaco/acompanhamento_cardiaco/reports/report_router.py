from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.database import get_db
from acompanhamento_cardiaco.reports.report_schemas import (
    HeartHealthReportResponse,
)
from acompanhamento_cardiaco.reports.report_service import ReportService
from acompanhamento_cardiaco.users.user_schemas import ErrorResponse

router = APIRouter(
    prefix='/reports',
    tags=['Relatórios'],
)


@router.get(
    '/heart-health',
    response_model=HeartHealthReportResponse,
    status_code=status.HTTP_200_OK,
    summary='Relatório de saúde cardíaca',
    description=(
        'Apresenta médias, histórico e alertas relacionados à evolução da '
        'saúde cardíaca.'
    ),
    responses={
        400: {
            'model': ErrorResponse,
            'description': 'Período inválido.',
        },
        500: {
            'model': ErrorResponse,
            'description': 'Erro interno no servidor.',
        },
    },
)
def gerar_relatorio_saude_cardiaca(
    data_inicial: date | None = Query(
        default=None,
        alias='dataInicial',
        description='Data inicial do relatório no formato AAAA-MM-DD.',
    ),
    data_final: date | None = Query(
        default=None,
        alias='dataFinal',
        description='Data final do relatório no formato AAAA-MM-DD.',
    ),
    db: Session = Depends(get_db),
) -> HeartHealthReportResponse:
    """Gera relatório de evolução da saúde cardíaca.

    Args:
        data_inicial: Data inicial usada no filtro.
        data_final: Data final usada no filtro.
        db: Sessão ativa com o banco de dados.

    Returns:
        HeartHealthReportResponse: Relatório consolidado de saúde cardíaca.
    """
    service = ReportService(db)
    return service.gerar_relatorio_saude_cardiaca(data_inicial, data_final)
