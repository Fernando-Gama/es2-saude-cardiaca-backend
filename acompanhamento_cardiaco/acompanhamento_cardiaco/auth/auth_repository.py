from acompanhamento_cardiaco.users.user_repository import UserRepository


class AuthRepository:
    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def buscar_usuario_por_email(self, email: str):
        return self.user_repo.buscar_por_email(email)
