from datetime import date
from decimal import Decimal
from os.path import dirname
from unittest import main
from unittest import TestCase

from movs.estrattoconto.__init__ import read_estrattoconto

PATH = f'{dirname(__file__)}/../test_estrattoconto.pdf'


class TestEstrattoconto(TestCase):
    def test_base(self) -> None:
        kv, rows = read_estrattoconto(PATH)

        # kv
        self.assertEqual(date(2022, 8, 31), kv.da)
        self.assertEqual(date(2022, 8, 31), kv.a)
        self.assertEqual('Tutte', kv.tipo)
        self.assertEqual('001030700957', kv.conto_bancoposta)
        self.assertEqual('CHREIM ELENA DE TULLIO VITO', kv.intestato_a)
        self.assertEqual(date(2022, 8, 31), kv.saldo_al)
        self.assertEqual(Decimal('350.85'), kv.saldo_contabile)
        self.assertEqual(Decimal('350.85'), kv.saldo_disponibile)

        # rows
        self.assertEqual([
        ], rows)


if __name__ == '__main__':
    main()
