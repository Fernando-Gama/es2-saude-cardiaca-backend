from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class SexoEnum(str, Enum):
    """Enum com os valores permitidos para o sexo do usuário."""

    M = "M"
    F = "F"


class UserRegistrationRequest(BaseModel):
    """Schema de entrada para cadastro de usuário."""

    nome: str = Field(..., description="Primeiro nome do usuário.")
    sobrenome: str = Field(..., description="Sobrenome do usuário.")
    email: EmailStr = Field(..., description="E-mail único do usuário.")
    celular: str = Field(..., description="Número de celular com código do país.")
    senha: str = Field(..., description="Senha do usuário.")
    confirmarSenha: str = Field(..., description="Confirmação da senha informada.")
    dataNascimento: date = Field(
        ...,
        description="Data de nascimento no formato AAAA-MM-DD.",
    )
    sexo: SexoEnum = Field(..., description="Sexo informado pelo usuário.")
    paisResidencia: str = Field(..., description="País de residência do usuário.")
    naturalidadeUF: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Unidade federativa de naturalidade.",
    )


class UserResponse(BaseModel):
    """Schema de resposta com os dados públicos do usuário."""

    idUsuario: int = Field(..., description="Identificador único do usuário.")
    nome: str
    sobrenome: str
    email: EmailStr
    celular: str
    dataNascimento: date
    sexo: SexoEnum
    paisResidencia: str
    naturalidadeUF: str


class CreateUserResponse(UserResponse):
    """Schema de resposta após criação de usuário."""

    mensagem: str = "Conta criada com sucesso"


class ErrorResponse(BaseModel):
    """Schema padrão para respostas de erro da API."""

    codigo: int = Field(..., description="Código HTTP do erro.")
    mensagem: str = Field(..., description="Mensagem explicando o erro ocorrido.")
    detalhes: dict[str, Any] | None = Field(
        default=None,
        description="Detalhes adicionais sobre o erro, quando existirem.",
    )
