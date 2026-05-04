# Configuração do Ambiente

Este documento explica como configurar o ambiente de desenvolvimento do projeto **API de Acompanhamento de Saúde Cardíaca**.

A ideia é que qualquer pessoa consiga clonar o repositório, instalar as dependências e executar o projeto localmente.

O projeto utiliza:

- Python 3.13 ou superior
- pipx
- Poetry
- Taskipy
- Ruff
- Pytest
- FastAPI

O `pipx` será usado para instalar o Poetry de forma isolada.

O Poetry será usado para:

- instalar ou selecionar a versão do Python usada no projeto;
- criar o ambiente virtual;
- instalar as dependências;
- executar comandos dentro do ambiente virtual;
- gerenciar as dependências no `pyproject.toml`.

---

## 1. Requisitos

Antes de executar o projeto, é necessário ter instalado:

- `git`
- `pipx`
- `Poetry`

A versão do Python exigida pelo projeto está definida no arquivo `pyproject.toml`:

```toml
[project]
requires-python = ">=3.13,<4.0"
```

Portanto, o projeto deve ser executado com Python 3.13 ou superior, respeitando o limite definido no `pyproject.toml`.

Neste projeto, a instalação do Python pode ser feita pelo próprio Poetry, desde que a versão instalada tenha suporte ao comando:

```bash
poetry python install
```

---

## 2. Instalando o pipx

O `pipx` serve para instalar ferramentas Python de linha de comando em ambientes isolados.

Neste projeto, ele será usado para instalar o Poetry.

No Ubuntu, instale com:

```bash
sudo apt update
sudo apt install pipx
```

Depois, garanta que o diretório do `pipx` esteja no `PATH`:

```bash
pipx ensurepath
```

Feche e abra o terminal novamente.

Para verificar se a instalação funcionou:

```bash
pipx --version
```

---

## 3. Instalando o Poetry com pipx

Com o `pipx` instalado, instale o Poetry:

```bash
pipx install poetry
```

Verifique se o Poetry foi instalado corretamente:

```bash
poetry --version
```

O Poetry é parecido com o Maven no Java, pois permite gerenciar o projeto, suas dependências e seu ambiente de execução.

Caso o comando `poetry python install` não esteja disponível, atualize o Poetry:

```bash
pipx upgrade poetry
```

---

