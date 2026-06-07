from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.measurements.measurement_models import Medicao


class MeasurementRepository:
    """Repositório responsável pelo acesso aos dados de medições cardíacas."""

    def __init__(self, db: Session) -> None:
        """Inicializa o repositório de medições.

        Args:
            db: Sessão ativa com o banco de dados.
        """
        self.db = db

    def listar(self) -> list[Medicao]:
        """Lista todas as medições cadastradas.

        Returns:
            list[Medicao]: Lista de medições encontradas.
        """
        stmt = select(Medicao)
        return list(self.db.execute(stmt).scalars().all())

    def listar_por_periodo(
        self,
        data_inicial: date | None = None,
        data_final: date | None = None,
    ) -> list[Medicao]:
        """Lista medições filtradas por período.

        Args:
            data_inicial: Data inicial do filtro.
            data_final: Data final do filtro.

        Returns:
            list[Medicao]: Lista de medições encontradas no período.
        """
        stmt = select(Medicao)

        if data_inicial:
            stmt = stmt.where(Medicao.data_medicao >= data_inicial)

        if data_final:
            stmt = stmt.where(Medicao.data_medicao <= data_final)

        stmt = stmt.order_by(Medicao.data_medicao)

        return list(self.db.execute(stmt).scalars().all())

    def buscar_por_id(self, id_medicao: int) -> Medicao | None:
        """Busca uma medição pelo identificador.

        Args:
            id_medicao: Identificador da medição.

        Returns:
            Medicao | None: Medição encontrada ou None caso não exista.
        """
        stmt = select(Medicao).where(Medicao.id_medicao == id_medicao)
        return self.db.execute(stmt).scalar_one_or_none()

    def salvar(self, medicao: Medicao) -> Medicao:
        """Salva uma nova medição no banco de dados.

        Args:
            medicao: Objeto Medicao que será persistido.

        Returns:
            Medicao: Medição salva com ID gerado pelo banco.

        Raises:
            SQLAlchemyError: Quando ocorre erro ao salvar no banco.
        """
        try:
            self.db.add(medicao)
            self.db.commit()
            self.db.refresh(medicao)
            return medicao

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def atualizar(self, medicao: Medicao) -> Medicao:
        """Atualiza uma medição existente no banco de dados.

        Args:
            medicao: Objeto Medicao que será atualizado.

        Returns:
            Medicao: Medição atualizada.

        Raises:
            SQLAlchemyError: Quando ocorre erro ao atualizar no banco.
        """
        try:
            self.db.commit()
            self.db.refresh(medicao)
            return medicao

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def remover(self, medicao: Medicao) -> None:
        """Remove uma medição existente do banco de dados.

        Args:
            medicao: Objeto Medicao que será removido.

        Raises:
            SQLAlchemyError: Quando ocorre erro ao remover do banco.
        """
        try:
            self.db.delete(medicao)
            self.db.commit()

        except SQLAlchemyError:
            self.db.rollback()
            raise
