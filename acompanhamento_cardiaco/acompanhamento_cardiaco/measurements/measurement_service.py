from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.measurements.measurement_models import Medicao
from acompanhamento_cardiaco.measurements.measurement_repository import (
    MeasurementRepository,
)
from acompanhamento_cardiaco.measurements.measurement_schemas import (
    CreateMeasurementResponse,
    MeasurementRequest,
    MeasurementResponse,
)


class MeasurementService:
    """Serviço responsável pelas regras de negócio de medições cardíacas."""

    def __init__(self, db: Session) -> None:
        """Inicializa o serviço de medições.

        Args:
            db: Sessão ativa com o banco de dados.
        """
        self.repository = MeasurementRepository(db)

    def cadastrar_medicao(
        self,
        dados_medicao: MeasurementRequest,
        id_usuario: int,
    ) -> CreateMeasurementResponse:
        """Cadastra uma nova medição cardíaca no sistema.

        Args:
            dados_medicao: Dados recebidos para criação da medição.
            id_usuario: Identificador do usuário autenticado.

        Returns:
            CreateMeasurementResponse: Dados da medição criada.
        """
        medicao = Medicao(
            id_usuario=id_usuario,
            pressao_sistolica=dados_medicao.pressaoSistolica,
            pressao_diastolica=dados_medicao.pressaoDiastolica,
            frequencia_cardiaca=dados_medicao.frequenciaCardiaca,
            nivel_oxigenacao=dados_medicao.nivelOxigenacao,
            peso_corporal=dados_medicao.pesoCorporal,
            falta_ar=dados_medicao.faltaAr,
            dor_peito=dados_medicao.dorPeito,
            tontura=dados_medicao.tontura,
            observacoes=dados_medicao.observacoes,
            data_medicao=dados_medicao.dataMedicao,
        )

        medicao_criada = self.repository.salvar(medicao)

        return CreateMeasurementResponse(
            **self._montar_resposta_medicao(medicao_criada).model_dump(),
            mensagem='Medição criada com sucesso',
        )

    def listar_medicoes(self, id_usuario: int) -> list[MeasurementResponse]:
        """Lista todas as medições cardíacas cadastradas.

        Args:
            id_usuario: Identificador do usuário autenticado.

        Returns:
            list[MeasurementResponse]: Lista de medições cadastradas.
        """
        medicoes = self.repository.listar_por_usuario(id_usuario)
        return [self._montar_resposta_medicao(medicao) for medicao in medicoes]

    def buscar_medicao(
        self,
        id_medicao: int,
        id_usuario: int,
    ) -> MeasurementResponse:
        """Busca uma medição cardíaca pelo identificador.

        Args:
            id_medicao: Identificador da medição.
            id_usuario: Identificador do usuário autenticado.

        Returns:
            MeasurementResponse: Dados da medição encontrada.

        Raises:
            HTTPException: Quando a medição não existe.
        """
        medicao = self._buscar_medicao_existente(id_medicao, id_usuario)
        return self._montar_resposta_medicao(medicao)

    def atualizar_medicao(
        self,
        id_medicao: int,
        dados_medicao: MeasurementRequest,
        id_usuario: int,
    ) -> MeasurementResponse:
        """Atualiza uma medição cardíaca existente.

        Args:
            id_medicao: Identificador da medição.
            dados_medicao: Dados recebidos para atualização da medição.
            id_usuario: Identificador do usuário autenticado.

        Returns:
            MeasurementResponse: Dados da medição atualizada.

        Raises:
            HTTPException: Quando a medição não existe.
        """
        medicao = self._buscar_medicao_existente(id_medicao, id_usuario)

        medicao.pressao_sistolica = dados_medicao.pressaoSistolica
        medicao.pressao_diastolica = dados_medicao.pressaoDiastolica
        medicao.frequencia_cardiaca = dados_medicao.frequenciaCardiaca
        medicao.nivel_oxigenacao = dados_medicao.nivelOxigenacao
        medicao.peso_corporal = dados_medicao.pesoCorporal
        medicao.falta_ar = dados_medicao.faltaAr
        medicao.dor_peito = dados_medicao.dorPeito
        medicao.tontura = dados_medicao.tontura
        medicao.observacoes = dados_medicao.observacoes
        medicao.data_medicao = dados_medicao.dataMedicao

        medicao_atualizada = self.repository.atualizar(medicao)
        return self._montar_resposta_medicao(medicao_atualizada)

    def remover_medicao(self, id_medicao: int, id_usuario: int) -> None:
        """Remove uma medição cardíaca existente.

        Args:
            id_medicao: Identificador da medição.
            id_usuario: Identificador do usuário autenticado.

        Raises:
            HTTPException: Quando a medição não existe.
        """
        medicao = self._buscar_medicao_existente(id_medicao, id_usuario)
        self.repository.remover(medicao)

    def _buscar_medicao_existente(
        self,
        id_medicao: int,
        id_usuario: int,
    ) -> Medicao:
        """Busca uma medição existente ou levanta erro 404.

        Args:
            id_medicao: Identificador da medição.
            id_usuario: Identificador do usuário autenticado.

        Returns:
            Medicao: Medição encontrada.

        Raises:
            HTTPException: Quando a medição não existe.
        """
        medicao = self.repository.buscar_por_id_e_usuario(id_medicao, id_usuario)

        if not medicao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    'codigo': 404,
                    'mensagem': 'Medição não encontrada',
                    'detalhes': {
                        'campo': 'id_medicao',
                        'motivo': 'Não existe medição com o ID informado.',
                    },
                },
            )

        return medicao

    @staticmethod
    def _montar_resposta_medicao(medicao: Medicao) -> MeasurementResponse:
        """Monta a resposta com os dados da medição.

        Args:
            medicao: Medição cadastrada no banco de dados.

        Returns:
            MeasurementResponse: Resposta no formato definido no Swagger.
        """
        return MeasurementResponse(
            idMedicao=medicao.id_medicao,
            pressaoSistolica=medicao.pressao_sistolica,
            pressaoDiastolica=medicao.pressao_diastolica,
            frequenciaCardiaca=medicao.frequencia_cardiaca,
            nivelOxigenacao=medicao.nivel_oxigenacao,
            pesoCorporal=medicao.peso_corporal,
            faltaAr=medicao.falta_ar,
            dorPeito=medicao.dor_peito,
            tontura=medicao.tontura,
            observacoes=medicao.observacoes,
            dataMedicao=medicao.data_medicao,
        )
