import datetime
import decimal
import itertools
import typing

from . import iterhelper
from . import model
import dataclasses

csv_field_indexes = list(iterhelper.zip_with_next((1, 18, 32, 50, 69), None))


def conv_date(dt: str) -> datetime.date:
    return datetime.datetime.strptime(dt, '%d/%m/%Y').date()


def conv_date_inv(d: datetime.date) -> str:
    return d.strftime('%d/%m/%Y')


def read_kv(kv_file: typing.Iterable[str]) -> model.KV:

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

    return model.KV(da, a, tipo, conto_bancoposta, intestato_a, saldo_al,
                    saldo_contabile, saldo_disponibile)


def write_kv(f: typing.TextIO, kv: model.KV) -> None:
    for field in dataclasses.fields(model.KV):
        if field.type is datetime.date:
            tostr = conv_date_inv
        elif field.type is decimal.Decimal:
            tostr = lambda d: str(d).replace('.', ',') + '_' * 5
        else:
            tostr = lambda x: x
        f.write(f'{field.name}: {tostr(getattr(kv, field.name))}\n')


def read_csv(csv_file: typing.Iterable[str]) -> typing.Iterable[model.Row]:

    def conv_cvs_decimal(dec: str) -> typing.Optional[decimal.Decimal]:
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

        yield model.Row(data_contabile, data_valuta, addebiti, accrediti,
                        descrizione_operazioni)


def write_csv(f: typing.TextIO, csv: typing.Iterable[model.Row]) -> None:
    f.write('\n')
    for row in csv:
        f.write(' ')
        for (a, b), field in zip(csv_field_indexes, dataclasses.fields(model.Row)):
            if field.type is datetime.date:
                tostr = conv_date_inv
            elif field.type is typing.Optional[decimal.Decimal]:
                tostr = lambda d: '' if d is None else str(d).replace('.', ',')
            else:
                tostr = lambda x: x

            if b is not None:
                l = b-a
                f.write('%*.*s' % (-l, l, tostr(getattr(row, field.name))))
            else:
                f.write(tostr(getattr(row, field.name)))

        f.write('\n')


def read_txt(fn: str) -> typing.Tuple[model.KV, typing.Iterable[model.Row]]:
    with open(fn) as f:
        kv_file = itertools.islice(f, 8)
        csv_file = f
        kv = read_kv(kv_file)
        csv = list(read_csv(csv_file))
        return kv, csv


def write_txt(fn: str, kv: model.KV, csv: typing.Iterable[model.Row]) -> None:
    with open(fn, 'w') as f:
        write_kv(f, kv)
        write_csv(f, csv)
