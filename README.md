# MCP CONDER

**Espacialização dos Decretos Estaduais – SECAR/INFORMS**

Este projeto implementa um servidor MCP (Model Context Protocol) voltado à consulta e espacialização de dados do serviço WFS da CONDER, especialmente poligonais georreferenciadas de decretos estaduais da Bahia entre 2013 e 2025.

## 🛰️ Objetivo

- Conectar a serviços WFS públicos (ex: CONDER)
- Interpretar arquivos `capabilities.xml`, `featuretype.xml`, `GML`
- Atuar como backend para integração com LLMs (Claude Desktop, Ollama)
- Disponibilizar um protocolo `STDIO` para agentes inteligentes

---

## 🖥️ Requisitos

- Windows 10 ou superior
- Python 3.12
- Acesso à internet para instalar dependências

---

## 📦 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/sandovalmedeiros/mcp_conder.git
cd mcp_conder
```

### 2. Configure o Python

Verifique o caminho do seu Python (ex: `C:\Program Files\Python312\python.exe`) e ajuste no script `run_mcp_server.bat`, se necessário.

### 3. Execute com o script automatizado

```cmd
run_mcp_server.bat
```

Esse script:
- Verifica/instala `pydantic` e `fastmcp`
- Inicializa `mcp_stdio_server.py`
- Emite logs de depuração (usados por Claude Desktop)

---

## 🧪 Estrutura do Projeto

| Arquivo                        | Função Principal                                  |
|-------------------------------|----------------------------------------------------|
| `main.py`                     | Versão alternativa de execução do servidor        |
| `mcp_stdio_server.py`         | Entrada principal usada com Claude Desktop        |
| `run_mcp_server.bat`          | Inicializador automático no Windows               |
| `capabilities.xml`            | Exemplo de resposta GetCapabilities do WFS        |
| `featuretype.xml`             | Exemplo de FeatureTypeSchema                      |
| `exemplo_GML3.xml`            | Exemplo de resposta WFS com geometrias            |
| `.env`                        | Configurações como URL do WFS                     |
| `pyproject.toml`              | Definição de dependências                         |

---

## 🔐 Exemplo de `.env`

```env
WFS_URL=https://mapas.conder.ba.gov.br/arcgis/services/Decretos/Decretos/MapServer/WFSServer
MCP_PORT=8000
```

---


## 🧠 Integração com Claude Desktop

Este servidor MCP pode ser integrado ao Claude Desktop por meio do protocolo STDIO.

### Configuração recomendada

No painel de configurações avançadas do Claude Desktop ou no arquivo `claude.desktop.json`, adicione:

```json
"mcpServers": {
  "wfs-decreto-server": {
    "command": "D:\\Proj_CrewAI\\Projetos\\mcp_conder\\run_mcp_server.bat"
  }
}
```

Isso permite que o Claude acione o servidor MCP diretamente para responder a perguntas sobre os dados espaciais dos decretos.

> Certifique-se de que o caminho do script `.bat` está correto e o Python esteja instalado conforme especificado.


## 📤 Publicando no GitHub

```bash
git init
git remote add origin https://github.com/sandovalmedeiros/mcp_conder.git
git add .
git commit -m "Versão inicial do servidor MCP CONDER"
git push -u origin main
```

## 🧑‍💼 Autoria

Projeto desenvolvido por **Sandoval Medeiros, DIGEO/SEI Bahia**, no âmbito do **SECAR/INFORMS**, com foco na governança territorial baseada em dados.

---

> Este projeto está licenciado nos termos da [MIT License](LICENSE).
