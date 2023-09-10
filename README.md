# API para cadastro de funcionários

Esse projeto apresenta o MVP de requisido para conclusão da sprint 1 da curso de  **Engenharia de Softaware**  oferecido pela **PUC-Rio**

Para tal, foi criado uma API em python, utilizando como base as bibliotecas flask e sqlalchemy. 

Essa API tem como objetivo prover ferramentas para criação de um sistema de cadastro de funcionário. 

Para interação da API com o banco e front-end, foram criadas diversas rodas, entre elas:


>**/login_cadastro** - para incluir um novo login no sistema

>**/logins** - para obter uma lista dos logins de usuário cadastrados

>**/login_validacao** - para realizar o login na interface

>**/login_excluir** - para apagar um login

>**/login_atualiza** - para alterar alterar / realizar o reset da senha e forçar o usuário a alterar a senha no próximo login

---
## Banco

Para realizar a rentenção dos dados, a API cria um banco .sqlite3, caso o mesmo não exista.

O Banco, possuio a tabela `login`, que armazena os campos de login, e-mail, senha, responsável pelo cadastro e o flag de necessidade de reset de senha

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução nas três vesões disponíveis (Sswagger, ReDoc, RapiDoc).

Para versão `Swagger` abra o link [http://localhost:5000/openapi/swagger#/](http://localhost:5000/openapi/swagger#/) no navegador
