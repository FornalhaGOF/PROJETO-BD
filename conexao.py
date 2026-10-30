"""Conexao compartilhada com o MongoDB.

A URI e lida do arquivo .env (variavel MONGO_URI), portanto o mesmo codigo
funciona com o MongoDB local ou com um cluster no MongoDB Atlas.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / '.env')

URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

cliente = MongoClient(URI, serverSelectionTimeoutMS=5000)

try:
    cliente.admin.command('ping')
except PyMongoError as exc:
    raise SystemExit(
        'Nao foi possivel conectar ao MongoDB.\n'
        f'URI usada: {URI}\n'
        'Verifique se o servidor esta ligado (scripts\\iniciar_mongodb.bat)\n'
        'ou se a URI do Atlas esta correta no arquivo .env.\n'
        f'Detalhe tecnico: {exc}'
    ) from exc

banco = cliente['laboratorio_python']
