"""Inspection Viewer app behavior."""
from . import TypeHorWeld
from .csvfile import row, File as FileBase

SEAM = {
  TypeHorWeld.HORIZONTAL: "Продольный шов",
  TypeHorWeld.SECOND: "Двойной прод. шов",
  TypeHorWeld.NO_WELD: "Цельнотянутая труба",
  TypeHorWeld.SPIRAL: "Спиральный шов",
  TypeHorWeld.UNKNOWN: "Не определено",
}


class File(FileBase):
    """Export/import Deftable.csv file."""

    ENCODING = 'windows-1251'


class Row(row.Row):
    """Row of Deftable.csv file."""

    @staticmethod
    def name_seam(code):
        """Return text for seam object_code_t field."""
        return SEAM[code]
