# API para gerenciamento de contas de usuários

Esse projeto apresenta o MVP de requisido para conclusão da sprint 3 da curso de  **Engenharia de Softaware**  oferecido pela **PUC-Rio**

Para tal, foi criado uma API em python, utilizando como base as bibliotecas flask e sqlalchemy. 

Essa API tem como objetivo prover ferramentas para criação de um sistema de cadastro de usuários. 

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

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Caso não exita, crie uma interface de rede para servir de ponte entre os outros container

```
$ docker network create --driver=bridge minha-rede
```
Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t api-login .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -d --name=api_login_ip --network=minha-rede -p 5000:5000 api-login
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador.
