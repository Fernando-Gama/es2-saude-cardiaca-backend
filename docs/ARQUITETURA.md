# Arquitetura do Projeto

## 1. Visão Geral

Este projeto implementa uma API REST para acompanhamento de saúde cardíaca.

A aplicação foi construída com FastAPI, SQLAlchemy e Pydantic, usando uma arquitetura em camadas para separar responsabilidades entre entrada HTTP, validação de dados, regras de negócio, acesso ao banco de dados e modelos de persistência.

Os módulos funcionais atuais são:

- Usuários;
- Autenticação;
- Medições de saúde cardíaca;
- Relatórios de saúde cardíaca.

O ponto de entrada da aplicação é:

```text
acompanhamento_cardiaco/main.py
```

Nesse arquivo, a aplicação FastAPI é criada e os routers dos módulos são registrados com o prefixo global `/v1`.

## 2. Estrutura Atual do Projeto

A estrutura principal do backend fica dentro da pasta:

```text
acompanhamento_cardiaco/
└── acompanhamento_cardiaco/
```

Estrutura resumida:

```text
acompanhamento_cardiaco/
├── acompanhamento_cardiaco/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── auth/
│   │   ├── auth_dependencies.py
│   │   ├── auth_repository.py
│   │   ├── auth_router.py
│   │   ├── auth_schemas.py
│   │   ├── auth_service.py
│   │   └── jwt_handler.py
│   ├── measurements/
│   │   ├── measurement_models.py
│   │   ├── measurement_repository.py
│   │   ├── measurement_router.py
│   │   ├── measurement_schemas.py
│   │   └── measurement_service.py
│   ├── reports/
│   │   ├── report_router.py
│   │   ├── report_schemas.py
│   │   └── report_service.py
│   └── users/
│       ├── user_models.py
│       ├── user_repository.py
│       ├── user_router.py
│       ├── user_schemas.py
│       └── user_service.py
├── tests/
├── pyproject.toml
└── poetry.lock
```

## 3. Padrão Arquitetural Adotado

O projeto usa uma arquitetura em camadas por módulo.

O padrão atual de nomes é usar o prefixo do domínio no nome dos arquivos:

```text
nome_do_modulo/
├── dominio_router.py
├── dominio_schemas.py
├── dominio_service.py
├── dominio_repository.py
└── dominio_models.py
```

Exemplo no módulo de usuários:

```text
users/
├── user_router.py
├── user_schemas.py
├── user_service.py
├── user_repository.py
└── user_models.py
```

Nem todo módulo precisa ter todas as camadas. O módulo `reports`, por exemplo, atualmente possui `report_router.py`, `report_schemas.py` e `report_service.py`, mas não possui `report_repository.py` nem `report_models.py`, porque o relatório é gerado a partir de dados já persistidos em outros módulos.

## 4. Responsabilidade de Cada Camada

### 4.1 Router

Arquivos terminados em `_router.py` definem os endpoints HTTP do módulo.

Responsabilidades principais:

- Definir rotas, métodos HTTP e status codes;
- Declarar schemas de entrada e saída;
- Receber dependências do FastAPI, como sessão de banco e usuário autenticado;
- Instanciar o service do módulo;
- Retornar a resposta HTTP adequada.

Exemplos:

- `users/user_router.py`;
- `auth/auth_router.py`;
- `measurements/measurement_router.py`;
- `reports/report_router.py`.

### 4.2 Schemas

Arquivos terminados em `_schemas.py` definem os contratos de entrada e saída da API usando Pydantic.

Responsabilidades principais:

- Validar dados recebidos nas requisições;
- Definir o formato das respostas;
- Representar mensagens de erro;
- Documentar a API automaticamente no Swagger/OpenAPI.

Exemplos:

- `users/user_schemas.py`;
- `auth/auth_schemas.py`;
- `measurements/measurement_schemas.py`;
- `reports/report_schemas.py`.

### 4.3 Service

Arquivos terminados em `_service.py` concentram as regras de negócio.

Responsabilidades principais:

- Aplicar validações específicas da aplicação;
- Coordenar chamadas ao repository;
- Gerar respostas de negócio;
- Lançar erros HTTP quando uma regra não é atendida;
- Garantir que cada usuário acesse apenas os próprios recursos quando necessário.

