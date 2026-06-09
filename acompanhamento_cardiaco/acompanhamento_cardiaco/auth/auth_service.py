from fastapi import HTTPException, status

from acompanhamento_cardiaco.auth.auth_repository import AuthRepository
from acompanhamento_cardiaco.auth.auth_schemas import TokenResponse
from acompanhamento_cardiaco.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from acompanhamento_cardiaco.security import verificar_senha


class AuthService:
    """Serviço responsável pelas regras de autenticação."""

    def __init__(self, db):
        """Inicializa o serviço de autenticação."""
        self.repository = AuthRepository(db)

    def login(self, email: str, senha: str) -> TokenResponse:
        """Autentica o usuário e retorna tokens de acesso e renovação."""
        usuario = self.repository.buscar_usuario_por_email(email)

        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'codigo': 401, 'mensagem': 'Credenciais inválidas'},
            )

        access_token, expires_in = create_access_token(str(usuario.id_usuario))
        refresh_token = create_refresh_token(str(usuario.id_usuario))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )

    @staticmethod
    def refresh(refresh_token: str) -> TokenResponse:
        """Gera um novo par de tokens a partir de um refresh token válido."""
        try:
            payload = decode_token(refresh_token)

            if payload.get('type') != 'refresh':
                raise ValueError('Tipo inválido')

            user_id = payload['sub']

        except (KeyError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'codigo': 401, 'mensagem': 'Refresh token inválido'},
            )

        access_token, expires_in = create_access_token(user_id)
        new_refresh = create_refresh_token(user_id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh,
            expires_in=expires_in,
        )
