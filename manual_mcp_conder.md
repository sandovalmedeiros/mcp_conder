# Manual da Aplicação – MCP CONDER

**Projeto:** Espacialização dos Decretos Estaduais – SECAR/INFORMS  
**Instituição:** SEI Bahia / DIGEO  
**Finalidade:** Estruturar um servidor MCP para acessar e interpretar dados espaciais de decretos estaduais via serviço WFS da CONDER.

---

## 1. Visão Geral

Este manual documenta a instalação, configuração, execução e uso do sistema MCP CONDER. A aplicação tem como finalidade principal servir como uma interface intermediária entre serviços WFS (ArcGIS Server) e agentes inteligentes, como LLMs integradas via protocolo MCP.

---

## 2. Pré-requisitos

- **Sistema Operacional:** Windows 10 ou superior
- **Python:** versão 3.12 instalada
- **Editor recomendado:** VSCode ou Notepad++
- **Permissões de internet e firewall liberadas**

---

## 3. Estrutura da Aplicação

```
mcp_conder/
├── main.py
├── mcp_stdio_server.py
├── run_mcp_server.bat
├── capabilities.xml
├── featuretype.xml
├── exemplo_GML3.xml
├── .env
├── pyproject.toml
├── configuracao_producao.md
├── readme_instrucoes.md
```

- `mcp_stdio_server.py`: principal servidor usado em integração com Claude Desktop
- `run_mcp_server.bat`: script automatizado para execução e instalação de dependências
- `*.xml`: exemplos de resposta WFS

---

## 4. Configuração

### 4.1. Variáveis `.env`

Crie um arquivo `.env` com:

```
WFS_URL=https://mapas.conder.ba.gov.br/arcgis/services/Decretos/Decretos/MapServer/WFSServer
MCP_PORT=8000
```

---

## 5. Execução

### Método recomendado:

Execute o script `.bat`:

```cmd
run_mcp_server.bat
```

Este comando:
- Define caminhos de Python e projeto
- Verifica/instala `pydantic` e `fastmcp`
- Executa o script `mcp_stdio_server.py`
- Gera logs de depuração para uso com Claude Desktop

### Alternativamente:

```bash
python mcp_stdio_server.py
```

---

## 6. Integração com Claude Desktop

Este projeto pode ser consumido como uma **ferramenta via protocolo MCP STDIO** pelo Claude Desktop.

### Configuração

Inclua no arquivo `claude.desktop.json` ou no painel de configuração avançado do Claude Desktop:

```json
"mcpServers": {
  "wfs-decreto-server": {
    "command": "D:\\Proj_CrewAI\\Projetos\\mcp_conder\\run_mcp_server.bat"
  }
}
```

> Certifique-se de que o caminho seja acessível e que o script `run_mcp_server.bat` esteja funcionando corretamente.

### Execução

- Inicie o Claude Desktop
- Selecione o MCP `wfs-decreto-server`
- Comece a interagir com perguntas como:
  - “Liste os decretos de desapropriação em 2021.”
  - “Quais municípios estão afetados pelos decretos ativos?”


Este projeto pode ser consumido como uma **ferramenta via protocolo MCP STDIO** pelo Claude Desktop. Para isso:
- Execute o script `run_mcp_server.bat`
- Configure o Claude Desktop para ler via STDIO local
- O modelo pode fazer perguntas ao MCP (ex: “Quais decretos estão ativos em Salvador?”)

---

## 7. Exemplos de Uso

- `capabilities.xml` → resultado de um GetCapabilities
- `featuretype.xml` → descrição de camadas (layer schema)
- `exemplo_GML3.xml` → resposta real com poligonais

Esses arquivos podem ser usados para testes com agentes de IA que interpretam XML e GML.

---

## 8. Solução de Problemas

| Problema                                      | Solução                                               |
|----------------------------------------------|--------------------------------------------------------|
| Python não encontrado                        | Ajuste o caminho da variável `PYTHON_EXE` no `.bat`    |
| Falha ao instalar dependência via pip        | Execute manualmente: `pip install fastmcp pydantic`   |
| Porta ocupada (erro 8000)                    | Altere `MCP_PORT` no `.env` para uma porta livre       |
| Claude Desktop não responde                  | Verifique logs `mcp_server.log`                        |

---

## 9. Autoria

Projeto desenvolvido pela equipe da **Diretoria de Geoinformação (DIGEO)** da **SEI Bahia**, no âmbito do projeto **SECAR/INFORMS**.

---

## 10. Licença

Este projeto é distribuído sob os termos da licença MIT. Veja o arquivo `LICENSE` (se aplicável).
