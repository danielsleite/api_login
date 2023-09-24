from pydantic import BaseModel
from typing import Optional, List
from model import Usuario


class UsuarioSchema(BaseModel):
    """Define como um novo login a ser inserido deve ser representado"""

    login: str = "jsilva"
    senha: str = "*******"
    email: str = "joao.silva@empresa.com"
    alterar_senha: bool = True
    cadastrado_por: str = "Admin"


class LoginBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca do funcinário.

    A busca é feita baseada no login do login
    """

    login: str = "jsilva"


class LoginSenhaNovaSchema(BaseModel):
    """Define a estrutura para envio de uma nova senha.
    Além do usuário, para a busca, e a senha para a atualização, também é enviado o flag de reset.
    Caso o flag de reset seja verdadeiro, o valor da senha padrão = "123456", é utlizado, no lugar
    do valor do campo senha

    """

    login: str = "jsilva"
    senha: str = "******"
    alterar_senha: bool = False


class ListagemLoginsSchema(BaseModel):
    """Define como uma listagem de logins será retornada."""

    logins: List[UsuarioSchema]


class InterfaceParaSenha(BaseModel):
    """Define como o retorno da consulta de senha ocorre."""

    senha: str = "******"


class InterfaceParaLogin(BaseModel):
    """Define como o formado do envio do dado para login."""

    login: str = "jsilva"
    senha: str = "123456"


class RetornoLoginValido(BaseModel):
    """
    Retorna o status de login do usuário, após validação do login e senha no banco
    """

    logado: bool = True
    lterar_senha: bool = False


class RetornoLoginNaoValido(BaseModel):
    """
    Retorna o status de login do usuário, após validação do login e senha no banco
    """

    logado: bool = False
    alterar_senha: bool = False


class UsuarioViewSchema(BaseModel):
    """Define como um funcinário será retornado"""

    login: str = "jsilva"
    senha: str = "*******"
    email: str = "joao.silva@empresa.com"
    alterar_senha: bool = True
    cadastrado_por: str = "Admin"


def apresenta_logins(logins: List[Usuario]):
    """Retorna um dicionario com todos os funcionarios cadastrados no banco e seus respectivos capos."""
    result = []

    for login in logins:
        result.append(apresenta_login(login))

    return {"logins": result}


def apresenta_login(login: Usuario):
    """Retorna os campos que representam o funcionaro."""
    return {
        "login": login.login,
        "senha": "******",
        "email": login.email,
        "cadastrado_por": login.cadastrado_por,
        "alterar_senha": login.alterar_senha,
    }


def apresenta_senha(login: Usuario):
    """Retorna uma string com a senha do usuario

    Args:
        login (Login): objeto funcionaro obtido pela query
    """

    return {
        "senha": login.senha,
    }
