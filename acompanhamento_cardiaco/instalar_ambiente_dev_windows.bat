@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist "pyproject.toml" (
    echo ERRO: este arquivo .bat deve estar na raiz do projeto.
    echo Nao foi encontrado o arquivo pyproject.toml.
    echo.
    echo Coloque este arquivo na mesma pasta do pyproject.toml.
    pause
    exit /b 1
)

echo ============================================
echo Configuracao do ambiente - Windows
echo Projeto: acompanhamento-cardiaco
echo ============================================
echo.

REM ==================================================
REM 1. Verifica se o Git esta instalado
REM ==================================================
echo [1/9] Verificando Git...

where git >nul 2>nul

if errorlevel 1 (
    echo Git nao encontrado.
    echo Tentando instalar Git com winget...

    where winget >nul 2>nul

    if errorlevel 1 (
        echo ERRO: winget nao encontrado.
        echo Instale o Git manualmente em:
        echo https://git-scm.com/downloads
        pause
        exit /b 1
    )

    winget install --id Git.Git -e
) else (
    echo Git encontrado.
)

echo.

REM ==================================================
REM 2. Verifica se existe um Python inicial
REM ==================================================
echo [2/9] Verificando Python inicial...

where py >nul 2>nul

if errorlevel 1 (
    echo Python Launcher nao encontrado.
    echo Tentando instalar Python 3.13 com winget...

    where winget >nul 2>nul

    if errorlevel 1 (
        echo ERRO: winget nao encontrado.
        echo Instale o Python manualmente em:
        echo https://www.python.org/downloads/
        pause
        exit /b 1
    )

    winget install --id Python.Python.3.13 -e

    echo.
    echo Feche e abra o terminal novamente depois da instalacao do Python.
    echo Em seguida, execute este arquivo .bat outra vez.
    pause
    exit /b 0
) else (
    py --version
)

echo.

REM ==================================================
REM 3. Instala ou atualiza o pipx
REM ==================================================
echo [3/9] Instalando pipx...

py -m pip install --user --upgrade pipx

if errorlevel 1 (
    echo ERRO: falha ao instalar o pipx.
    pause
    exit /b 1
)

py -m pipx ensurepath

REM Atualiza o PATH desta sessao para tentar reconhecer pipx/poetry sem reabrir o terminal
set "PATH=%USERPROFILE%\.local\bin;%APPDATA%\Python\Python312\Scripts;%PATH%"

for /d %%D in ("%APPDATA%\Python\Python*\Scripts") do (
    set "PATH=%%~fD;!PATH!"
)

echo pipx instalado/configurado.
echo.

REM ==================================================
REM 4. Instala ou atualiza o Poetry
REM ==================================================
echo [4/9] Instalando Poetry com pipx...

py -m pipx install poetry

if errorlevel 1 (
    echo Poetry pode ja estar instalado. Tentando atualizar...
    py -m pipx upgrade poetry
)

echo.

REM ==================================================
REM 5. Verifica se o Poetry esta disponivel
REM ==================================================
echo [5/9] Verificando Poetry...

set "POETRY_CMD=poetry"

where poetry >nul 2>nul

if errorlevel 1 (
    if exist "%USERPROFILE%\.local\bin\poetry.exe" (
        set "POETRY_CMD=%USERPROFILE%\.local\bin\poetry.exe"
    ) else if exist "%USERPROFILE%\pipx\venvs\poetry\Scripts\poetry.exe" (
        set "POETRY_CMD=%USERPROFILE%\pipx\venvs\poetry\Scripts\poetry.exe"
    ) else (
        echo Poetry ainda nao foi reconhecido nesta sessao.
        echo.
        echo Feche e abra o terminal novamente.
        echo Depois execute este arquivo .bat outra vez.
        echo.
        echo Caso ainda nao funcione, rode:
        echo py -m pipx ensurepath
        pause
        exit /b 0
    )
)

"%POETRY_CMD%" --version

if errorlevel 1 (
    echo ERRO: Poetry foi encontrado, mas nao executou corretamente.
    pause
    exit /b 1
)

echo.

REM ==================================================
REM 6. Configura ambiente virtual dentro do projeto
REM ==================================================
echo [6/9] Configurando ambiente virtual dentro do projeto...

"%POETRY_CMD%" config virtualenvs.in-project true --local

if errorlevel 1 (
    echo ERRO: falha ao configurar o ambiente virtual local.
    pause
    exit /b 1
)

echo Ambiente virtual sera criado em .venv/
echo.

REM ==================================================
REM 7. Instala Python 3.13 pelo Poetry
REM ==================================================
echo [7/9] Instalando Python 3.13 pelo Poetry...

"%POETRY_CMD%" python install 3.13

if errorlevel 1 (
    echo AVISO: nao foi possivel instalar o Python 3.13 pelo Poetry.
    echo Tentando atualizar o Poetry...
    py -m pipx upgrade poetry

    "%POETRY_CMD%" python install 3.13

    if errorlevel 1 (
        echo ERRO: falha ao instalar Python 3.13 pelo Poetry.
        echo Instale o Python 3.13 manualmente ou verifique sua versao do Poetry.
        pause
        exit /b 1
    )
)

echo.

REM ==================================================
REM 8. Cria ambiente e instala dependencias
REM ==================================================
echo [8/9] Instalando dependencias do projeto...

"%POETRY_CMD%" env use 3.13

if errorlevel 1 (
    echo AVISO: Poetry nao encontrou o Python apenas com "3.13".
    echo.
    echo Listando versoes disponiveis:
    "%POETRY_CMD%" python list
    echo.
    echo Tente configurar manualmente depois com:
    echo poetry env use CAMINHO_DO_PYTHON
    pause
    exit /b 1
)

"%POETRY_CMD%" install

if errorlevel 1 (
    echo ERRO: falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.

REM ==================================================
REM 9. Configura VS Code sem sobrescrever settings existente
REM ==================================================
echo [9/9] Configurando VS Code...

if not exist ".vscode" (
    mkdir ".vscode"
    echo Pasta .vscode criada.
) else (
    echo Pasta .vscode ja existe.
)

if exist ".vscode\settings.json" (
    echo Arquivo .vscode\settings.json ja existe.
    echo Nenhuma alteracao foi feita para evitar sobrescrever configuracoes existentes.
) else (
    (
    echo {
    echo   "python.defaultInterpreterPath": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
    echo   "python.testing.pytestEnabled": true,
    echo   "python.testing.pytestArgs": [
    echo     "tests"
    echo   ],
    echo   "editor.formatOnSave": true,
    echo   "ruff.enable": true
    echo }
    ) > ".vscode\settings.json"

    echo Arquivo .vscode\settings.json criado com sucesso.
)

echo.
echo ============================================
echo Ambiente configurado com sucesso!
echo ============================================
echo.
echo Para rodar o projeto:
echo poetry run task run
echo.
echo Para rodar os testes:
echo poetry run task test
echo.
echo Para rodar o lint:
echo poetry run task lint
echo.
echo Para formatar o codigo:
echo poetry run task format
echo.
echo Para ativar o ambiente virtual no CMD:
echo .venv\Scripts\activate.bat
echo.
echo Para ativar o ambiente virtual no PowerShell:
echo .venv\Scripts\Activate.ps1
echo.
echo Para sair do ambiente virtual:
echo deactivate
echo.
pause