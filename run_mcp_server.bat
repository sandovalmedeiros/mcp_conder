@echo off
REM run_mcp_server.bat - Script para executar servidor MCP com dependências

REM Definir variáveis
set PYTHON_EXE="C:\Program Files\Python312\python.exe"
set PROJECT_DIR=D:\Proj_CrewAI\Projetos\mcp_conder
set SERVER_SCRIPT=%PROJECT_DIR%\mcp_stdio_server.py

REM Log de debug para Claude Desktop
echo [DEBUG] Iniciando servidor MCP... >&2
echo [DEBUG] Python: %PYTHON_EXE% >&2
echo [DEBUG] Projeto: %PROJECT_DIR% >&2
echo [DEBUG] Script: %SERVER_SCRIPT% >&2

REM Mudar para diretório do projeto
cd /d "%PROJECT_DIR%"

REM Verificar se pydantic está instalado, se não, instalar
%PYTHON_EXE% -c "import pydantic" 2>nul
if %errorlevel% neq 0 (
    echo [DEBUG] Instalando pydantic... >&2
    %PYTHON_EXE% -m pip install pydantic --quiet
    if %errorlevel% neq 0 (
        echo [ERROR] Falha ao instalar pydantic >&2
        exit /b 1
    )
    echo [DEBUG] Pydantic instalado com sucesso >&2
)

REM Verificar se fastmcp está instalado
%PYTHON_EXE% -c "import fastmcp" 2>nul
if %errorlevel% neq 0 (
    echo [DEBUG] Instalando fastmcp... >&2
    %PYTHON_EXE% -m pip install fastmcp --quiet
    if %errorlevel% neq 0 (
        echo [ERROR] Falha ao instalar fastmcp >&2
        exit /b 1
    )
    echo [DEBUG] FastMCP instalado com sucesso >&2
)

REM Verificar se arquivo existe
if not exist "%SERVER_SCRIPT%" (
    echo [ERROR] Arquivo não encontrado: %SERVER_SCRIPT% >&2
    exit /b 1
)

REM Executar servidor MCP
echo [DEBUG] Executando servidor MCP... >&2
%PYTHON_EXE% "%SERVER_SCRIPT%"

REM Se chegou aqui, algo deu errado
echo [ERROR] Servidor MCP terminou inesperadamente >&2
exit /b 1
