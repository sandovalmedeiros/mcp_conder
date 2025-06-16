# diagnostico.py
"""Script para diagnosticar problemas com ferramentas MCP"""

import sys
import importlib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verificar_imports():
    """Verifica se todos os imports necessários estão disponíveis"""
    imports_necessarios = [
        "fastmcp",
        "fastmcp.tools.schema",
        "fastmcp.tools.base",
        "requests",
        "json"
    ]
    
    problemas = []
    
    for modulo in imports_necessarios:
        try:
            importlib.import_module(modulo)
            logger.info(f"✅ {modulo} - OK")
        except ImportError as e:
            logger.error(f"❌ {modulo} - ERRO: {str(e)}")
            problemas.append(f"Módulo {modulo} não encontrado: {str(e)}")
    
    return problemas

def verificar_estrutura_arquivos():
    """Verifica se a estrutura de arquivos está correta"""
    arquivos_necessarios = [
        "main.py",
        "mcp_server/server.py",
        "wfs_decreto_tool.py"
    ]
    
    problemas = []
    
    for arquivo in arquivos_necessarios:
        if Path(arquivo).exists():
            logger.info(f"✅ {arquivo} - OK")
            
            # Verificar se não está vazio
            if Path(arquivo).stat().st_size == 0:
                logger.warning(f"⚠️  {arquivo} está vazio")
                problemas.append(f"Arquivo {arquivo} está vazio")
        else:
            logger.error(f"❌ {arquivo} - NÃO ENCONTRADO")
            problemas.append(f"Arquivo {arquivo} não encontrado")
    
    return problemas

def verificar_sintaxe():
    """Verifica sintaxe dos arquivos Python"""
    arquivos_python = [
        "main.py",
        "mcp_server/server.py", 
        "wfs_decreto_tool.py"
    ]
    
    problemas = []
    
    for arquivo in arquivos_python:
        if Path(arquivo).exists():
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    codigo = f.read()
                    
                if codigo.strip():  # Se não está vazio
                    compile(codigo, arquivo, 'exec')
                    logger.info(f"✅ {arquivo} - Sintaxe OK")
            except SyntaxError as e:
                logger.error(f"❌ {arquivo} - ERRO DE SINTAXE: {str(e)}")
                problemas.append(f"Erro de sintaxe em {arquivo}: {str(e)}")
            except Exception as e:
                logger.error(f"❌ {arquivo} - ERRO: {str(e)}")
                problemas.append(f"Erro ao verificar {arquivo}: {str(e)}")
    
    return problemas

def testar_instanciacao():
    """Testa se as classes podem ser instanciadas"""
    problemas = []
    
    try:
        # Tentar importar e instanciar a ferramenta
        from wfs_decreto_tool import WFSDecretoTool
        tool = WFSDecretoTool()
        logger.info("✅ WFSDecretoTool instanciada com sucesso")
        
        # Verificar se tem os métodos necessários
        metodos_necessarios = ['execute', 'get_schema']
        for metodo in metodos_necessarios:
            if hasattr(tool, metodo):
                logger.info(f"✅ Método {metodo} encontrado")
            else:
                logger.error(f"❌ Método {metodo} não encontrado")
                problemas.append(f"Método {metodo} não implementado")
                
    except Exception as e:
        logger.error(f"❌ Erro ao instanciar WFSDecretoTool: {str(e)}")
        problemas.append(f"Não foi possível instanciar WFSDecretoTool: {str(e)}")
    
    return problemas

def main():
    """Executa todos os diagnósticos"""
    logger.info("🔍 Iniciando diagnóstico do projeto MCP...")
    logger.info("=" * 50)
    
    todos_problemas = []
    
    # Verificar imports
    logger.info("📦 Verificando imports...")
    problemas = verificar_imports()
    todos_problemas.extend(problemas)
    
    # Verificar estrutura
    logger.info("\n📁 Verificando estrutura de arquivos...")
    problemas = verificar_estrutura_arquivos()
    todos_problemas.extend(problemas)
    
    # Verificar sintaxe
    logger.info("\n🐍 Verificando sintaxe Python...")
    problemas = verificar_sintaxe()
    todos_problemas.extend(problemas)
    
    # Testar instanciação
    logger.info("\n🔧 Testando instanciação de classes...")
    problemas = testar_instanciacao()
    todos_problemas.extend(problemas)
    
    # Relatório final
    logger.info("\n" + "=" * 50)
    if todos_problemas:
        logger.error("❌ PROBLEMAS ENCONTRADOS:")
        for i, problema in enumerate(todos_problemas, 1):
            logger.error(f"  {i}. {problema}")
        
        logger.info("\n💡 SUGESTÕES:")
        logger.info("  - Instale as dependências: pip install -r requirements.txt")
        logger.info("  - Verifique se todos os arquivos foram criados corretamente")
        logger.info("  - Corrija os erros de sintaxe listados acima")
        
    else:
        logger.info("✅ Nenhum problema encontrado!")
        logger.info("   O projeto parece estar configurado corretamente.")

if __name__ == "__main__":
    main()