from datetime import date

from sqlalchemy import Boolean, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from acompanhamento_cardiaco.database import Base


class Medicao(Base):
    """Modelo que representa a tabela de medições cardíacas no banco."""

    __tablename__ = 'medicoes'

    id_medicao: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey('users.id_usuario'),
        nullable=False,
        index=True,
    )

    pressao_sistolica: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    pressao_diastolica: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    frequencia_cardiaca: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    nivel_oxigenacao: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    peso_corporal: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    falta_ar: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    dor_peito: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    tontura: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    observacoes: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    data_medicao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
