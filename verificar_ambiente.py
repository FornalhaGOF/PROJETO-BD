"""Verifica o ambiente antes da apresentacao.

Uso (na raiz do projeto, com o .venv ativado):
    python verificar_ambiente.py
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def main():
    print(f'Python: {sys.version.split()[0]}')

    faltando = []
    for modulo in ('pymongo', 'dotenv', 'fastapi', 'uvicorn', 'matplotlib'):
        try:
            __import__(modulo)
            print(f'  [OK] {modulo}')
        except ImportError:
            print(f'  [FALTA] {modulo}')
            faltando.append(modulo)

    if faltando:
        print('\nInstale as dependencias:')
        print('  python -m pip install -r requirements.txt')
        return 1

    if not (BASE / '.env').exists():
        print('\n[AVISO] Arquivo .env ausente. Copie .env.example para .env')
        return 1

    from conexao import banco

    print(f'\nMongoDB conectado. Banco: {banco.name}')
    for nome in sorted(banco.list_collection_names()):
        total = banco[nome].estimated_document_count()
        print(f'  {nome}: {total} documento(s)')

    print('\nAmbiente pronto para a apresentacao.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
