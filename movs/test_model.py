from datetime import date
from decimal import Decimal
from unittest import TestCase

from .model import Row

data_contabile = date(2022, 11, 5)
data_valuta = date(2022, 11, 5)
descrizione_operazioni = 'descrizione_operazioni'


class TestRow(TestCase):
    def test_money_addebiti(self) -> None:
        addebiti = Decimal('123')
        accrediti = None

        row = Row(data_contabile, data_valuta, addebiti,
                  accrediti, descrizione_operazioni)

        expected = Decimal('-123')
        actual = row.money

        self.assertEqual(expected, actual)

    def test_money_accrediti(self) -> None:
        addebiti = None
        accrediti = Decimal('123')

        row = Row(data_contabile, data_valuta, addebiti,
                  accrediti, descrizione_operazioni)

        expected = Decimal('123')
        actual = row.money

        self.assertEqual(expected, actual)

    def test_money_zero(self) -> None:
        addebiti = None
        accrediti = None

        row = Row(data_contabile, data_valuta, addebiti,
                  accrediti, descrizione_operazioni)

        expected = Decimal('0')
        actual = row.money

        self.assertEqual(expected, actual)
