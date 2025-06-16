# main.py
"""Arquivo principal para executar o servidor MCP - FastMCP 2.8.1"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Adicionar o diretório atual ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server.server import (
    create_mcp_server, 
    list_registered_tools, 
    test_tool_registration,
    debug_fastmcp_structure
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('mcp_server.log')
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Função principal para inicializar e testar o servidor MCP"""
    try:
        logger.info("🚀 INICIANDO SERVIDOR MCP - FastMCP 2.8.1")
        logger.info("=" * 60)
        
        # Criar servidor MCP
        logger.info("📦 Criando servidor MCP...")
        mcp = create_mcp_server()
        
        # Debug da estrutura interna (para entender melhor)
        debug_fastmcp_structure(mcp)
        
        # Testar registro de ferramentas
        if not test_tool_registration(mcp):
            logger.error("❌ Falha no teste de registro de ferramentas")
            return False
        
        # Listar ferramentas registradas
        tools = list_registered_tools(mcp)
        logger.info("\n📋 FERRAMENTAS REGISTRADAS:")
        logger.info("-" * 30)
        
        if tools and isinstance(tools, dict):
            for tool_name, tool_info in tools.items():
                if isinstance(tool_info, dict):
                    description = tool_info.get('description', 'Sem descrição')
                    logger.info(f"  🔧 {tool_name}: {description}")
                else:
                    logger.info(f"  🔧 {tool_name}: {str(tool_info)}")
        else:
            logger.warning("⚠️  Nenhuma ferramenta listada ou formato inválido")
            logger.info(f"📊 Tipo recebido: {type(tools)}")
            logger.info(f"📊 Conteúdo: {tools}")
        
        # Testar chamadas de ferramenta
        await test_tool_calls(mcp)
        
        # Informações finais
        logger.info("\n" + "=" * 60)
        logger.info("✅ SERVIDOR MCP INICIADO COM SUCESSO!")
        logger.info("🎯 Servidor pronto para receber chamadas")
        logger.info("📝 Log salvo em: mcp_server.log")
        logger.info("\n💡 Para testar as ferramentas:")
        logger.info("  - Decreto específico: numero_decreto='123', ano='2024'")
        logger.info("  - Busca avançada: municipio='Salvador', tipo_decreto='ORDINÁRIO'")
        
        # Manter servidor rodando
        logger.info("\n⏳ Pressione Ctrl+C para parar o servidor")
        
        # Em um ambiente real, você iniciaria o servidor MCP aqui
        # Exemplo: await mcp.run()
        
        # Para este exemplo, vamos simular o servidor rodando
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Parando servidor...")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro fatal ao iniciar servidor: {str(e)}")
        import traceback
        logger.error(f"📍 Traceback completo:\n{traceback.format_exc()}")
        return False

async def test_tool_calls(mcp):
    """Testa chamadas das ferramentas registradas"""
    logger.info("\n🧪 TESTANDO CHAMADAS DE FERRAMENTAS")
    logger.info("-" * 40)
    
    try:
        # Tentar diferentes formas de chamar as ferramentas
        
        # Teste 1: Busca básica de decreto
        logger.info("📤 Teste 1: Busca básica de decreto")
        await test_wfs_decreto_search(mcp)
        
        # Teste 2: Busca avançada
        logger.info("\n📤 Teste 2: Busca avançada de decretos")
        await test_busca_avancada(mcp)
        
    except Exception as e:
        logger.error(f"❌ Erro nos testes de ferramentas: {str(e)}")

async def test_wfs_decreto_search(mcp):
    """Testa a ferramenta de busca básica de decretos"""
    try:
        # Dados de teste
        test_data = {
            "numero_decreto": "12345",
            "ano": "2024",
            "assunto": "trânsito"
        }
        
        logger.info(f"  📋 Dados de entrada: {test_data}")
        
        # Tentar chamar a ferramenta
        result = await call_tool_safely(mcp, "wfs_decreto_search", test_data)
        
        if result:
            if result.get("success"):
                data = result.get("data", {})
                total = data.get("total_encontrados", 0)
                logger.info(f"  ✅ Sucesso! {total} decreto(s) encontrado(s)")
                
                # Mostrar primeiro decreto se existir
                decretos = data.get("decretos", [])
                if decretos:
                    primeiro = decretos[0]
                    logger.info(f"  📄 Primeiro resultado: Decreto {primeiro.get('numero')}/{primeiro.get('ano')}")
                    logger.info(f"      Assunto: {primeiro.get('assunto')}")
            else:
                logger.warning(f"  ⚠️  Ferramenta retornou erro: {result.get('error')}")
        else:
            logger.error("  ❌ Falha ao chamar ferramenta")
            
    except Exception as e:
        logger.error(f"  ❌ Erro no teste: {str(e)}")

