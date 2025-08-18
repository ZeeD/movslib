from typing import TYPE_CHECKING

from movslib.autotag.model import TagRow
from movslib.autotag.model import TagRows
from movslib.autotag.model import Tags

if TYPE_CHECKING:
    from movslib.model import Row
    from movslib.model import Rows


def autotag(rows: 'Rows') -> TagRows:
    return TagRows(rows.name, map(_autotag_row, rows))


def _autotag_row(row: 'Row') -> TagRow:
    """Add zero, one, or more tags to a row, based on patterns."""
    ret = TagRow(
        row.data_contabile,
        row.data_valuta,
        row.addebiti,
        row.accrediti,
        row.descrizione_operazioni,
    )

    if (
        'BONIFICO SEPA' in row.descrizione_operazioni
        and row.accrediti is not None
    ):
        ret.tags.add(Tags.BONIFICO)

    if row.descrizione_operazioni.startswith('COMMISSIONI'):
        ret.tags.add(Tags.COMMISSIONI)
    if row.descrizione_operazioni.startswith('CANONE'):
        ret.tags.add(Tags.COMMISSIONI)

    if 'AUTOSTRADA' in row.descrizione_operazioni:
        ret.tags.add(Tags.AUTOSTRADA)

    if 'ENEL ENERGIA' in row.descrizione_operazioni:
        ret.tags.add(Tags.BOLLETTE)
        ret.tags.add(Tags.LUCE)

    if 'Wind Tre S.p.A.' in row.descrizione_operazioni:
        ret.tags.add(Tags.BOLLETTE)
        ret.tags.add(Tags.TELEFONO)

    if 'SORGENIA S P A' in row.descrizione_operazioni:
        ret.tags.add(Tags.BOLLETTE)
        ret.tags.add(Tags.GAS)

    return ret
