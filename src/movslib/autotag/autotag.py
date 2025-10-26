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
    accrediti = row.accrediti
    descrizione_operazioni = row.descrizione_operazioni

    ret = TagRow(
        row.data_contabile,
        row.data_valuta,
        row.addebiti,
        accrediti,
        descrizione_operazioni,
    )

    if accrediti is not None:
        ret.tags.add(Tags.ENTRATE)

    for pattern, tags in {'BONIFICO SEPA': [Tags.BONIFICO]}.items():
        if pattern in descrizione_operazioni and accrediti is not None:
            ret.tags.update(tags)

    for pattern, tags in {
        'COMMISSIONI': [Tags.COMMISSIONI],
        'CANONE': [Tags.COMMISSIONI],
    }.items():
        if descrizione_operazioni.startswith(pattern):
            ret.tags.update(tags)

    for pattern, tags in {
        'AUTOSTRADA': [Tags.AUTOSTRADA],
        'ENEL ENERGIA': [Tags.BOLLETTE, Tags.LUCE],
        'Wind Tre S.p.A.': [Tags.BOLLETTE, Tags.TELEFONO],
        'WIND TRE S P A': [Tags.BOLLETTE, Tags.TELEFONO],
        'SORGENIA S P A': [Tags.BOLLETTE, Tags.GAS],
        **{
            p: [Tags.SPESA]
            for p in ('ESSELUNGA', 'EUROSPIN', 'IPERCOOP', 'SUPERMERCATO')
        },
        'RICARICA POSTEPAY': [Tags.RICARICA_POSTEPAY],
        **{
            p: [Tags.CONDOMINIO]
            for p in (
                'STUDIO RAG. ANDREA IANNUZZI',
                'Gestione ordinaria',
                '-CMAV-',
                'ORDINARIA',
                'anticipata',
                'RIFACIMENTO IMPIANTO VIDEOCITOF',
                'ANTICIPATA',
                'TINTEGGIATURA SCALE',
                'BENEF BANCA DI CREDITO COOPERATIVO PER CAUSALE',
            )
        },
        '1 H CLEAN DI ROZZA GIU': [Tags.LAVANDERIA],
    }.items():
        if pattern in descrizione_operazioni:
            ret.tags.update(tags)

    return ret
