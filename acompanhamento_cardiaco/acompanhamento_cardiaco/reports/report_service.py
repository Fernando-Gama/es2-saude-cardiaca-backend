from collections.abc import Iterable
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.measurements.measurement_models import Medicao
from acompanhamento_cardiaco.measurements.measurement_repository import (
    MeasurementRepository,
)
from acompanhamento_cardiaco.reports.report_schemas import (
    HeartHealthReportResponse,
    ReportHistoryItemResponse,
    ReportPeriodResponse,
    ReportSummaryResponse,
    SymptomsSummaryResponse,
)

PRESSAO_SISTOLICA_ALTA = 140
PRESSAO_DIASTOLICA_ALTA = 90
OXIGENACAO_BAIXA = 95
FREQUENCIA_CARDIACA_BAIXA = 60
FREQUENCIA_CARDIACA_ALTA = 100


class ReportService:
    """Serviço responsável por relatórios de saúde cardíaca."""

    def __init__(self, db: Session) -> None:
        """Inicializa o serviço de relatórios."""
        self.measurement_repository = MeasurementRepository(db)

    def gerar_relatorio_saude_cardiaca(
        self,
        data_inicial: date | None = None,
        data_final: date | None = None,
    ) -> HeartHealthReportResponse:
        """Gera relatório com médias, histórico e alertas cardíacos."""
        self._validar_periodo(data_inicial, data_final)

        medicoes = self.measurement_repository.listar_por_periodo(
            data_inicial=data_inicial,
            data_final=data_final,
        )

        return HeartHealthReportResponse(
            periodo=ReportPeriodResponse(
                dataInicial=data_inicial,
                dataFinal=data_final,
            ),
            resumo=self._montar_resumo(medicoes),
            sintomas=self._montar_resumo_sintomas(medicoes),
            alertas=self._montar_alertas(medicoes),
            historico=self._montar_historico(medicoes),
        )

    @staticmethod
    def _validar_periodo(
        data_inicial: date | None,
        data_final: date | None,
    ) -> None:
        if data_inicial and data_final and data_inicial > data_final:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    'codigo': 400,
                    'mensagem': 'Período inválido',
                    'detalhes': {
                        'campo': 'dataInicial/dataFinal',
                        'motivo': (
                            'A data inicial deve ser menor ou igual à final.'
                        ),
                    },
                },
            )

    @staticmethod
    def _montar_resumo(medicoes: list[Medicao]) -> ReportSummaryResponse:
        total = len(medicoes)

        if total == 0:
            return ReportSummaryResponse(
                totalMedicoes=0,
                mediaPressaoSistolica=None,
                mediaPressaoDiastolica=None,
                mediaFrequenciaCardiaca=None,
                mediaNivelOxigenacao=None,
                mediaPesoCorporal=None,
            )

        return ReportSummaryResponse(
            totalMedicoes=total,
            mediaPressaoSistolica=_media(
                medicao.pressao_sistolica for medicao in medicoes
            ),
            mediaPressaoDiastolica=_media(
                medicao.pressao_diastolica for medicao in medicoes
            ),
            mediaFrequenciaCardiaca=_media(
                medicao.frequencia_cardiaca for medicao in medicoes
            ),
            mediaNivelOxigenacao=_media(
                medicao.nivel_oxigenacao for medicao in medicoes
            ),
            mediaPesoCorporal=_media(
                medicao.peso_corporal for medicao in medicoes
            ),
        )

    @staticmethod
    def _montar_resumo_sintomas(
        medicoes: list[Medicao],
    ) -> SymptomsSummaryResponse:
        return SymptomsSummaryResponse(
            registrosFaltaAr=sum(1 for medicao in medicoes if medicao.falta_ar),
            registrosDorPeito=sum(1 for medicao in medicoes if medicao.dor_peito),
            registrosTontura=sum(1 for medicao in medicoes if medicao.tontura),
        )

    @staticmethod
    def _montar_historico(
        medicoes: list[Medicao],
    ) -> list[ReportHistoryItemResponse]:
        return [
            ReportHistoryItemResponse(
                dataMedicao=medicao.data_medicao,
                pressaoSistolica=medicao.pressao_sistolica,
                pressaoDiastolica=medicao.pressao_diastolica,
                frequenciaCardiaca=medicao.frequencia_cardiaca,
                nivelOxigenacao=medicao.nivel_oxigenacao,
                pesoCorporal=medicao.peso_corporal,
                faltaAr=medicao.falta_ar,
                dorPeito=medicao.dor_peito,
                tontura=medicao.tontura,
            )
            for medicao in sorted(medicoes, key=lambda item: item.data_medicao)
        ]

    @staticmethod
    def _montar_alertas(medicoes: list[Medicao]) -> list[str]:
        alertas = []

        total_pressao_alta = sum(
            1
            for medicao in medicoes
            if medicao.pressao_sistolica >= PRESSAO_SISTOLICA_ALTA
            or medicao.pressao_diastolica >= PRESSAO_DIASTOLICA_ALTA
        )
        total_oxigenacao_baixa = sum(
            1
            for medicao in medicoes
            if medicao.nivel_oxigenacao < OXIGENACAO_BAIXA
        )
        total_frequencia_alterada = sum(
            1
            for medicao in medicoes
            if medicao.frequencia_cardiaca < FREQUENCIA_CARDIACA_BAIXA
            or medicao.frequencia_cardiaca > FREQUENCIA_CARDIACA_ALTA
        )
        total_dor_peito = sum(1 for medicao in medicoes if medicao.dor_peito)
        total_falta_ar = sum(1 for medicao in medicoes if medicao.falta_ar)
        total_tontura = sum(1 for medicao in medicoes if medicao.tontura)

        if total_pressao_alta:
            alertas.append(
                f'Pressão arterial elevada em {total_pressao_alta} medição(ões).'
            )

        if total_oxigenacao_baixa:
            alertas.append(
                f'Oxigenação abaixo de 95% em {total_oxigenacao_baixa} '
                'medição(ões).'
            )

        if total_frequencia_alterada:
            alertas.append(
                'Frequência cardíaca fora da faixa esperada em '
                f'{total_frequencia_alterada} medição(ões).'
            )

        if total_dor_peito:
            alertas.append(
                f'Dor no peito registrada em {total_dor_peito} medição(ões).'
            )

        if total_falta_ar:
            alertas.append(
                f'Falta de ar registrada em {total_falta_ar} medição(ões).'
            )

        if total_tontura:
            alertas.append(f'Tontura registrada em {total_tontura} medição(ões).')

        if not medicoes:
            alertas.append('Nenhuma medição encontrada para o período informado.')

        return alertas


def _media(valores: Iterable[float | int]) -> float:
    valores_calculados = list(valores)
    return round(sum(valores_calculados) / len(valores_calculados), 2)
