from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from model import Base
from datetime import datetime
import re

"""
    Classe Login
    A classe cria uma representação genérica de um Login, com os campos login, senha e email
    Cria a tabela de login Login para retenção desses dados no banco.
"""
 
class Usuario(Base):
    __tablename__ = "Login"

    login = Column("login", String(15), unique=True, nullable=False, primary_key=True)
    senha = Column("senha", String(15), unique=False, nullable=False)
    email = Column("email", String(15), unique=True, nullable=False)
    alterar_senha = Column("altera_senha", Boolean, nullable=False)
    cadastrado_por = Column("cadastrado_por", String(15))
    nivel = Column("nivel", Integer, nullable=False, default=1)  # nivel de acesso do usuario, 1 = usuario nivel, 2 = usuario nivel 2, 3 = usuario nivel 3, 4 = usuario nivel 4, 5 = usuario nivel 5, 6 = usuario nivel 6, 7 = usuario nivel 7, 8 = usuario nivel 8, 9 = usuario nivel 9, 10 = usuario nivel 10
    senhaOld1 = Column("senhaOld1", String(15), unique=False, nullable=True)
    senhaOld2 = Column("senhaOld2", String(15), unique=False, nullable=True)
    senhaOld3 = Column("senhaOld3", String(15), unique=False, nullable=True)
    data_criacao_alteracao = Column("data_senha", String(15), unique=False, nullable=False)

    def is_strong_password(self, password: str) -> bool:
        if len(password) < 8:
            return False

        has_upper = re.search(r"[A-Z]", password) is not None
        has_lower = re.search(r"[a-z]", password) is not None
        has_number = re.search(r"\d", password) is not None
        has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None

        return has_upper and has_lower and has_number and has_special

    def diff_time(self):
        return datetime.now() - datetime.strptime(self.data_criacao_alteracao, "%d/%m/%Y, %H:%M:%S")

    def __init__(
        self,
        login: str,
        senha: str,
        email: str,
        cadastrado_por: str,
        alterar_senha: bool = True,
        nivel: int = 1, # nivel de acesso do usuario, 1 = usuario nivel, 2 = usuario nivel 2, 3 = usuario nivel 3, 4 = usuario nivel 4, 5 = usuario nivel 5, 6 = usuario nivel 6, 7 = usuario nivel 7, 8 = usuario nivel 8, 9 = usuario nivel 9, 10 = usuario nivel 10
        data_criacao_alteracao: str = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")

    ) -> None:
        super().__init__()
        self.login = login
        self.senha = senha
        self.email = email
        self.cadastrado_por = cadastrado_por
        self.alterar_senha = alterar_senha
        self.nivel = nivel
        self.data_criacao_alteracao = data_criacao_alteracao