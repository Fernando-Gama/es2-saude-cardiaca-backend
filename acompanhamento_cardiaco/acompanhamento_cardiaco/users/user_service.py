from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from acompanhamento_cardiaco.acompanhamento_cardiaco.security import gerar_hash_senha
from acompanhamento_cardiaco.acompanhamento_cardiaco.users.user_models import User
from acompanhamento_cardiaco.acompanhamento_cardiaco.users.user_repository import UserRepository
from acompanhamento_cardiaco.acompanhamento_cardiaco.users.user_schemas import (
    CreateUserResponse,
    UserRegistrationRequest,
)


class UserService:
    """Serviço responsável pelas regras de negócio de usuários."""

    def __init__(self, db: Session) -> None:
        """Inicializa o serviço de usuários.

        Args:
            db: Sessão ativa com o banco de dados.
        """
        self.repository = UserRepository(db)

    def cadastrar_usuario(
        self,
        dados_usuario: UserRegistrationRequest,
    ) -> CreateUserResponse:
        """Cadastra um novo usuário no sistema.

        Args:
            dados_usuario: Dados recebidos para criação da conta.

        Returns:
            CreateUserResponse: Dados públicos do usuário criado.

        Raises:
            HTTPException: Quando as senhas não conferem ou o e-mail já existe.
        """
        self._validar_confirmacao_senha(dados_usuario)

        self._validar_email_disponivel(dados_usuario.email)

        senha_hash = gerar_hash_senha(dados_usuario.senha)

        usuario = User(
            nome=dados_usuario.nome,
            sobrenome=dados_usuario.sobrenome,
            email=dados_usuario.email,
            celular=dados_usuario.celular,
            senha_hash=senha_hash,
            data_nascimento=dados_usuario.dataNascimento,
            sexo=dados_usuario.sexo.value,
            pais_residencia=dados_usuario.paisResidencia,
            naturalidade_uf=dados_usuario.naturalidadeUF,
        )

        usuario_criado = self.repository.salvar(usuario)

        return self._montar_resposta_usuario_criado(usuario_criado)

    def _validar_confirmacao_senha(
        self,
        dados_usuario: UserRegistrationRequest,
    ) -> None:
        """Valida se a senha e a confirmação de senha são iguais.

        Args:
            dados_usuario: Dados recebidos para criação da conta.

        Raises:
            HTTPException: Quando a senha e a confirmação são diferentes.
        """
        if dados_usuario.senha != dados_usuario.confirmarSenha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "codigo": 400,
                    "mensagem": "Campos obrigatórios não preenchidos",
                    "detalhes": {
                        "campo": "confirmarSenha",
                        "motivo": "A confirmação de senha deve ser igual à senha.",
                    },
                },
            )

    def _validar_email_disponivel(self, email: str) -> None:
        """Valida se o e-mail informado ainda não está cadastrado.

        Args:
            email: E-mail informado no cadastro.

        Raises:
            HTTPException: Quando já existe usuário com o e-mail informado.
        """
        usuario_existente = self.repository.buscar_por_email(email)

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "codigo": 409,
                    "mensagem": "E-mail já cadastrado",
                    "detalhes": {
                        "campo": "email",
                        "motivo": "Já existe uma conta utilizando este e-mail.",
                    },
                },
            )

    def _montar_resposta_usuario_criado(
        self,
        usuario: User,
    ) -> CreateUserResponse:
        """Monta a resposta de sucesso do cadastro.

        Args:
            usuario: Usuário criado no banco de dados.

        Returns:
            CreateUserResponse: Resposta no formato definido no Swagger.
        """
        return CreateUserResponse(
            idUsuario=usuario.id_usuario,
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            email=usuario.email,
            celular=usuario.celular,
            dataNascimento=usuario.data_nascimento,
            sexo=usuario.sexo,
            paisResidencia=usuario.pais_residencia,
            naturalidadeUF=usuario.naturalidade_uf,
            mensagem="Conta criada com sucesso",
        )
