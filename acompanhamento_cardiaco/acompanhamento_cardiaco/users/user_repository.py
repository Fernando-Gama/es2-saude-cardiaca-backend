from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.acompanhamento_cardiaco.users.user_models import User


class UserRepository:
    """Repositório responsável pelo acesso aos dados de usuários."""

    def __init__(self, db: Session) -> None:
        """Inicializa o repositório de usuários.

        Args:
            db: Sessão ativa com o banco de dados.
        """
        self.db = db

    def buscar_por_email(self, email: str) -> User | None:
        """Busca um usuário pelo e-mail.

        Args:
            email: E-mail do usuário.

        Returns:
            User | None: Usuário encontrado ou None caso não exista.
        """
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def salvar(self, usuario: User) -> User:
        """Salva um novo usuário no banco de dados.

        Args:
            usuario: Objeto User que será persistido.

        Returns:
            User: Usuário salvo com ID gerado pelo banco.

        Raises:
            SQLAlchemyError: Quando ocorre erro ao salvar no banco.
        """
        try:
            self.db.add(usuario)
            self.db.commit()
            self.db.refresh(usuario)
            return usuario

        except SQLAlchemyError:
            self.db.rollback()
            raise
