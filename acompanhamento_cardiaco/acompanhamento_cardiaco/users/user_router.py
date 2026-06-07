from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.database import get_db
from acompanhamento_cardiaco.users.user_schemas import (
    CreateUserResponse,
    ErrorResponse,
    UserRegistrationRequest,
)
from acompanhamento_cardiaco.users.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Usuários"],
)


@router.post(
    "",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar conta",
    description="Cadastra um novo usuário no sistema.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Campos obrigatórios não preenchidos.",
        },
        409: {
            "model": ErrorResponse,
            "description": "E-mail já cadastrado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Erro interno no servidor.",
        },
    },
)
def cadastrar_usuario(
    dados_usuario: UserRegistrationRequest,
    db: Session = Depends(get_db),
) -> CreateUserResponse:
    """Cadastra um novo usuário no sistema.

    Args:
        dados_usuario: Dados enviados pelo usuário para criação da conta.
        db: Sessão ativa com o banco de dados.

    Returns:
        CreateUserResponse: Dados do usuário criado e mensagem de sucesso.
    """
    service = UserService(db)
    return service.cadastrar_usuario(dados_usuario)
