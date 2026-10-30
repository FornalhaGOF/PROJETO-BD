# Dashboard de Vendas — MongoDB + Python (Projeto 10)

Projeto de Banco de Dados — 4º bimestre.
Implementação completa dos 10 exercícios do material **MongoDB + Python**, com foco de
apresentação no **Projeto 10 (Dashboard de Vendas)**.

---

## 1. O que o projeto faz

O Projeto 10 lê vendas armazenadas no MongoDB, consolida os dados com um
**aggregation pipeline** (`$match`, `$group`, `$sum`, `$sort`, `$limit`) e gera:

- relatório de faturamento por categoria no terminal;
- ranking dos produtos mais vendidos;
- gráfico de barras em `p10_dashboard/grafico_vendas.png`;
- resumo exportado em `p10_dashboard/relatorio_vendas.csv`.

A carga inicial de dados é **idempotente**: rodar o script várias vezes **não duplica** vendas,
porque cada venda usa `update_one(..., upsert=True)` com `$setOnInsert` sobre o campo `codigo` (índice único).

## 2. Estrutura do repositório

```
ProjetoBD-4Bimestre/
├── README.md                     # material original da disciplina
├── README_DO_PROJETO.md          # este documento
├── GUIA_APRESENTACAO.md          # roteiro da apresentação
├── Ficha_Avaliacao_Projetos.pdf  # critérios de avaliação
├── conexao.py                    # conexão compartilhada (lê o .env)
├── requirements.txt
├── .env.example                  # modelo de configuração
├── verificar_ambiente.py         # checa dependências + conexão
├── scripts/
│   ├── iniciar_mongodb.bat       # sobe o MongoDB local
│   ├── parar_mongodb.bat         # encerra o MongoDB local
│   ├── demo_apresentacao.bat     # roda a demonstração completa (ensaio)
│   ├── abrir_compass.bat         # abre o Compass no banco local
│   └── publicar_github.bat       # envia o projeto para o GitHub
├── tests/
│   └── test_dashboard.py         # 6 testes automatizados do Projeto 10
├── p01_alunos/main.py            # CRUD de alunos
├── p02_biblioteca/main.py        # empréstimo atômico
├── p03_estoque/main.py           # $inc e estoque mínimo
├── p04_contatos/main.py          # regex e índice único
├── p05_financas/main.py          # agregações e centavos
├── p06_tarefas/main.py           # datas e atrasos
├── p07_turmas_notas/main.py      # $lookup e $avg
├── p08_corretor_provas/main.py   # regras de negócio
├── p09_api/main.py               # API REST com FastAPI
└── p10_dashboard/main.py         # dashboard de vendas  ← apresentação
```

## 3. Requisitos

| Item | Versão usada |
|------|--------------|
| Python | 3.13 |
| MongoDB Community Server | 8.0.3 (portátil, sem instalação) |
| PyMongo | 4.x |
| Matplotlib | 3.8+ |

## 4. Como executar

### 4.1 Ligar o MongoDB

```bat
scripts\iniciar_mongodb.bat
```

### 4.2 Criar o ambiente virtual e instalar dependências (primeira vez)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

> Se o PowerShell bloquear a ativação, use `.\.venv\Scripts\python.exe` direto.

### 4.3 Configurar a conexão

```powershell
Copy-Item .env.example .env
```

O padrão `mongodb://localhost:27017/` já funciona com o MongoDB local.
Para o Atlas, troque a `MONGO_URI` (o arquivo `.env` não vai para o GitHub).

### 4.4 Verificar o ambiente

```powershell
python verificar_ambiente.py
```

Saída esperada (resumo):

```
Python: 3.13.15
  [OK] pymongo
  [OK] dotenv
  [OK] fastapi
  [OK] uvicorn
  [OK] matplotlib

MongoDB conectado. Banco: laboratorio_python
  ...
Ambiente pronto para a apresentacao.
```

### 4.5 Rodar o Projeto 10

```powershell
python -m p10_dashboard.main
```

Opções:

```powershell
python -m p10_dashboard.main --dias 7      # só os últimos 7 dias
python -m p10_dashboard.main --top 3       # top 3 produtos
python -m p10_dashboard.main --sem-grafico # não gera o PNG
python -m p10_dashboard.main --sem-csv     # não gera o CSV
```

Saída esperada (12 vendas de exemplo):

