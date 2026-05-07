# Arquitetura do Projeto

## 1. Visão Geral

Este projeto implementa uma API REST para acompanhamento de saúde cardíaca, conforme especificado no contrato OpenAPI/Swagger da aplicação.

A API possui diferentes módulos funcionais, como:

- Usuários;
- Autenticação;
- Medições de saúde cardíaca;
- Relatórios progressivos.

Para manter o projeto organizado, foi adotada uma arquitetura em camadas. Essa arquitetura será usada como padrão para todos os módulos da aplicação.

O primeiro módulo implementado será o módulo de usuários, responsável pelo endpoint de cadastro:

POST /v1/users

## 2. Padrão Arquitetural Adotado

O projeto utiliza uma arquitetura em camadas, separando responsabilidades entre rotas, validação de dados, regras de negócio, persistência e modelos de banco de dados.

Cada módulo da aplicação seguirá a seguinte estrutura:

```text
app/
└── nome_do_modulo/
    ├── router.py
    ├── schemas.py
    ├── service.py
    ├── repository.py
    └── models.py
```
Exemplo no módulo de usuários:

```text
app/
└── users/
    ├── router.py
    ├── schemas.py
    ├── service.py
    ├── repository.py
    └── models.py
```

## 3. Responsabilidade de Cada Camada

### 3.1 Router

A camada `router.py` é responsável por definir os endpoints HTTP do módulo.

Ela recebe as requisições da API, define os métodos HTTP, configura os status codes e chama a camada de serviço responsável pela regra de negócio.

Essa camada não deve conter regra de negócio complexa.

Exemplo de responsabilidade:

- Definir `POST /v1/users`;
- Receber os dados da requisição;
- Chamar o serviço de cadastro;
- Retornar a resposta HTTP adequada.

## 3.2 Schemas

A camada `schemas.py` é responsável por definir os contratos de entrada e saída da API utilizando Pydantic.

Ela representa os dados que entram e saem da aplicação.

Essa camada valida dados como:

- Campos obrigatórios;
- Tipos de dados;
- Formato de e-mail;
- Formato de datas;
- Valores permitidos;
- Tamanho mínimo e máximo de campos.

No módulo de usuários, por exemplo, os schemas representam:

- Dados necessários para cadastrar um usuário;
- Dados retornados após o cadastro;
- Estrutura de erro da API.

## 3.3 Service

A camada `service.py` concentra as regras de negócio do módulo.

Ela recebe dados já validados pelos schemas e executa as validações específicas da aplicação.

Essa camada pode verificar regras como:

- Se uma senha e sua confirmação são iguais;
- Se um e-mail já está cadastrado;
- Se um usuário existe;
- Se uma medição pertence a determinado usuário;
- Se um relatório pode ser gerado.

A camada de serviço também coordena o fluxo entre os dados recebidos, o repositório e a resposta final.

## 3.4 Repository

A camada `repository.py` é responsável pelo acesso ao banco de dados.

Ela isola a lógica de persistência, evitando que o restante da aplicação dependa diretamente de consultas SQL ou comandos do ORM.

Essa camada pode conter métodos como:

- Buscar por ID;
- Buscar por e-mail;
- Listar registros;
- Salvar;
- Atualizar;
- Remover.

O objetivo é deixar a regra de negócio separada da forma como os dados são armazenados.

## 3.5 Models

A camada `models.py` define os modelos do banco de dados utilizando SQLAlchemy.

Esses modelos representam as tabelas da aplicação.

No módulo de usuários, por exemplo, o model representa a tabela de usuários.

Nos próximos módulos, poderão existir models como:

- Measurement;
- ProgressiveReport;
- AuthToken;
- UserSession.

## 4. Fluxo Padrão de uma Requisição

O fluxo geral de uma requisição na aplicação segue o seguinte padrão:

Cliente
   ↓
router.py
   ↓
schemas.py / Pydantic
   ↓
service.py
   ↓
repository.py
   ↓
banco de dados

Na resposta, o fluxo retorna:

banco de dados
   ↑
repository.py
   ↑
service.py
   ↑
router.py
   ↑
cliente

## 5. Exemplo no Módulo de Usuários

No cadastro de usuário, o fluxo será:

POST /v1/users
   ↓
router.py recebe a requisição
   ↓
Pydantic valida os dados usando schemas.py
   ↓
service.py aplica as regras de negócio
   ↓
repository.py salva os dados no banco
   ↓
banco de dados persiste o usuário

A resposta retorna ao cliente com status HTTP 201 em caso de sucesso.

## 6. Justificativa da Arquitetura

A arquitetura em camadas foi escolhida para organizar melhor o código e separar responsabilidades.

Com essa divisão, cada parte do sistema possui uma função clara:

- O `router` cuida da comunicação HTTP;
- O `schema` define e valida os dados da API;
- O `service` concentra as regras de negócio;
- O `repository` acessa o banco de dados;
- O `model` representa as tabelas do banco.

Essa separação facilita a manutenção, pois alterações em uma camada tendem a ter menor impacto nas outras.

Também facilita a criação de testes, já que as regras de negócio podem ser testadas separadamente da API e do banco de dados.

Além disso, permite que novos módulos sigam o mesmo padrão, mantendo consistência em todo o projeto.

## 7. Aplicação da Arquitetura nos Próximos Módulos

Os próximos módulos da API devem seguir a mesma estrutura.

Por exemplo, o módulo de medições poderá ser organizado assim:

```text
app/
└── measurements/
    ├── router.py
    ├── schemas.py
    ├── service.py
    ├── repository.py
    └── models.py
```

O módulo de relatórios poderá seguir a mesma ideia:

```text
app/
└── reports/
    ├── router.py
    ├── schemas.py
    ├── service.py
    ├── repository.py
    └── models.py
```

E o módulo de autenticação:

```text
app/
└── auth/
    ├── router.py
    ├── schemas.py
    ├── service.py
    ├── repository.py
    └── models.py
```

Dessa forma, todos os módulos terão uma organização parecida, facilitando o entendimento do projeto por qualquer integrante do grupo.

## 8. Considerações Finais

A arquitetura adotada busca deixar o projeto mais modular, organizado e fácil de evoluir.

Embora a primeira funcionalidade implementada seja o cadastro de usuários, a mesma estrutura poderá ser reutilizada nos demais módulos da aplicação.

Essa padronização torna o desenvolvimento mais consistente e reduz a complexidade conforme novas funcionalidades forem adicionadas.