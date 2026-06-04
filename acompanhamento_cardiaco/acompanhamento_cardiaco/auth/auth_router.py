from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from acompanhamento_cardiaco.acompanhamento_cardiaco.database import get_db
from acompanhamento_cardiaco.acompanhamento_cardiaco.auth.auth_service import AuthService
from acompanhamento_cardiaco.acompanhamento_cardiaco.auth.auth_schemas import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponse, summary="Login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    service = AuthService(db)
    return service.login(payload.email, payload.senha)


@router.post("/refresh", response_model=TokenResponse, summary="Refresh token")
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> TokenResponse:
    service = AuthService(db)
    return service.refresh(payload.refresh_token)