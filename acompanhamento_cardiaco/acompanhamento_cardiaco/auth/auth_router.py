from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.auth.auth_schemas import (
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from acompanhamento_cardiaco.auth.auth_service import AuthService
from acompanhamento_cardiaco.database import get_db

router = APIRouter(prefix='/auth', tags=['Autenticação'])


@router.post('/login', response_model=TokenResponse, summary='Login')
async def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Autentica um usuário por e-mail e senha."""
    service = AuthService(db)
    return service.login(payload.email, payload.senha)


@router.post('/refresh', response_model=TokenResponse, summary='Refresh token')
async def refresh(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Renova os tokens usando um refresh token válido."""
    service = AuthService(db)
    return service.refresh(payload.refresh_token)
