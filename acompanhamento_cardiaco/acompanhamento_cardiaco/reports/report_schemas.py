from datetime import date

from pydantic import BaseModel, Field


class ReportPeriodResponse(BaseModel):
    """Schema com o período considerado no relatório."""

    dataInicial: date | None = Field(
        default=None,
        description='Data inicial usada no filtro.',
    )
    dataFinal: date | None = Field(
        default=None,
        description='Data final usada no filtro.',
    )


class ReportSummaryResponse(BaseModel):
    """Schema com indicadores consolidados de saúde cardíaca."""

    totalMedicoes: int = Field(..., description='Total de medições analisadas.')
    mediaPressaoSistolica: float | None = Field(
        default=None,
        description='Média da pressão sistólica.',
    )
    mediaPressaoDiastolica: float | None = Field(
        default=None,
        description='Média da pressão diastólica.',
    )
    mediaFrequenciaCardiaca: float | None = Field(
        default=None,
        description='Média da frequência cardíaca.',
    )
    mediaNivelOxigenacao: float | None = Field(
        default=None,
        description='Média do nível de oxigenação.',
    )
    mediaPesoCorporal: float | None = Field(
        default=None,
        description='Média do peso corporal.',
    )


class SymptomsSummaryResponse(BaseModel):
    """Schema com a quantidade de sintomas registrados."""

    registrosFaltaAr: int = Field(..., description='Registros com falta de ar.')
    registrosDorPeito: int = Field(..., description='Registros com dor no peito.')
    registrosTontura: int = Field(..., description='Registros com tontura.')


class ReportHistoryItemResponse(BaseModel):
    """Schema com um ponto do histórico usado para gráficos."""

    dataMedicao: date
    pressaoSistolica: int
    pressaoDiastolica: int
    frequenciaCardiaca: int
    nivelOxigenacao: float
    pesoCorporal: float
    faltaAr: bool
    dorPeito: bool
    tontura: bool


class HeartHealthReportResponse(BaseModel):
    """Schema de resposta do relatório de saúde cardíaca."""

    periodo: ReportPeriodResponse
    resumo: ReportSummaryResponse
    sintomas: SymptomsSummaryResponse
    alertas: list[str]
    historico: list[ReportHistoryItemResponse]