Exemplos de regras:

- Verificar se a senha e a confirmação de senha são iguais;
- Verificar se um e-mail já está cadastrado;
- Validar credenciais no login;
- Validar se uma medição pertence ao usuário autenticado;
- Consolidar dados para geração de relatório.

### 4.4 Repository

Arquivos terminados em `_repository.py` concentram o acesso ao banco de dados.

Responsabilidades principais:

- Buscar registros;
- Criar registros;
- Atualizar registros;
- Remover registros;
- Isolar consultas SQLAlchemy do restante da aplicação.

Exemplos:

- `users/user_repository.py`;
- `auth/auth_repository.py`;
- `measurements/measurement_repository.py`.

### 4.5 Models

Arquivos terminados em `_models.py` definem os modelos SQLAlchemy usados para representar tabelas no banco de dados.

Responsabilidades principais:

- Declarar tabelas;
- Declarar colunas;
- Declarar relacionamentos entre entidades quando necessário.

Exemplos:

- `users/user_models.py`;
- `measurements/measurement_models.py`.

## 5. Componentes Compartilhados

Além dos módulos de domínio, o projeto possui arquivos compartilhados na raiz do pacote.

### 5.1 `main.py`

Cria a instância FastAPI, define metadados da API e registra os routers:

```text
/v1/users
/v1/auth
/v1/measurements
/v1/reports
```

Também executa a criação das tabelas com:

```python
Base.metadata.create_all(bind=engine)
```

### 5.2 `database.py`

Configura o banco de dados SQLite, a engine do SQLAlchemy, a sessão `SessionLocal`, a classe base `Base` e a dependência `get_db`.

A dependência `get_db` é usada nos routers para entregar uma sessão ativa do banco durante o processamento da requisição.

### 5.3 `config.py`

Centraliza configurações da aplicação, como:

- Chave secreta;
- Algoritmo dos tokens;
- Tempo de expiração do access token;
- Tempo de expiração do refresh token.

As configurações podem ser lidas de um arquivo `.env`.

### 5.4 `security.py`

Centraliza funções de segurança relacionadas a senha:

- Geração de hash de senha;
- Verificação de senha em texto puro contra o hash armazenado.

### 5.5 `auth/jwt_handler.py`

Centraliza a criação e validação de tokens JWT.

### 5.6 `auth/auth_dependencies.py`

Define a dependência `get_current_user_id`, usada em rotas protegidas para obter o usuário autenticado a partir do token Bearer.

Atualmente, medições e relatórios dependem dessa autenticação.

## 6. Módulos da Aplicação

### 6.1 Usuários

Responsável pelo cadastro de usuários.

Arquivos principais:

```text
users/
├── user_models.py
├── user_repository.py
├── user_router.py
├── user_schemas.py
└── user_service.py
```

Endpoint atual:

```text
POST /v1/users
```

### 6.2 Autenticação

Responsável por login, renovação de tokens e suporte à autenticação JWT.

Esse módulo não possui model próprio atualmente. O `auth_repository.py` reutiliza o repositório de usuários para buscar o usuário por e-mail durante o login.

Arquivos principais:

```text
auth/
├── auth_dependencies.py
├── auth_repository.py
├── auth_router.py
├── auth_schemas.py
├── auth_service.py
└── jwt_handler.py
```

Endpoints atuais:

```text
POST /v1/auth/login
POST /v1/auth/refresh
```

### 6.3 Medições

Responsável pelo cadastro, listagem, busca, atualização e remoção de medições cardíacas.

Arquivos principais:

```text
measurements/
├── measurement_models.py
├── measurement_repository.py
├── measurement_router.py
├── measurement_schemas.py
└── measurement_service.py
```

Endpoints atuais:

```text
POST   /v1/measurements
GET    /v1/measurements
GET    /v1/measurements/{id_medicao}
PUT    /v1/measurements/{id_medicao}
DELETE /v1/measurements/{id_medicao}
```

Todas essas rotas exigem autenticação via token Bearer.

### 6.4 Relatórios

