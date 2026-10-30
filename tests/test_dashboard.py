"""Testes do Projeto 10 (dashboard de vendas).

Uso (da raiz do projeto, com o MongoDB ligado):
    python -m unittest discover -s tests -v
"""
import unittest

from p10_dashboard.main import (filtro_periodo, reais, resumo_por_categoria,
                                semear_dados, top_produtos, vendas)


class TestDashboard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        semear_dados()

    def test_semente_idempotente(self):
        """Executar a semente duas vezes nao duplica as vendas."""
        antes = vendas.count_documents({})
        semear_dados()
        semear_dados()
        self.assertEqual(antes, vendas.count_documents({}))

    def test_codigos_unicos(self):
        codigos = vendas.distinct('codigo')
        self.assertEqual(len(codigos), vendas.count_documents({}))

    def test_total_por_categoria(self):
        dados = resumo_por_categoria({})
        self.assertTrue(dados)
        total = sum(d['faturamento'] for d in dados)
        direto = sum(d['total_centavos'] for d in vendas.find({}))
        self.assertEqual(total, direto)

    def test_top_produtos_respeita_limite(self):
        self.assertEqual(len(top_produtos({}, 3)), 3)
        ranking = top_produtos({}, 5)
        valores = [item['faturamento'] for item in ranking]
        self.assertEqual(valores, sorted(valores, reverse=True))

    def test_filtro_periodo_invalido_nao_retorna_vendas_antigas(self):
        from datetime import datetime, timedelta, timezone
        filtro = {'data': {'$lt': datetime.now(timezone.utc) - timedelta(days=365)}}
        self.assertEqual(resumo_por_categoria(filtro), [])

    def test_formato_reais(self):
        self.assertEqual(reais(567640), 'R$ 5.676,40')
        self.assertEqual(reais(50), 'R$ 0,50')


if __name__ == '__main__':
    unittest.main()
