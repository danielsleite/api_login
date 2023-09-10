from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Usuario


from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(
    title="API para gerenciamento de logins. Autor: Daniel Leite", version="1.0.0"
)
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(
    name="Documentação",
    description="Documentação da API com a ferramenta Swagger",
)
login_tag = Tag(
    name="Login",
    description="Adição, visualização, validação de login e alteração de senhas de usuario",
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela de documentação."""
    return redirect("/openapi/swagger#/")


@app.post(
    "/login_cadastro",
    tags=[login_tag],
    responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema},
)
def add_login(form: UsuarioSchema):
    """Adiciona um novo login à base de dados

    Retorna uma representação dos login, em caso de sucesso, ou uma mensagem de erro, em caso de falha.
    Ao criar um funcionário, o campo senha sempre será preenchido com o valor padrão = "123456" e um flag para
    reset da senha será ligado.
    """
    usr = Usuario(
        login=form.login,
        senha="123456",
        email=form.email,
        cadastrado_por=form.cadastrado_por,
        alterar_senha=True,
    )
    logger.debug(f"Tentativa de adicionar login de nome: '{usr.login}'")
    logger.warning(apresenta_login(usr))
    try:
        # criando conexão com a base
        session = Session()

        # adicionando produto
        session.add(usr)

        # efetivando o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Adicionado login de nome: '{usr.login}'")
        return apresenta_login(usr), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "login de mesmo nome já salvo na base :/"
        logger.warning(f"Erro tentar cadastrar: '{usr.login}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao tentar cadastrar o login: '{usr.login}', {error_msg}")
        return {"message": error_msg}, 400


@app.get(
    "/logins",
    tags=[login_tag],
    responses={"200": ListagemLoginsSchema, "404": ErrorSchema},
)
def get_logins():
    """Faz a busca por todos os logins cadastrados

    Retorna uma representação da listagem de funcionários, em caso de sucesso.
    """

    logger.debug("Coletando informação de logins")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    logins = session.query(Usuario).all()

    if not logins:
        # se não há produtos cadastrados
        return {"logins": []}, 200
    else:
        logger.debug("%d logins econtrados" % len(logins))
        # retorna a representação de produto
        print(logins)
        return apresenta_logins(logins), 200


@app.post(
    "/login_validacao",
    tags=[login_tag],
    responses={"200": RetornoLoginValido, "202": RetornoLoginNaoValido},
)
def get_login(form: InterfaceParaLogin):
    """Envia os dados de login e senha do usuário, para validação com a interface.

    Retorna um dicionário com a informação de login realizado e o status de reset de senha.
    """

    logger.debug(f"Validando login do login:  #{form.login}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usr = (
        session.query(Usuario)
        .filter(Usuario.login == form.login)
        .filter(Usuario.senha == form.senha)
        .first()
    )

    if not usr:
        # se o produto não foi encontrado
        error_msg = "login não encontrado na base :/"
        logger.warning(
            f"Erro ao buscar login '{form.login}' e senha '{form.senha}', {error_msg}"
        )
        return {"logado": False}, 202

    else:
        # logger.warning(f"Login realizado com sucesso'{form.login}' e senha '{form.senha}', {error_msg}")
        logger.warning(f"Logado: '{usr.login}'")
        # retorna a representação de produto
        return {"logado": True, "alterar_senha": usr.alterar_senha}, 200


@app.put(
    "/senha",
    tags=[login_tag],
    responses={
        "200": UsuarioViewSchema,
        "404": ErrorSchema,
        "400": ErrorSchema,
    },
)
def altera_senha(form: LoginSenhaNovaSchema):
    """Altera a senha de um dado funcioanrio, a partir da informação de login do mesmo.
      Caso a flag de reset esteja ativa, o senha colocada será a senha padrão '123456'

    Retorna uma representação dos logins.
    """

    pessoa_login = form.login
    usr = busca_por_login(pessoa_login)
    nova_senha = form.senha

    if form.alterar_senha:
        nova_senha = "123456"

    elif not nova_senha:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Nao foi possivel alterar a senha do login. Verifique se o campo usr está correto.:/"
        logger.warning(f"Erro ao alterar senha do login: '{usr.login}', {error_msg}")
        return {"message": error_msg}, 404

    if not usr:
        # se o produto não foi encontrado
        error_msg = "login não encontrado na base :/"
        logger.warning(f"Erro ao buscar login '{pessoa_login}', {error_msg}")
        return {"message": error_msg}, 404

    try:
        # criando conexão com a base
        logger.warning(f"Encontrado usuario de login: '{pessoa_login}'")
        session = Session()
        session.query(Usuario).filter(Usuario.login == pessoa_login).update(
            {
                Usuario.senha: nova_senha,
                Usuario.alterar_senha: form.alterar_senha,
            }
        )
        session.commit()
        logger.debug(f"Alterada a senha do login: '{usr.login}'")
        return apresenta_login(usr), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Nao foi possivel alterar a senha do login. Verifique se o campo login está correto.:/"
        logger.warning(f"Erro ao alterar senha do login: '{usr.login}', {error_msg}")
        return {"message": error_msg}, 404

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Erro ao atualizar a senha :/"
        logger.warning(f"Erro ao alterar a senha do '{usr.login}', {error_msg}")
        return {"message": error_msg}, 400


@app.delete(
    "/login_excluir",
    tags=[login_tag],
    responses={
        "200": ErrorSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
        "409": ErrorSchema,
    },
)
def exclui_login(query: LoginBuscaSchema):
    """Apaga o login da base de dados

    Utiliza o campo login como filtro para busca do funcionário que será excluído

    Retorna uma mensagem com a confirmação da exclusão ou informação do erro
    """

    pessoa_login = query.login
    usr = busca_por_login(pessoa_login)

    if not usr:
        # se o produto não foi encontrado
        error_msg = f"login não encontrado na base: '{query.login}'"
        logger.warning(f"Erro ao buscar login '{pessoa_login}', {error_msg}")
        return {"message": error_msg}, 404

    try:
        # Salva o CPF do login para fazer a relaçaõ entra a tebela login e a tabela login
        # criando conexão com a base
        session = Session()

        session.query(Usuario).filter(Usuario.login == pessoa_login).delete()

        session.commit()

        logger.debug(f"login excluido com sucesso: '{usr.login}'")
        error_msg = f"login exlcuido com sucesso: '{usr.login}'"
        return {"message": error_msg}, 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = (
            "Nao foi excluir o login. Verifique se o campo login está correto.:/"
        )
        logger.warning(f"Erro ao excluir o login: '{usr.login}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Erro ao atualizar os dados do login :/"
        logger.warning(f"Erro ao dados do login: '{usr.login}', {error_msg}")
        return {"message": error_msg}, 400


# Função auxiliar para buscar funcionário
def busca_por_login(login: str) -> Usuario:
    logger.debug(f"Procurando senha do login de login:  #{login}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usr = session.query(Usuario).filter(Usuario.login == login).first()
    return usr
