"""Projeto 10: dashboard de vendas com aggregation pipeline e grafico.

Execucao:
    python -m p10_dashboard.main
    python -m p10_dashboard.main --dias 30 --top 3

O script e idempotente: rodar varias vezes nao duplica as vendas de exemplo.
"""
import argparse
import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # backend sem janela: gera apenas o arquivo PNG
import matplotlib.pyplot as plt

from conexao import banco

PASTA = Path(__file__).resolve().parent
ARQUIVO_GRAFICO = PASTA / 'grafico_vendas.png'
ARQUIVO_CSV = PASTA / 'relatorio_vendas.csv'

vendas = banco['vendas_p10']
vendas.create_index('codigo', unique=True)
vendas.create_index([('categoria', 1), ('data', -1)])


def adicionar(codigo, categoria, produto, quantidade, preco_centavos, dias_atras=0):
    """Insere a venda apenas se o codigo ainda nao existir (idempotente)."""
    vendas.update_one(
        {'codigo': codigo},
        {'$setOnInsert': {
            'codigo': codigo,
            'categoria': categoria,
            'produto': produto,
            'quantidade': quantidade,
            'preco_centavos': preco_centavos,
            'total_centavos': quantidade * preco_centavos,
            'data': datetime.now(timezone.utc) - timedelta(days=dias_atras),
        }},
        upsert=True,
    )


def semear_dados():
    """Dados didaticos de exemplo (executar duas vezes nao duplica)."""
    adicionar('V001', 'Informática', 'Teclado', 2, 8990)
    adicionar('V002', 'Informática', 'Mouse', 4, 4590)
    adicionar('V003', 'Papelaria', 'Caderno', 5, 2490)
    adicionar('V004', 'Papelaria', 'Caneta', 20, 350)
    adicionar('V005', 'Informática', 'Monitor', 1, 89900)

    # Vendas adicionais para enriquecer o dashboard e o ranking.
    adicionar('V006', 'Informática', 'Notebook', 1, 349900, dias_atras=12)
    adicionar('V007', 'Informática', 'Headset', 3, 15900, dias_atras=9)
    adicionar('V008', 'Papelaria', 'Mochila', 2, 12990, dias_atras=6)
    adicionar('V009', 'Móveis', 'Cadeira Gamer', 1, 119900, dias_atras=4)
    adicionar('V010', 'Móveis', 'Mesa Digitalizadora', 1, 45900, dias_atras=3)
    adicionar('V011', 'Papelaria', 'Marca-texto', 10, 790, dias_atras=2)
    adicionar('V012', 'Informática', 'Webcam', 2, 21900, dias_atras=1)


def reais(centavos):
    """Formata centavos no padrao brasileiro: 567640 -> 'R$ 5.676,40'."""
    texto = f'{centavos / 100:,.2f}'
    return 'R$ ' + texto.replace(',', 'X').replace('.', ',').replace('X', '.')


def filtro_periodo(dias):
    if not dias:
        return {}
    limite = datetime.now(timezone.utc) - timedelta(days=dias)
    return {'data': {'$gte': limite}}


def resumo_por_categoria(filtro):
    pipeline = [
        {'$match': filtro},
        {'$group': {'_id': '$categoria',
                    'faturamento': {'$sum': '$total_centavos'},
                    'unidades': {'$sum': '$quantidade'},
                    'pedidos': {'$sum': 1}}},
        {'$sort': {'faturamento': -1}},
    ]
    return list(vendas.aggregate(pipeline))


def top_produtos(filtro, limite):
    pipeline = [
        {'$match': filtro},
        {'$group': {'_id': {'produto': '$produto', 'categoria': '$categoria'},
                    'unidades': {'$sum': '$quantidade'},
                    'faturamento': {'$sum': '$total_centavos'}}},
        {'$sort': {'faturamento': -1}},
        {'$limit': limite},
    ]
    return list(vendas.aggregate(pipeline))


def gerar_grafico(dados, destino):
    categorias = [d['_id'] for d in dados]
    valores = [d['faturamento'] / 100 for d in dados]
    rotulos = [reais(d['faturamento']) for d in dados]

    plt.figure(figsize=(9, 5))
    barras = plt.bar(categorias, valores, color='#2e7d32')
    plt.bar_label(barras, labels=rotulos, padding=4, fontsize=9)
    plt.ylabel('Faturamento (R$)')
    plt.title('Vendas por categoria')
    plt.ylim(0, max(valores) * 1.18)
    plt.grid(axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.savefig(destino, dpi=150)
    plt.close()
    return destino


def exportar_csv(dados, destino):
    with open(destino, 'w', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.writer(arquivo, delimiter=';')
        escritor.writerow(['categoria', 'pedidos', 'unidades', 'faturamento_reais'])
        for d in dados:
            escritor.writerow([d['_id'], d['pedidos'], d['unidades'],
                               f"{d['faturamento'] / 100:.2f}".replace('.', ',')])
    return destino


def main(argv=None):
    parser = argparse.ArgumentParser(description='Dashboard de vendas (MongoDB + Python)')
    parser.add_argument('--dias', type=int, default=None,
                        help='considerar apenas vendas dos ultimos N dias')
    parser.add_argument('--top', type=int, default=5,
                        help='quantidade de produtos no ranking (padrao: 5)')
    parser.add_argument('--sem-grafico', action='store_true',
                        help='nao gerar o arquivo PNG')
    args = parser.parse_args(argv)

    semear_dados()

    filtro = filtro_periodo(args.dias)
    dados = resumo_por_categoria(filtro)
    if not dados:
        print('Sem dados de vendas para o filtro escolhido.')
        return 1

    periodo = f'últimos {args.dias} dias' if args.dias else 'todo o período'
    print('=' * 58)
    print(f'RELATÓRIO DE VENDAS POR CATEGORIA ({periodo})')
    print('=' * 58)
    for item in dados:
        print(f"{item['_id']:<14} {item['unidades']:>4} un. | "
              f"{item['pedidos']:>2} pedidos | {reais(item['faturamento']):>14}")

    total = sum(item['faturamento'] for item in dados)
    unidades = sum(item['unidades'] for item in dados)
    print('-' * 58)
    print(f"Faturamento geral: {reais(total)} | Unidades: {unidades}")

    ranking = top_produtos(filtro, args.top)
    print(f'\nTOP {args.top} PRODUTOS POR FATURAMENTO')
    for posicao, item in enumerate(ranking, start=1):
        nome = item['_id']['produto']
        categoria = item['_id']['categoria']
        print(f"{posicao}. {nome} ({categoria}) -> "
              f"{item['unidades']} un. | {reais(item['faturamento'])}")

    if not args.sem_grafico:
        print(f'\nGráfico gerado: {gerar_grafico(dados, ARQUIVO_GRAFICO)}')
    print(f'CSV gerado:     {exportar_csv(dados, ARQUIVO_CSV)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
