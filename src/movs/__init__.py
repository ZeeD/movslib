import decimal
import itertools
from dataclasses import fields
from datetime import date
from datetime import datetime
from typing import Callable
from typing import cast
from typing import Iterable
from typing import Optional
from typing import TextIO
from typing import Tuple
from typing import Union

from .iterhelper import zip_with_next
from .model import KV
from .model import Row

csv_field_indexes = list(zip_with_next((1, 18, 32, 50, 69), None))


def conv_date(dt: str) -> Optional[date]:
    try:
        return datetime.strptime(dt, '%d/%m/%Y').date()
    except ValueError:
        return None


def conv_date_inv(d: date) -> str:
    return d.strftime('%d/%m/%Y')


def read_kv(kv_file: Iterable[str]) -> KV:

    def next_token() -> str:
        return next(iter(kv_file)).rstrip().split(': ')[-1]

    def conv_kv_decimal(dec: str) -> decimal.Decimal:
        return decimal.Decimal(dec.replace('.', '').replace(',', '.')[:-5])

    da = conv_date(next_token())
    a = conv_date(next_token())
    tipo = next_token()
    conto_bancoposta = next_token()
    intestato_a = next_token()
    saldo_al = conv_date(next_token())
    saldo_contabile = conv_kv_decimal(next_token())
    saldo_disponibile = conv_kv_decimal(next_token())

    return KV(da, a, tipo, conto_bancoposta, intestato_a, saldo_al,
              saldo_contabile, saldo_disponibile)


def fmt_value(type_: type,
              e: Union[date, decimal.Decimal, None, str],
              conv_decimal_inv: Callable[[decimal.Decimal], str]) -> str:
    if type_ is date or type_ is Optional[date]:
        if e is None:
            return ''
        return conv_date_inv(cast(date, e))

    if type_ is decimal.Decimal or type_ is Optional[decimal.Decimal]:
        if e is None:
            return ''
        return conv_decimal_inv(cast(decimal.Decimal, e))

    return str(e)


def write_kv(f: TextIO, kv: KV) -> None:
    def conv_kv_decimal_inv(d: decimal.Decimal) -> str:
        fmtd = f'{d:,}'.replace(',', '_').replace('.', ',').replace('_', '.')
        return f'+{fmtd} Euro'

    for field in fields(KV):
        field_key_str = {
            'da': 'da: (gg/mm/aaaa)',
            'a': ' a: (gg/mm/aaaa)',
            'tipo': ' Tipo(operazioni)',
            'conto_bancoposta': ' Conto BancoPosta n.',
            'intestato_a': ' Intestato a',
            'saldo_al': ' Saldo al',
            'saldo_contabile': ' Saldo contabile',
            'saldo_disponibile': ' Saldo disponibile',
        }[field.name]

        value = getattr(kv, field.name)
        kv_str = fmt_value(field.type, value, conv_kv_decimal_inv)
        f.write(f'{field_key_str}: {kv_str}\n')


def read_csv(csv_file: Iterable[str]) -> Iterable[Row]:

    def conv_cvs_decimal(dec: str) -> Optional[decimal.Decimal]:
        if not dec:
            return None
        return decimal.Decimal(dec.replace('.', '').replace(',', '.'))

    for row in itertools.islice(csv_file, 1, None):
        els = (row[a:b].rstrip() for a, b in csv_field_indexes)

        data_contabile = conv_date(next(els))
        data_valuta = conv_date(next(els))
        addebiti = conv_cvs_decimal(next(els))
        accrediti = conv_cvs_decimal(next(els))
        descrizione_operazioni = next(els)

        if data_contabile is None:
            raise ValueError()
        if data_valuta is None:
            raise ValueError()

        yield Row(data_contabile, data_valuta, addebiti, accrediti,
                  descrizione_operazioni)


def write_csv(f: TextIO, csv: Iterable[Row]) -> None:
    def conv_csv_decimal_inv(d: decimal.Decimal) -> str:
        fmtd = f'{d:,}'.replace(',', '_').replace('.', ',').replace('_', '.')
        return fmtd

    f.write(' Data Contabile'
            '   Data Valuta'
            '   Addebiti (euro)'
            '   Accrediti (euro)'
            '   Descrizione operazioni\n')
    for row in csv:
        f.write(' ')
        for (a, b), field in zip(csv_field_indexes, fields(Row)):
            value = getattr(row, field.name)
            row_str = fmt_value(field.type, value, conv_csv_decimal_inv)
            if b is not None:
                diff = b - a
                f.write('%*.*s' % (-diff, diff, row_str))
            else:
                f.write(row_str)

        f.write('\n')


def read_txt(fn: str) -> Tuple[KV, list[Row]]:
    with open(fn, encoding='UTF-8') as f:
        kv_file = itertools.islice(f, 8)
        csv_file = f
        kv = read_kv(kv_file)
        csv = list(read_csv(csv_file))
        return kv, csv


def write_txt(fn: str, kv: KV, csv: Iterable[Row]) -> None:
    with open(fn, 'w', encoding='UTF-8') as f:
        write_kv(f, kv)
        write_csv(f, csv)
