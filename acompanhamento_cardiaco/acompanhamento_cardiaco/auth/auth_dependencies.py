from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from acompanhamento_cardiaco.auth.jwt_handler import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    """Retorna o id do usuário autenticado pelo token Bearer."""
    if not credentials:
        raise _erro_token_invalido()

    token = credentials.credentials

    try:
        payload = decode_token(token)

        if payload.get('type') != 'access':
            raise ValueError('Tipo inválido')

        return int(payload['sub'])

    except (KeyError, TypeError, ValueError):
        raise _erro_token_invalido()


def _erro_token_invalido() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'codigo': 401, 'mensagem': 'Token inválido ou expirado'},
        headers={'WWW-Authenticate': 'Bearer'},
    )
