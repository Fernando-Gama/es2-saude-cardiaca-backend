from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from acompanhamento_cardiaco.database import Base


class User(Base):
    """Modelo que representa a tabela de usuários no banco de dados."""

    __tablename__ = "users"

    id_usuario: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    sobrenome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    celular: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    data_nascimento: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    sexo: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
    )

    pais_residencia: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    naturalidade_uf: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )
