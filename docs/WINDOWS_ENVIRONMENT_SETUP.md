# Configuração do Ambiente no Windows

Este documento explica como configurar o ambiente de desenvolvimento do projeto **API de Acompanhamento de Saúde Cardíaca** no Windows.

A ideia é que qualquer pessoa consiga clonar o repositório, instalar as dependências e executar o projeto localmente.

O projeto utiliza:

- Python 3.13 ou superior
- pipx
- Poetry
- Taskipy
- Ruff
- Pytest
- FastAPI
- VS Code

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

Neste projeto, a instalação do Python usado pela aplicação pode ser feita pelo próprio Poetry, por meio do comando:

```powershell
poetry python install 3.13
```

> Observação: para instalar o `pipx` e o `Poetry`, o Windows precisa ter pelo menos uma instalação inicial do Python. Depois disso, o Python usado pelo projeto pode ser instalado pelo próprio Poetry.

---

## 2. Possível aviso sobre PATH

Durante a instalação do `pipx` ou do `Poetry`, pode aparecer uma mensagem dizendo que a ferramenta foi adicionada ao `PATH`, mas que é necessário fechar e abrir o terminal novamente.

Exemplo:

```text
You will need to open a new terminal or re-login for the PATH changes to take effect.
```

Caso isso aconteça, feche o CMD ou PowerShell, abra novamente e continue a configuração a partir do próximo comando.

---

## 3. Instalando o Git

Instale o Git pelo site oficial:

```text
https://git-scm.com/downloads
```

Após instalar, abra o CMD ou PowerShell e verifique:

```bat
git --version
```

---

## 4. Instalando o pipx

Para instalar o `pipx`, execute:

```bat
py -m pip install --user pipx
```

Depois, garanta que o `pipx` esteja no `PATH`:

```bat
py -m pipx ensurepath
```

Feche e abra o terminal novamente.

Para verificar se funcionou:

```bat
pipx --version
```

---

## 5. Instalando o Poetry

Com o `pipx` instalado, instale o Poetry:

```bat
pipx install poetry
```

Verifique se o Poetry foi instalado corretamente:

```bat
poetry --version
```

Caso precise atualizar o Poetry:

```bat
pipx upgrade poetry
```

---

## 6. Clonando o projeto

Escolha uma pasta para guardar seus projetos.

Exemplo:

```bat
cd %USERPROFILE%\Documents
```

Clone o repositório:

```bat
git clone URL_DO_REPOSITORIO
```

Entre na pasta do projeto:

```bat
cd es2-saude-cardiaca-backend\acompanhamento_cardiaco
```

Caso o nome da pasta seja diferente, entre na pasta que contém o arquivo `pyproject.toml`.

---

## 7. Configurando o ambiente virtual dentro do projeto

Para facilitar a configuração do VS Code, é recomendado criar o ambiente virtual dentro da pasta do projeto.

Execute:

```bat
poetry config virtualenvs.in-project true --local
```

Esse comando faz com que o ambiente virtual seja criado na pasta:

```text
.venv/
```

No Windows, o Python do ambiente virtual ficará em:

```text
.venv\Scripts\python.exe
```

Essa pasta não deve ser enviada para o Git.

---

## 8. Instalando o Python 3.13 pelo Poetry

Este projeto usa Python 3.13 ou superior.

Para instalar o Python 3.13 pelo Poetry, execute:

```bat
poetry python install 3.13
```

Depois, verifique as versões de Python disponíveis para o Poetry:

```bat
poetry python list
```

Agora configure o projeto para usar o Python 3.13:

```bat
poetry env use 3.13
```

Caso o comando acima não encontre o Python, veja o caminho do Python instalado pelo Poetry:

```bat
poetry python list
```

Depois use o caminho completo:

```bat
poetry env use CAMINHO_DO_PYTHON
```

Para verificar o ambiente criado pelo Poetry:

```bat
poetry env info
```

Para ver o caminho exato do Python usado no ambiente virtual:

```bat
poetry env info --executable
```

O caminho esperado será parecido com:

```text
C:\caminho\para\es2-saude-cardiaca-backend\acompanhamento_cardiaco\.venv\Scripts\python.exe
```

---

## 9. Instalando as dependências do projeto

Dentro da pasta que contém o arquivo `pyproject.toml`, execute:

```bat
poetry install
```

Esse comando instala as dependências definidas no `pyproject.toml` e cria o ambiente virtual do projeto.

As dependências principais do projeto ficam na seção:

```toml
[project]
dependencies = [
    "fastapi[standard] (>=0.136.1,<0.137.0)",
    "sqlalchemy (>=2.0.49,<3.0.0)",
    "passlib (>=1.7.4,<2.0.0)"
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

## 10. Ativando o ambiente virtual no CMD

Para ativar o ambiente virtual no CMD, entre na raiz do projeto e execute:

```bat
.venv\Scripts\activate.bat
```

Se deu certo, o terminal ficará parecido com:

```text
(.venv) C:\caminho\para\es2-saude-cardiaca-backend\acompanhamento_cardiaco>
```

Depois disso, você pode executar comandos diretamente:

```bat
task run
task test
task lint
```

Para sair do ambiente virtual:

```bat
deactivate
```

---

## 11. Ativando o ambiente virtual no PowerShell

Para ativar o ambiente virtual no PowerShell, execute:

```powershell
.venv\Scripts\Activate.ps1
```

Caso apareça um erro parecido com:

```text
cannot be loaded because running scripts is disabled on this system
```

Execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente ativar novamente:

```powershell
.venv\Scripts\Activate.ps1
```

Para sair do ambiente virtual:

```powershell
deactivate
```

---

## 12. Executando comandos sem ativar a `.venv`

Também é possível executar os comandos sem ativar o ambiente virtual.

Para isso, use `poetry run`.

Exemplo:

```bat
poetry run task run
```

Essa é uma forma segura de garantir que o comando será executado dentro do ambiente virtual correto.

---

## 13. Executando o projeto

Para rodar a aplicação FastAPI em modo de desenvolvimento:

```bat
poetry run task run
```

Esse comando executa a task `run`, definida no `pyproject.toml`:

```toml
run = "fastapi dev acompanhamento_cardiaco/main.py"
```

Ou seja, ele executa internamente:

```bat
fastapi dev acompanhamento_cardiaco/main.py
```

Depois de iniciar o servidor, a documentação automática da API fica disponível em:

```text
http://127.0.0.1:8000/docs
```

---

## 14. Comandos disponíveis com Taskipy

O projeto utiliza o Taskipy para criar atalhos de comandos.

As tasks podem ser configuradas no arquivo `pyproject.toml` da seguinte forma:

```toml
[tool.taskipy.tasks]
lint = "ruff check ."
pre_format = "ruff check . --fix"
format = "ruff format ."
run = "fastapi dev acompanhamento_cardiaco/main.py"
pre_test = "task lint"
test = "pytest -s -x --cov=acompanhamento_cardiaco -vv"
post_test = "coverage html"
```

---

### `task run`

Executa a aplicação FastAPI em modo de desenvolvimento:

```bat
poetry run task run
```

Internamente executa:

```bat
fastapi dev acompanhamento_cardiaco/main.py
```

---

### `task lint`

Verifica problemas no código usando o Ruff:

```bat
poetry run task lint
```

Internamente executa:

```bat
ruff check .
```

Esse comando aponta problemas de estilo, imports, erros simples e regras configuradas no Ruff.

---

### `task format`

Formata o código usando o Ruff:

```bat
poetry run task format
```

Antes de executar o `format`, o Taskipy executa automaticamente a task `pre_format`:

```toml
pre_format = "ruff check . --fix"
```

Ou seja, ao rodar:

```bat
poetry run task format
```

O Taskipy executa primeiro:

```bat
ruff check . --fix
```

Depois executa:

```bat
ruff format .
```

Na prática, esse comando tenta corrigir problemas automaticamente e depois formata o código.

---

### `task test`

Executa os testes do projeto:

```bat
poetry run task test
```

Antes de executar os testes, o Taskipy executa automaticamente a task `pre_test`:

```toml
pre_test = "task lint"
```

Ou seja, antes dos testes, ele roda:

```bat
task lint
```

Depois executa:

```bat
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