## 4. Clonando o projeto

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bash
cd acompanhamento-cardiaco
```

Caso o nome da pasta seja diferente, entre na pasta correta do repositório clonado.

---

## 5. Configurando o ambiente virtual dentro do projeto

Para facilitar a configuração do VS Code, é recomendado criar o ambiente virtual dentro da pasta do projeto.

Execute:

```bash
poetry config virtualenvs.in-project true --local
```

Esse comando faz com que o ambiente virtual seja criado na pasta:

```bash
.venv/
```

Essa pasta não deve ser enviada para o Git.

---

## 6. Instalando o Python 3.13 pelo Poetry

Este projeto usa Python 3.13 ou superior.

Para instalar o Python 3.13 pelo Poetry, execute:

```bash
poetry python install 3.13
```

Depois, verifique as versões de Python disponíveis para o Poetry:

```bash
poetry python list
```

Agora configure o projeto para usar o Python 3.13:

```bash
poetry env use 3.13
```

Caso o comando acima não encontre o Python, tente usar o executável diretamente:

```bash
poetry env use python3.13
```

Para verificar o ambiente criado pelo Poetry:

```bash
poetry env info
```

Para ver o caminho exato do Python usado no ambiente virtual:

```bash
poetry env info --executable
```

---

## 7. Instalando as dependências do projeto

Dentro da pasta do projeto, execute:

```bash
poetry install
```

Esse comando instala as dependências definidas no `pyproject.toml` e cria o ambiente virtual do projeto.

As dependências principais do projeto ficam na seção:

```toml
[project]
dependencies = [
    "fastapi[standard] (>=0.136.1,<0.137.0)"
]
```

As dependências de desenvolvimento ficam na seção:

```toml
[dependency-groups]
dev = [
    "ruff (>=0.15.12,<0.16.0)",
    "pytest (>=9.0.3,<10.0.0)",
    "pytest-cov (>=7.1.0,<8.0.0)",
    "taskipy (>=1.14.1,<2.0.0)"
]
```

---

## 8. Ativando o ambiente virtual do Poetry

Existem duas formas de executar comandos dentro do ambiente virtual do Poetry.

### Opção 1: Usar `poetry run`

Essa opção executa um comando dentro do ambiente virtual sem precisar ativá-lo manualmente.

Exemplo:

```bash
poetry run task run
```

---

### Opção 2: Ativar o ambiente virtual

Para ativar o ambiente virtual no terminal, use:

```bash
eval $(poetry env activate)
```

Depois disso, você pode executar os comandos diretamente:

```bash
task run
task test
task lint
```

Para sair do ambiente virtual:

```bash
deactivate
```

---

## 9. Executando o projeto

Para rodar a aplicação FastAPI em modo de desenvolvimento:

```bash
poetry run task run
```

Esse comando executa a task `run`, definida no `pyproject.toml`:

```toml
run = "fastapi dev acompanhamento_cardiaco/main.py"
```

Ou seja, ele executa internamente:

```bash
fastapi dev acompanhamento_cardiaco/main.py
```

Depois de iniciar o servidor, a documentação automática da API fica disponível em:

```text
http://127.0.0.1:8000/docs
```

---

## 10. Comandos disponíveis com Taskipy

O projeto utiliza o Taskipy para criar atalhos de comandos.

As tasks podem ser configuradas no arquivo `pyproject.toml` da seguinte forma:

```toml
[tool.taskipy.tasks]
lint = "ruff check"
pre_format = "ruff check --fix"
format = "ruff format"
run = "fastapi dev acompanhamento_cardiaco/main.py"
pre_test = "task lint"
test = "pytest -s -x --cov=acompanhamento_cardiaco -vv"
post_test = "coverage html"
```

---

### `task run`

Executa a aplicação FastAPI em modo de desenvolvimento:

```bash
poetry run task run
```

Internamente executa:

```bash
fastapi dev acompanhamento_cardiaco/main.py
```

---

### `task lint`

Verifica problemas no código usando o Ruff:

```bash
poetry run task lint
```

Internamente executa:

```bash
ruff check
```

Esse comando aponta problemas de estilo, imports, erros simples e regras configuradas no Ruff.

---

### `task format`

Formata o código usando o Ruff:

```bash
poetry run task format
```

Antes de executar o `format`, o Taskipy executa automaticamente a task `pre_format`:

```toml
pre_format = "ruff check --fix"
```

Ou seja, ao rodar:

```bash
poetry run task format
```

O Taskipy executa primeiro:

```bash
ruff check --fix
```

Depois executa:

```bash
ruff format
```

Na prática, esse comando tenta corrigir problemas automaticamente e depois formata o código.

---

### `task test`

Executa os testes do projeto:

```bash
poetry run task test
```

Antes de executar os testes, o Taskipy executa automaticamente a task `pre_test`:

```toml
pre_test = "task lint"
```

Ou seja, antes dos testes, ele roda:

```bash
task lint
```

Depois executa:

```bash
pytest -s -x --cov=acompanhamento_cardiaco -vv
```

Esse comando faz o seguinte:

- `pytest`: executa os testes;
- `-s`: permite mostrar saídas no terminal, como `print`;
- `-x`: para a execução no primeiro erro;
- `--cov=acompanhamento_cardiaco`: calcula a cobertura de testes do pacote principal do projeto;
- `-vv`: mostra uma saída mais detalhada dos testes.

Depois dos testes, o Taskipy executa automaticamente a task `post_test`:

```toml
post_test = "coverage html"
```

Esse comando gera um relatório HTML de cobertura de testes.

O relatório fica na pasta:

```bash
htmlcov/
```

Para abrir o relatório, acesse o arquivo:

```bash
htmlcov/index.html
```

---

## 11. Executando comandos sem Taskipy

Também é possível executar os comandos diretamente, sem usar o Taskipy.

Rodar o projeto:

```bash
poetry run fastapi dev acompanhamento_cardiaco/main.py
```

Rodar o lint:

```bash
poetry run ruff check
```

Formatar o código:

```bash
poetry run ruff check --fix
poetry run ruff format
```

Rodar os testes:

```bash
poetry run pytest -s -x --cov=acompanhamento_cardiaco -vv
```

Gerar relatório HTML de cobertura:

```bash
poetry run coverage html
```

---

## 12. Configurando o VS Code

Caso o VS Code não reconheça as bibliotecas instaladas pelo Poetry, descubra o caminho do Python do ambiente virtual:

```bash
poetry env info --executable
```

Depois, no VS Code:

1. Pressione `Ctrl + Shift + P`
2. Procure por `Python: Select Interpreter`
3. Escolha o interpretador retornado pelo comando acima

Como o ambiente virtual foi configurado para ficar dentro do projeto, o caminho esperado é:

```bash
.venv/bin/python
```

Também é possível criar o arquivo `.vscode/settings.json` para configurar o interpretador automaticamente no VS Code:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "editor.formatOnSave": true,
  "ruff.enable": true
}
```

A pasta `.vscode/` pode ser versionada quando as configurações forem úteis para todo o grupo.

---

## 13. Arquivos que devem ser versionados

Os arquivos abaixo devem ser enviados para o Git:

- `pyproject.toml`
- `poetry.lock`
- `README.md`
- `docs/CONFIGURACAO_AMBIENTE.md`
- `acompanhamento_cardiaco/`
- `tests/`
- `.vscode/settings.json`, caso o grupo queira padronizar o VS Code

O arquivo `poetry.lock` é importante porque registra as versões exatas das dependências instaladas.

Isso ajuda a garantir que outra pessoa consiga instalar o projeto com as mesmas versões.

---

## 14. Arquivos que não devem ser versionados

Os arquivos abaixo não devem ser enviados para o Git:

- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.ruff_cache/`
- `htmlcov/`
- `.coverage`
- `.env`

Exemplo de `.gitignore`:

```gitignore
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
htmlcov/
.coverage
.env
```

---

## 15. Docker

Caso o projeto utilize Docker futuramente, esta seção deve explicar:

- como construir a imagem;
- como subir os containers;
- como parar os containers;
- quais serviços são usados, como banco de dados ou backend.

Exemplo para subir os containers:

```bash
docker compose up --build
```

Exemplo para parar os containers:

```bash
docker compose down
```

---

## 16. Resumo dos principais comandos

Instalar o pipx:

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
```

Instalar o Poetry:

```bash
pipx install poetry
```

Atualizar o Poetry:

```bash
pipx upgrade poetry
```

Configurar ambiente virtual dentro do projeto:

```bash
poetry config virtualenvs.in-project true --local
```

Instalar o Python 3.13 pelo Poetry:

```bash
poetry python install 3.13
```

Configurar o projeto para usar Python 3.13:

```bash
poetry env use 3.13
```

Instalar dependências:

```bash
poetry install
```

Rodar aplicação:

```bash
poetry run task run
```

Rodar lint:

```bash
poetry run task lint
```

Formatar código:

```bash
poetry run task format
```

Rodar testes:

```bash
poetry run task test
```

Ativar ambiente virtual:

```bash
eval $(poetry env activate)
```

Sair do ambiente virtual:

```bash
deactivate
```