import datetime
import decimal
import itertools
import typing

import iterhelper
import model


def conv_date(dt: str) -> datetime.date:
    return datetime.datetime.strptime(dt, '%d/%m/%Y').date()


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


def read_csv(csv_file: typing.Iterable[str]) -> typing.Iterable[model.Row]:
    field_indexes = list(iterhelper.zip_with_next((1, 18, 32, 50, 69), None))

    def conv_cvs_decimal(dec: str) -> typing.Optional[decimal.Decimal]:
        if not dec:
            return None
        return decimal.Decimal(dec.replace('.', '').replace(',', '.'))

    for row in itertools.islice(csv_file, 1, None):
        els = (row[a:b].rstrip() for a, b in field_indexes)

        data_contabile = conv_date(next(els))
        data_valuta = conv_date(next(els))
        addebiti = conv_cvs_decimal(next(els))
        accrediti = conv_cvs_decimal(next(els))
        descrizione_operazioni = next(els)

        yield model.Row(data_contabile, data_valuta, addebiti, accrediti,
                        descrizione_operazioni)


def read_txt(fn: str) -> typing.Tuple[model.KV, typing.Iterable[model.Row]]:
    with open(fn) as f:
        kv_file = itertools.islice(f, 8)
        csv_file = f
        kv = read_kv(kv_file)
        csv = list(read_csv(csv_file))
        return kv, csv
