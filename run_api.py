#!/usr/bin/env python
"""
Script para iniciar a API Bancária com FastAPI
Execute este arquivo para começar o servidor
"""

import subprocess
import sys
import webbrowser
import time

def main():
    print("\n" + "="*60)
    print("🚀 INICIANDO API BANCÁRIA DIO")
    print("="*60 + "\n")
    
    print("📋 Informações:")
    print("  • API: http://localhost:8000")
    print("  • Documentação Swagger: http://localhost:8000/docs")
    print("  • Documentação ReDoc: http://localhost:8000/redoc")
    print("  • Teste: python test_api.py")
    print("\n⏳ Iniciando servidor...\n")
    
    try:
        # Executar o servidor uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "api:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n\n✋ Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