Responsável por gerar relatórios consolidados de saúde cardíaca a partir das medições do usuário autenticado.

Arquivos principais:

```text
reports/
├── report_router.py
├── report_schemas.py
└── report_service.py
```

Endpoint atual:

```text
GET /v1/reports/heart-health
```

Essa rota aceita filtros opcionais por período:

```text
dataInicial
dataFinal
```

A rota exige autenticação via token Bearer.

## 7. Fluxo Padrão de uma Requisição

O fluxo geral de uma requisição segue este padrão:

```text
Cliente
   ↓
FastAPI / main.py
   ↓
router do módulo
   ↓
schemas / Pydantic
   ↓
service do módulo
   ↓
repository do módulo
   ↓
database.py / SQLAlchemy
   ↓
banco de dados SQLite
```

Na resposta, o fluxo retorna:

```text
banco de dados SQLite
   ↑
database.py / SQLAlchemy
   ↑
repository do módulo
   ↑
service do módulo
   ↑
router do módulo
   ↑
FastAPI
   ↑
Cliente
```

Em rotas protegidas, existe uma etapa adicional de autenticação:

```text
Token Bearer
   ↓
auth_dependencies.py
   ↓
jwt_handler.py
   ↓
id do usuário autenticado
   ↓
service do módulo
```

## 8. Exemplo de Fluxo: Cadastro de Usuário

Fluxo do endpoint `POST /v1/users`:

```text
Cliente envia dados de cadastro
   ↓
user_router.py recebe a requisição
   ↓
user_schemas.py valida os dados com Pydantic
   ↓
user_service.py aplica regras de negócio
   ↓
user_repository.py consulta e salva no banco
   ↓
user_models.py representa a tabela de usuários
   ↓
database.py fornece a sessão SQLAlchemy
   ↓
SQLite persiste o usuário
```

A resposta retorna ao cliente com status HTTP `201 Created` em caso de sucesso.

## 9. Exemplo de Fluxo: Medição Autenticada

Fluxo do endpoint `POST /v1/measurements`:

```text
Cliente envia token Bearer e dados da medição
   ↓
measurement_router.py recebe a requisição
   ↓
auth_dependencies.py valida o token
   ↓
jwt_handler.py decodifica o JWT
   ↓
measurement_schemas.py valida os dados da medição
   ↓
measurement_service.py aplica regras de negócio
   ↓
measurement_repository.py salva a medição
   ↓
measurement_models.py representa a tabela de medições
   ↓
SQLite persiste a medição vinculada ao usuário
```

## 10. Testes

Os testes ficam na pasta:

```text
acompanhamento_cardiaco/tests/
```

Estrutura atual:

```text
tests/
├── auth/
│   └── test_auth_service.py
├── integration/
│   └── test_api.py
├── measurements/
│   └── test_measurement_service.py
├── reports/
│   └── test_report_service.py
└── users/
    └── test_user_service.py
```

Os testes de service validam regras de negócio isoladas por módulo. Os testes de integração validam o comportamento da API em conjunto.

## 11. Convenções Para Novos Módulos

Novos módulos devem seguir o padrão atual de organização:

```text
novo_modulo/
├── novo_modulo_router.py
├── novo_modulo_schemas.py
├── novo_modulo_service.py
├── novo_modulo_repository.py
└── novo_modulo_models.py
```

Quando o módulo não precisar de persistência própria, as camadas `repository` e `models` podem ser omitidas, como acontece atualmente no módulo `reports`.

Também é recomendado:

- Registrar o router em `main.py` com prefixo `/v1`;
- Usar `get_db` quando a rota precisar acessar o banco;
- Usar `get_current_user_id` quando a rota precisar de autenticação;
- Criar testes de service para regras de negócio;
- Criar testes de integração quando houver mudança em endpoints.

## 12. Considerações Finais

A arquitetura atual busca manter o backend modular, organizado e fácil de evoluir.

A separação entre router, schema, service, repository e model reduz acoplamento, facilita testes e deixa mais claro onde cada tipo de regra deve ficar.

Essa padronização também ajuda novos integrantes do projeto a entender rapidamente onde implementar endpoints, validações, regras de negócio e persistência.
