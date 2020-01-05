import dataclasses
import datetime
import decimal
import itertools
import logging
import typing


@dataclasses.dataclass
class KV:
    da: datetime.date
    a: datetime.date
    tipo: str
    conto_bancoposta: str
    intestato_a: str
    saldo_al: datetime.date
    saldo_contabile: decimal.Decimal
    saldo_disponibile: decimal.Decimal


@dataclasses.dataclass
class Row:
    data_contabile: datetime.date
    data_valuta: datetime.date
    addebiti: typing.Optional[decimal.Decimal]
    accrediti: typing.Optional[decimal.Decimal]
    descrizione_operazioni: str


def conv_date(dt: str) -> datetime.date:
    return datetime.datetime.strptime(dt, '%d/%m/%Y').date()


def read_kv(kv_file: typing.Iterable[str]) -> KV:
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


T = typing.TypeVar('T')


def zip_with_next(it: typing.Iterable[T],
                  last: T
                  ) -> typing.Iterable[typing.Tuple[T, T]]:
    c = itertools.chain(it, (last, ))
    next(c)
    return zip(it, c)


def read_csv(csv_file: typing.Iterable[str]) -> typing.Iterable[Row]:
    field_indexes = list(zip_with_next((1, 18, 32, 50, 69), None))

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

        yield Row(data_contabile, data_valuta, addebiti, accrediti,
                  descrizione_operazioni)


def read_txt(fn: str) -> typing.Tuple[KV, typing.Iterable[Row]]:
    with open(fn) as f:
        kv_file = itertools.islice(f, 8)
        csv_file = f
        kv = read_kv(kv_file)
        csv = list(read_csv(csv_file))
        return kv, csv


def main() ->None:
    fn = 'resources/BPOL_Lista_Movimenti.txt'
    kv, csv = read_txt(fn)
    logging.warning('kv: %s', kv)
    for row in csv:
        logging.warning('row: %s', row)


if __name__ == '__main__':
    main()