```
==========================================================
RELATÓRIO DE VENDAS POR CATEGORIA (todo o período)
==========================================================
Informática      13 un. |  6 pedidos |    R$ 5.676,40
Móveis            2 un. |  2 pedidos |    R$ 1.658,00
Papelaria        37 un. |  4 pedidos |      R$ 533,30
----------------------------------------------------------
Faturamento geral: R$ 7.867,70 | Unidades: 52

TOP 5 PRODUTOS POR FATURAMENTO
1. Notebook (Informática) -> 1 un. | R$ 3.499,00
2. Cadeira Gamer (Móveis) -> 1 un. | R$ 1.199,00
3. Monitor (Informática) -> 1 un. | R$ 899,00
4. Headset (Informática) -> 3 un. | R$ 477,00
5. Mesa Digitalizadora (Móveis) -> 1 un. | R$ 459,00
```

### 4.6 Rodar os outros projetos

```powershell
python -m p01_alunos.main
python -m p02_biblioteca.main
python -m p03_estoque.main
python -m p04_contatos.main
python -m p05_financas.main
python -m p06_tarefas.main
python -m p07_turmas_notas.main
python -m p08_corretor_provas.main
uvicorn p09_api.main:app --reload      # http://127.0.0.1:8000/docs
```

## 5. Modelo de dados

Coleção `vendas_p10` (banco `laboratorio_python`):

```json
{
  "_id": "6741f0c2e13a4b0f9c1d2e3f",
  "codigo": "V001",
  "categoria": "Informática",
  "produto": "Teclado",
  "quantidade": 2,
  "preco_centavos": 8990,
  "total_centavos": 17980,
  "data": "2026-10-30T18:51:03Z"
}
```

Decisões de modelagem:

- **Valores em centavos (inteiro)** para evitar erro de arredondamento de `float`.
- **`total_centavos` desnormalizado** (`quantidade × preco_centavos`) para que a agregação
  não precise recalcular a cada consulta.
- **`codigo` com índice único** garante a idempotência da carga.
- **Índice composto `(categoria, data)`** sustenta os filtros por período e o `$group` por categoria.

Índices criados pelo script:

```python
vendas.create_index('codigo', unique=True)
vendas.create_index([('categoria', 1), ('data', -1)])
```

## 6. Como o aggregation pipeline funciona

```python
[
  {'$match': filtro},                    # 1. filtra o período (opcional)
  {'$group': {'_id': '$categoria',       # 2. agrupa por categoria
              'faturamento': {'$sum': '$total_centavos'},
              'unidades':    {'$sum': '$quantidade'},
              'pedidos':     {'$sum': 1}}},
  {'$sort': {'faturamento': -1}},        # 3. maior faturamento primeiro
]
```

O ranking de produtos é o mesmo pipeline agrupando por
`{'produto': ..., 'categoria': ...}` e acrescentando `{'$limit': n}`.

## 7. Testes automatizados

Com o MongoDB ligado:

```powershell
python -m unittest discover -s tests -t . -v
```

Resultado: **6 testes, OK**.

| Teste | O que garante |
|-------|---------------|
| `test_semente_idempotente` | rodar a carga 3x não duplica vendas |
| `test_codigos_unicos` | o índice único funciona |
| `test_total_por_categoria` | soma do relatório = soma dos documentos |
| `test_top_produtos_respeita_limite` | `--top` e ordenação corretos |
| `test_filtro_periodo_invalido...` | filtro de data devolve vazio, sem erro |
| `test_formato_reais` | formatação `R$ 5.676,40` |

Tratamento de erros implementado: conexão indisponível (mensagem clara em `conexao.py`),
entradas inválidas, duplicidade (`DuplicateKeyError`), ID malformado (400) e produto
inexistente (404) na API.

## 8. Desafios extras implementados (Projeto 10)

- Filtro por período com `--dias N`.
- Ranking configurável dos produtos mais vendidos (`--top N`).
- Exportação do resumo em CSV (`relatorio_vendas.csv`).
- Rótulos de valor no gráfico e formatação monetária brasileira.
- Testes automatizados.

## 9. Publicar no GitHub (repositório público)

1. Crie um repositório **público** em <https://github.com/new> chamado `ProjetoBD-4Bimestre`
   (não marque "Add a README").
2. No PowerShell, dentro da pasta do projeto:

```powershell
scripts\publicar_github.bat https://github.com/SEU-USUARIO/ProjetoBD-4Bimestre.git
```

3. Confirme que o repositório está **Public** em Settings → General → Danger Zone.

O `.gitignore` já impede o envio de `.env`, `.venv/`, `__pycache__/`, `*.png` e `*.csv`.

## 10. Checklist da entrega

- [x] Código executa sem erro de sintaxe
- [x] Arquivos e dependências organizados
- [x] MongoDB armazena e retorna os dados corretamente
- [x] Funcionalidades demonstradas (relatório, ranking, gráfico, CSV)
- [x] Evidências de execução (terminal, gráfico e Compass)
- [x] Desafio extra implementado
- [x] `.env` fora do versionamento
- [x] README do projeto