```text
htmlcov/
```

Para abrir o relatório no Windows, execute:

```bat
start htmlcov\index.html
```

---

## 15. Executando comandos sem Taskipy

Também é possível executar os comandos diretamente, sem usar o Taskipy.

Rodar o projeto:

```bat
poetry run fastapi dev acompanhamento_cardiaco/main.py
```

Rodar o lint:

```bat
poetry run ruff check .
```

Formatar o código:

```bat
poetry run ruff check . --fix
poetry run ruff format .
```

Rodar os testes:

```bat
poetry run pytest -s -x --cov=acompanhamento_cardiaco -vv
```

Gerar relatório HTML de cobertura:

```bat
poetry run coverage html
```

Abrir relatório HTML:

```bat
start htmlcov\index.html
```

---

## 16. Configurando o VS Code

Para configurar o VS Code, crie o arquivo `.vscode/settings.json` na pasta que contém o `pyproject.toml`.

Esse arquivo configura o editor para usar o Python da `.venv` do projeto.

O conteúdo esperado é:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": [
    "tests"
  ],
  "editor.formatOnSave": true,
  "ruff.enable": true
}
```

Caso o VS Code não reconheça automaticamente o interpretador, descubra o caminho do Python do ambiente virtual:

```bat
poetry env info --executable
```

Ou, com a `.venv` ativada:

```bat
where python
```

Depois, no VS Code:

1. Pressione `Ctrl + Shift + P`
2. Procure por `Python: Select Interpreter`
3. Escolha o interpretador da `.venv`

O caminho esperado é:

```text
.venv\Scripts\python.exe
```

---

## 17. Como descobrir o caminho da `.venv`

Com o ambiente virtual ativado, execute no CMD:

```bat
echo %VIRTUAL_ENV%
```

Esse comando mostra o caminho da pasta da `.venv`.

Exemplo:

```text
C:\caminho\para\es2-saude-cardiaca-backend\acompanhamento_cardiaco\.venv
```

Para descobrir o caminho do Python usado pela `.venv`, execute:

```bat
where python
```

O caminho esperado será parecido com:

```text
C:\caminho\para\es2-saude-cardiaca-backend\acompanhamento_cardiaco\.venv\Scripts\python.exe
```

---

## 18. Arquivos que devem ser versionados

Os arquivos abaixo devem ser enviados para o Git:

- `pyproject.toml`
- `poetry.lock`
- `README.md`
- `docs/WINDOWS_ENVIRONMENT_SETUP.md`
- `acompanhamento_cardiaco/`
- `tests/`
- `.vscode/settings.json`, caso o grupo queira padronizar o VS Code

O arquivo `poetry.lock` é importante porque registra as versões exatas das dependências instaladas.

Isso ajuda a garantir que outra pessoa consiga instalar o projeto com as mesmas versões.

---

## 19. Arquivos que não devem ser versionados

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

## 20. Resumo dos principais comandos

Instalar o pipx:

```bat
py -m pip install --user pipx
py -m pipx ensurepath
```

Instalar o Poetry:

```bat
pipx install poetry
```

Atualizar o Poetry:

```bat
pipx upgrade poetry
```

Configurar ambiente virtual dentro do projeto:

```bat
poetry config virtualenvs.in-project true --local
```

Instalar o Python 3.13 pelo Poetry:

```bat
poetry python install 3.13
```

Listar versões de Python disponíveis para o Poetry:

```bat
poetry python list
```

Configurar o projeto para usar Python 3.13:

```bat
poetry env use 3.13
```

Instalar dependências:

```bat
poetry install
```

Rodar aplicação:

```bat
poetry run task run
```

Rodar lint:

```bat
poetry run task lint
```

Formatar código:

```bat
poetry run task format
```

Rodar testes:

```bat
poetry run task test
```

Ativar ambiente virtual no CMD:

```bat
.venv\Scripts\activate.bat
```

Ativar ambiente virtual no PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Sair do ambiente virtual:

```bat
deactivate
```
