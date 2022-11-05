from datetime import date
from decimal import Decimal
from unittest import TestCase

from . import conv_date
from . import conv_date_inv
from . import fmt_value
from . import read_kv
from .model import KV


class TestMovs(TestCase):
    def test_conv_date(self) -> None:
        expected = conv_date('11/05/1982')
        actual = date(1982, 5, 11)

        self.assertEqual(expected, actual)

    def test_conv_date_invalid(self) -> None:
        expected = conv_date('invalid')
        actual = None

        self.assertEqual(expected, actual)

    def test_conv_date_inv(self) -> None:
        expected = conv_date_inv(date(1982, 5, 11))
        actual = '11/05/1982'

        self.assertEqual(expected, actual)

    def test_read_kv(self) -> None:
        expected = read_kv(iter(('',
                                 '',
                                 ': tipo',
                                 ': conto_bancoposta',
                                 ': intestato_a',
                                 '',
                                 ': 0_____',
                                 ': 0_____')))
        actual = KV(None, None, 'tipo', 'conto_bancoposta',
                    'intestato_a', None, Decimal(0), Decimal(0))

        self.assertEqual(expected, actual)

    def test_fmt_value_none(self) -> None:
        expected = fmt_value(None, lambda _: '')
        actual = ''

        self.assertEqual(expected, actual)

    def test_fmt_value_date(self) -> None:
        expected = fmt_value(date(1982, 5, 11), lambda _: '')
        actual = '11/05/1982'

        self.assertEqual(expected, actual)

    def test_fmt_value_decimal(self) -> None:
        expected = fmt_value(Decimal(1), lambda d: f'_{d}_')
        actual = '_1_'

        self.assertEqual(expected, actual)

    def test_fmt_value_str(self) -> None:
        expected = fmt_value('foo', lambda _: '')
        actual = 'foo'

        self.assertEqual(expected, actual)
