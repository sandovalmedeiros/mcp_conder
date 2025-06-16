#!/usr/bin/env python3
# mcp_stdio_server.py
"""Servidor MCP usando STDIO para integração com Claude Desktop"""

import asyncio
import logging
import sys
import json
from pathlib import Path

# Adicionar path para imports
sys.path.insert(0, str(Path(__file__).parent))

# Configurar logging para arquivo (não interferir com STDIO)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_stdio.log'),
        # Não usar StreamHandler para não interferir com STDIO
    ]
)
logger = logging.getLogger(__name__)

def debug_to_stderr(message):
    """Envia mensagens de debug para stderr (visível no Claude Desktop)"""
    print(f"[DEBUG] {message}", file=sys.stderr, flush=True)

async def main():
    """Função principal para executar servidor STDIO"""
    try:
        debug_to_stderr("🚀 Iniciando servidor MCP STDIO para Claude Desktop...")
        logger.info("🚀 Iniciando servidor MCP STDIO para Claude Desktop...")
        
        # Importar FastMCP
        try:
            from fastmcp import FastMCP
            debug_to_stderr("✅ FastMCP importado com sucesso")
        except ImportError as e:
            debug_to_stderr(f"❌ Erro ao importar FastMCP: {e}")
            return
        
        # Importar ferramentas
        try:
            from wfs_decreto_tool import wfs_decreto_search, buscar_decretos_avancado
            debug_to_stderr("✅ Ferramentas importadas com sucesso")
        except ImportError as e:
            debug_to_stderr(f"❌ Erro ao importar ferramentas: {e}")
            return
        
        # Criar servidor MCP
        mcp = FastMCP("WFS Decreto Server")
        debug_to_stderr("✅ Servidor FastMCP criado")
        
        # Registrar ferramentas usando decorator @tool
        @mcp.tool
        async def consultar_decreto(numero_decreto: str, ano: str = "", assunto: str = "") -> dict:
            """
            Consulta um decreto específico por número.
            
            Args:
                numero_decreto: Número do decreto a ser consultado
                ano: Ano do decreto (opcional)
                assunto: Assunto/tema do decreto (opcional)
            
            Returns:
                Dicionário com informações do decreto encontrado
            """
            debug_to_stderr(f"📋 Claude solicitou consulta: decreto {numero_decreto}, ano {ano}")
            logger.info(f"📋 Claude solicitou consulta: decreto {numero_decreto}, ano {ano}")
            
            try:
                result = await wfs_decreto_search(numero_decreto, ano, assunto)
                total = result.get('data', {}).get('total_encontrados', 0)
                debug_to_stderr(f"📊 Resultado: {total} decreto(s) encontrado(s)")
                logger.info(f"📊 Resultado: {total} decreto(s)")
                return result
            except Exception as e:
                debug_to_stderr(f"❌ Erro na consulta: {e}")
                logger.error(f"❌ Erro na consulta: {e}")
                return {"success": False, "error": str(e)}
        
        @mcp.tool
        async def buscar_decretos_municipio(municipio: str, tipo_decreto: str = "", data_inicio: str = "", data_fim: str = "") -> dict:
            """
            Busca decretos por município com filtros opcionais.
            
            Args:
                municipio: Nome do município
                tipo_decreto: Tipo de decreto (ORDINÁRIO, COMPLEMENTAR, etc.)
                data_inicio: Data inicial da busca (YYYY-MM-DD)
                data_fim: Data final da busca (YYYY-MM-DD)
            
            Returns:
                Dicionário com lista de decretos encontrados
            """
            debug_to_stderr(f"🏙️ Claude solicitou busca: {municipio}, tipo {tipo_decreto}")
            logger.info(f"🏙️ Claude solicitou busca: {municipio}, tipo {tipo_decreto}")
            
            try:
                result = await buscar_decretos_avancado(municipio, tipo_decreto, data_inicio, data_fim)
                total = result.get('data', {}).get('total_encontrados', 0)
                debug_to_stderr(f"📊 Resultado: {total} decreto(s) encontrado(s)")
                logger.info(f"📊 Resultado: {total} decreto(s)")
                return result
            except Exception as e:
                debug_to_stderr(f"❌ Erro na busca: {e}")
                logger.error(f"❌ Erro na busca: {e}")
                return {"success": False, "error": str(e)}
        
        debug_to_stderr("✅ Ferramentas registradas para Claude Desktop")
        logger.info("✅ Ferramentas registradas para Claude Desktop")
        
        # Executar servidor em modo STDIO
        debug_to_stderr("🔌 Iniciando comunicação STDIO com Claude Desktop...")
        logger.info("🔌 Iniciando comunicação STDIO com Claude Desktop...")
        
        await mcp.run_stdio_async()
        
    except Exception as e:
        debug_to_stderr(f"❌ Erro no servidor STDIO: {e}")
        logger.error(f"❌ Erro no servidor STDIO: {e}")
        import traceback
        debug_to_stderr(f"📍 Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    # Executar servidor STDIO
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        debug_to_stderr("🛑 Servidor interrompido pelo usuário")
    except Exception as e:
        debug_to_stderr(f"💥 Erro fatal: {e}")
        sys.exit(1)