async def test_busca_avancada(mcp):
    """Testa a ferramenta de busca avançada"""
    try:
        # Dados de teste
        test_data = {
            "municipio": "Salvador",
            "tipo_decreto": "ORDINÁRIO",
            "data_inicio": "2024-01-01",
            "data_fim": "2024-12-31"
        }
        
        logger.info(f"  📋 Dados de entrada: {test_data}")
        
        # Tentar chamar a ferramenta
        result = await call_tool_safely(mcp, "buscar_decretos_avancado", test_data)
        
        if result:
            if result.get("success"):
                data = result.get("data", {})
                total = data.get("total_encontrados", 0)
                logger.info(f"  ✅ Sucesso! {total} decreto(s) encontrado(s)")
                
                # Mostrar tipos de decretos encontrados
                decretos = data.get("decretos", [])
                if decretos:
                    tipos = set(d.get("tipo", "N/A") for d in decretos)
                    logger.info(f"  📊 Tipos encontrados: {', '.join(tipos)}")
            else:
                logger.warning(f"  ⚠️  Ferramenta retornou erro: {result.get('error')}")
        else:
            logger.error("  ❌ Falha ao chamar ferramenta")
            
    except Exception as e:
        logger.error(f"  ❌ Erro no teste: {str(e)}")

async def call_tool_safely(mcp, tool_name: str, args: dict):
    """Chama uma ferramenta de forma segura, tentando diferentes métodos"""
    
    # Método 1: Tentar chamar diretamente se existir método call_tool
    if hasattr(mcp, 'call_tool'):
        try:
            return await mcp.call_tool(tool_name, args)
        except Exception as e:
            logger.warning(f"  ⚠️  call_tool falhou: {str(e)}")
    
    # Método 2: Tentar acessar via tools manager
    if hasattr(mcp, 'tools'):
        try:
            tools_manager = mcp.tools
            if hasattr(tools_manager, 'call'):
                return await tools_manager.call(tool_name, args)
            elif hasattr(tools_manager, 'tools') and tool_name in tools_manager.tools:
                tool_func = tools_manager.tools[tool_name]
                return await tool_func(**args)
        except Exception as e:
            logger.warning(f"  ⚠️  tools manager falhou: {str(e)}")
    
    # Método 3: Tentar importar e chamar diretamente
    try:
        if tool_name == "wfs_decreto_search":
            from wfs_decreto_tool import wfs_decreto_search
            return await wfs_decreto_search(**args)
        elif tool_name == "buscar_decretos_avancado":
            from wfs_decreto_tool import buscar_decretos_avancado
            return await buscar_decretos_avancado(**args)
    except Exception as e:
        logger.warning(f"  ⚠️  chamada direta falhou: {str(e)}")
    
    logger.error(f"  ❌ Todos os métodos de chamada falharam para {tool_name}")
    return None

def run_server():
    """Executa o servidor MCP"""
    try:
        # Verificar ambiente
        logger.info("🔍 Verificando ambiente...")
        
        # Verificar se os arquivos necessários existem
        required_files = ["wfs_decreto_tool.py", "mcp_server/server.py"]
        for file_path in required_files:
            if not Path(file_path).exists():
                logger.error(f"❌ Arquivo necessário não encontrado: {file_path}")
                return False
        
        # Executar servidor
        success = asyncio.run(main())
        return success
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Servidor parado pelo usuário")
        return True
    except Exception as e:
        logger.error(f"❌ Erro fatal: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🎬 Iniciando aplicação MCP...")
    
    success = run_server()
    
    if success:
        logger.info("👋 Aplicação finalizada com sucesso!")
        sys.exit(0)
    else:
        logger.error("💥 Aplicação finalizada com erros!")
        sys.exit(1)