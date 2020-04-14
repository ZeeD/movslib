import dataclasses
import datetime
import decimal
import itertools
import typing

from . import iterhelper
from . import model


csv_field_indexes = list(iterhelper.zip_with_next((1, 18, 32, 50, 69), None))


def conv_date(dt: str) -> typing.Optional[datetime.date]:
    try:
        return datetime.datetime.strptime(dt, '%d/%m/%Y').date()
    except ValueError:
        return None


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
    def tostr(type_: type,
              e: typing.Union[datetime.date,
                              decimal.Decimal,
                              None,
                              str]) -> str:
        if type_ is datetime.date:
            return conv_date_inv(typing.cast(datetime.date, e))
        if type_ is decimal.Decimal:
            return str(e).replace('.', ',') + '_' * 5
        return str(e)

    for field in dataclasses.fields(model.KV):
        f.write(f'{field.name}: {tostr(field.type, getattr(kv, field.name))}\n')


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

        if data_contabile is None:
            raise ValueError()
        if data_valuta is None:
            raise ValueError()

        yield model.Row(data_contabile, data_valuta, addebiti, accrediti,
                        descrizione_operazioni)


def write_csv(f: typing.TextIO, csv: typing.Iterable[model.Row]) -> None:
    def tostr(type_: type,
              e: typing.Union[datetime.date,
                              None,
                              decimal.Decimal,
                              str]) -> str:
        if type_ is datetime.date:
            return conv_date_inv(typing.cast(datetime.date, e))
        if type_ is typing.Optional[decimal.Decimal]:
            return '' if e is None else str(e).replace('.', ',')
        return str(e)

    f.write('\n')
    for row in csv:
        f.write(' ')
        for (a, b), field in zip(csv_field_indexes,
                                 dataclasses.fields(model.Row)):
            row_str = tostr(field.type, getattr(row, field.name))
            if b is not None:
                l = b - a
                f.write('%*.*s' % (-l, l, row_str))
            else:
                f.write(row_str)

        f.write('\n')


def read_txt(fn: str) -> typing.Tuple[model.KV, typing.Sequence[model.Row]]:
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
