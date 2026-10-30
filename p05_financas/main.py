"""Projeto 05: receitas, despesas e agregacoes com valores em centavos."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from conexao import banco

lancamentos = banco['lancamentos_p05']


def centavos(texto):
    try:
        valor = Decimal(texto.replace(',', '.'))
        if not valor.is_finite() or valor <= 0:
            raise ValueError
        return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError):
        return None


def reais(centavos):
    """Formata centavos no padrao brasileiro: 150050 -> 'R$ 1.500,50'."""
    texto = f'{centavos / 100:,.2f}'
    return 'R$ ' + texto.replace(',', 'X').replace('.', ',').replace('X', '.')


while True:
    print('\n[1] Registrar [2] Extrato [3] Resumo por categoria [0] Sair')
    op = input('Opcao: ').strip()
    if op == '1':
        tipo = input('Tipo (receita/despesa): ').strip().lower()
        categoria = input('Categoria: ').strip()
        valor = centavos(input('Valor (R$): ').strip())
        if tipo not in ('receita', 'despesa') or not categoria or valor is None:
            print('Dados invalidos.')
            continue
        lancamentos.insert_one({'tipo': tipo, 'categoria': categoria,
                                'valor_centavos': valor,
                                'criado_em': datetime.now(timezone.utc)})
        print('Lancamento registrado.')
    elif op == '2':
        for item in lancamentos.find().sort('criado_em', -1).limit(30):
            print(f"{item['tipo']} | {item['categoria']} | {reais(item['valor_centavos'])}")
    elif op == '3':
        pipeline = [
            {'$group': {'_id': {'tipo': '$tipo', 'categoria': '$categoria'},
                        'total': {'$sum': '$valor_centavos'}}},
            {'$sort': {'_id.tipo': 1, '_id.categoria': 1}}
        ]
        receitas = despesas = 0
        for item in lancamentos.aggregate(pipeline):
            tipo, categoria = item['_id']['tipo'], item['_id']['categoria']
            total = item['total']
            print(f'{tipo} / {categoria}: {reais(total)}')
            if tipo == 'receita':
                receitas += total
            else:
                despesas += total
        print(f'SALDO: {reais(receitas - despesas)}')
    elif op == '0':
        break
    else:
        print('Opcao invalida.')
