# API de Acompanhamento de Saúde Cardíaca

Back-end de uma API REST para acompanhamento de saúde cardíaca. O sistema permite cadastrar usuários, autenticar por credenciais, registrar medições cardíacas e gerar relatórios com histórico, médias e alertas.

## Links úteis

- Repositório Git: <https://github.com/Fernando-Gama/es2-saude-cardiaca-backend>
- Swagger local: <http://localhost:8000/docs>
- OpenAPI/Swagger JSON: [docs/swagger/swagger.json](docs/swagger/swagger.json)
- Arquitetura: [docs/ARQUITETURA.md](docs/ARQUITETURA.md)
- Roteiro de apresentação: [docs/ROTEIRO_APRESENTACAO.md](docs/ROTEIRO_APRESENTACAO.md)
- Setup Linux: [docs/LINUX_ENVIRONMENT_SETUP.md](docs/LINUX_ENVIRONMENT_SETUP.md)
- Setup Windows: [docs/WINDOWS_ENVIRONMENT_SETUP.md](docs/WINDOWS_ENVIRONMENT_SETUP.md)

## Entregáveis

- Link do repositório no Git:
  <https://github.com/Fernando-Gama/es2-saude-cardiaca-backend>
- Link da documentação da API:
  <http://localhost:8000/docs>
- Arquivo OpenAPI versionado:
  [docs/swagger/swagger.json](docs/swagger/swagger.json)
- Explicação da arquitetura e descrição da modularização:
  [docs/ARQUITETURA.md](docs/ARQUITETURA.md)
- Roteiro para demonstração do sistema, testes, estrutura e Swagger:
  [docs/ROTEIRO_APRESENTACAO.md](docs/ROTEIRO_APRESENTACAO.md)

## Funcionalidades

- Cadastro de usuários.
- Login com e-mail e senha.
- Autenticação com Bearer token.
- Renovação de tokens com refresh token.
- Cadastro, listagem, busca, atualização e remoção de medições cardíacas.
- Vínculo das medições ao usuário autenticado.
- Relatório de saúde cardíaca com médias, histórico e alertas.

## Tecnologias

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Passlib
- Poetry
- Taskipy
- Pytest
- Ruff

## Estrutura do repositório

```text
.
├── acompanhamento_cardiaco/
│   ├── acompanhamento_cardiaco/
│   │   ├── auth/
│   │   ├── measurements/
│   │   ├── reports/
│   │   ├── users/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── security.py
│   ├── tests/
│   ├── pyproject.toml
│   └── poetry.lock
├── docs/
│   ├── postman/
│   ├── swagger/
│   ├── ARQUITETURA.md
│   └── ROTEIRO_APRESENTACAO.md
├── LICENSE
└── README.md
```

## Como executar

Entre na pasta do projeto Python:

```bash
cd acompanhamento_cardiaco
```

Instale as dependências:

```bash
poetry install
```

Execute a API:

```bash
poetry run task run
```

Ou execute diretamente com FastAPI:

```bash
poetry run fastapi dev acompanhamento_cardiaco/main.py
```

A API ficará disponível em:

```text
http://localhost:8000
```

A documentação Swagger ficará disponível em:

```text
http://localhost:8000/docs
```

A especificação OpenAPI exportada também está versionada em:

```text
docs/swagger/swagger.json
```

Esse arquivo pode ser aberto em ferramentas compatíveis com OpenAPI, como o
Swagger Editor.

## Teste de serviços com Postman

A pasta [docs/postman](docs/postman) contém os arquivos usados para demonstrar a
API em uma ferramenta de teste de serviços:

- `API_Acompanhamento_Cardiaco_Roteiro_Apresentacao.postman_collection.json`
- `Local_Saude_Cardiaca_Apresentacao.postman_environment.json`

Para usar no Postman:

1. Importe a collection.
2. Importe o environment local.
3. Execute a API em `http://127.0.0.1:8000`.
4. Selecione o environment `Local - Saúde Cardíaca - Apresentação`.
5. Execute as requisições na ordem do roteiro.

A collection cobre o fluxo principal da apresentação:

- criar conta;
- fazer login;
- salvar o token no environment;
- cadastrar medição;
- listar, buscar, atualizar e remover medição;
- gerar relatório de saúde cardíaca;
- renovar token;
- demonstrar cenários de erro.

## Configurações

As configurações de autenticação podem ser definidas por variáveis de ambiente ou por um arquivo `.env` dentro da pasta `acompanhamento_cardiaco/`.

Exemplo:

```env
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Caso nenhuma chave seja configurada, o projeto usa valores padrão de desenvolvimento.

## Principais endpoints

### Usuários

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/v1/users` | Cria uma conta de usuário |

### Autenticação

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/v1/auth/login` | Autentica usuário e retorna tokens |
| POST | `/v1/auth/refresh` | Renova os tokens |

### Medições cardíacas

As rotas de medições exigem o header:

```http
Authorization: Bearer <access_token>
```

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/v1/measurements` | Cadastra uma medição |
| GET | `/v1/measurements` | Lista medições do usuário autenticado |
| GET | `/v1/measurements/{id_medicao}` | Busca uma medição do usuário |
| PUT | `/v1/measurements/{id_medicao}` | Atualiza uma medição do usuário |
| DELETE | `/v1/measurements/{id_medicao}` | Remove uma medição do usuário |

### Relatórios

A rota de relatório exige o header:

```http
Authorization: Bearer <access_token>
```

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/v1/reports/heart-health` | Gera relatório de saúde cardíaca |

O relatório aceita filtros opcionais por período:

```text
GET /v1/reports/heart-health?dataInicial=2026-06-01&dataFinal=2026-06-30
```

## Arquitetura

O projeto usa arquitetura em camadas por módulo:

```text
Cliente
  -> Router
  -> Schema / Pydantic
  -> Service
  -> Repository
  -> Banco de dados
```

Responsabilidades principais:

- `router`: define endpoints HTTP, status codes e dependências.
- `schemas`: define contratos de entrada e saída da API.
- `service`: concentra regras de negócio.
- `repository`: isola o acesso ao banco de dados.
- `models`: representa tabelas do banco com SQLAlchemy.

Mais detalhes estão em [docs/ARQUITETURA.md](docs/ARQUITETURA.md).

## Testes e qualidade

Execute os testes:

```bash
cd acompanhamento_cardiaco
poetry run task test
```

Execute o lint:

```bash
cd acompanhamento_cardiaco
poetry run task lint
```

Formate o código:

```bash
cd acompanhamento_cardiaco
poetry run task format
```

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
