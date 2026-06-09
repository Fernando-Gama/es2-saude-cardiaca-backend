from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///./database.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    """Classe base para os modelos do banco de dados."""


async def get_db() -> AsyncGenerator[Session, None]:
    """Cria uma sessão com o banco de dados para ser usada nas rotas.

    Yields:
        Session: Sessão ativa com o banco de dados.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
