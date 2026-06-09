from datetime import date

from pydantic import BaseModel, Field


class MeasurementRequest(BaseModel):
    """Schema de entrada para criação e atualização de medição cardíaca."""

    pressaoSistolica: int = Field(..., description='Pressão arterial sistólica.')
    pressaoDiastolica: int = Field(..., description='Pressão arterial diastólica.')
    frequenciaCardiaca: int = Field(..., description='Frequência cardíaca medida.')
    nivelOxigenacao: float = Field(..., description='Nível de oxigenação.')
    pesoCorporal: float = Field(
        ...,
        description='Peso corporal no dia da medição.',
    )
    faltaAr: bool = Field(..., description='Indica ocorrência de falta de ar.')
    dorPeito: bool = Field(..., description='Indica ocorrência de dor no peito.')
    tontura: bool = Field(..., description='Indica ocorrência de tontura.')
    observacoes: str | None = Field(
        default=None,
        description='Observações adicionais sobre a medição.',
    )
    dataMedicao: date = Field(
        ...,
        description='Data da medição no formato AAAA-MM-DD.',
    )


class MeasurementResponse(BaseModel):
    """Schema de resposta com os dados da medição cardíaca."""

    idMedicao: int = Field(..., description='Identificador único da medição.')
    pressaoSistolica: int
    pressaoDiastolica: int
    frequenciaCardiaca: int
    nivelOxigenacao: float
    pesoCorporal: float
    faltaAr: bool
    dorPeito: bool
    tontura: bool
    observacoes: str | None
    dataMedicao: date


class CreateMeasurementResponse(MeasurementResponse):
    """Schema de resposta após criação de medição cardíaca."""

    mensagem: str = 'Medição criada com sucesso'
