from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def gerar_hash_senha(senha: str) -> str:
    """Gera o hash de uma senha.

    Args:
        senha: Senha em texto puro informada pelo usuário.

    Returns:
        str: Hash seguro da senha.
    """
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se uma senha corresponde ao hash armazenado.

    Args:
        senha: Senha em texto puro informada pelo usuário.
        senha_hash: Hash da senha armazenado no banco de dados.

    Returns:
        bool: True se a senha corresponder ao hash, False caso contrário.
    """
    return pwd_context.verify(senha, senha_hash)
