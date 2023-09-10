from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from model import Base

"""
    Classe Login
    A classe cria uma representação genérica de um Login, com os campos login, senha e email
    Cria a tabela de login Login para retenção desses dados no banco.
"""


class Usuario(Base):
    __tablename__ = "Login"

    id = Column("id_login", Integer, primary_key=True)
    login = Column("login", String(15), unique=True, nullable=False)
    senha = Column("senha", String(15), unique=False, nullable=False)
    email = Column("email", String(15), unique=True, nullable=False)
    alterar_senha = Column("altera_senha", Boolean, nullable=False)
    cadastrado_por = Column("cadastrado_por", String(15))

    def __init__(
        self,
        login: str,
        senha: str,
        email: str,
        cadastrado_por: str,
        alterar_senha: bool = True,
    ) -> None:
        super().__init__()
        self.login = login
        self.senha = senha
        self.email = email
        self.cadastrado_por = cadastrado_por
        self.alterar_senha = alterar_senha
