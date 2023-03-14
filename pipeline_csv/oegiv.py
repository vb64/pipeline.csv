"""Inspection Viewer app behavior."""
from . import ObjectClass, TypeHorWeld
from .csvfile import row, File as FileBase


class TypeDefekt:
    """Types of defekt."""

    CORROZ = 0
    MECHANIC = 1
    DENT = 2
    DENT_METAL_LOSS = 3
    GOFRA = 4
    GWAN = 5
    TECHNOLOGY = 6
    FACTORY = 7
    ADDITIONAL_METAL = 8
    OTHER = 9
    CRACKS_HOR = 10
    CRACK_LIKE = 11
    CRACK_WELD = 12
    LAMINATION = 13
    ANOMALY_HOR_WELD = 14
    ANOMALY_SPIRAL_WELD = 15
    ELLIPSE = 16
    PODZHIG = 17
    GRINDING = 18


DEFEKTS = {
  TypeDefekt.CORROZ: "Коррозия",
  TypeDefekt.MECHANIC: "Мех. повреждение",
  TypeDefekt.DENT: "Вмятина",
  TypeDefekt.DENT_METAL_LOSS: "Вмятина с дефектами потери металла",
  TypeDefekt.GOFRA: "Гофра",
  TypeDefekt.GWAN: "Аномалия кольцевого шва",
  TypeDefekt.TECHNOLOGY: "Технологический дефект",
  TypeDefekt.FACTORY: "Заводской дефект",
  TypeDefekt.ADDITIONAL_METAL: "Дополнительный металл/материал",
  TypeDefekt.OTHER: "Другое",
  TypeDefekt.CRACKS_HOR: "Зона продольных трещин",
  TypeDefekt.CRACK_LIKE: "Трещиноподобный дефект",
  TypeDefekt.CRACK_WELD: "Трещина на кольцевом шве",
  TypeDefekt.LAMINATION: "Расслоение",
  TypeDefekt.ANOMALY_HOR_WELD: "Аномалия продольного шва",
  TypeDefekt.ANOMALY_SPIRAL_WELD: "Аномалия спирального шва",
  TypeDefekt.ELLIPSE: "Эллипсность",
  TypeDefekt.PODZHIG: "Поджиг",
  TypeDefekt.GRINDING: "Зашлифовка",
}

COMMON = {
  ObjectClass.WELD: "Шов",
  ObjectClass.THICK: "Изменение толщины стенки трубы",
  ObjectClass.PIPELINE_CATEGORY: "Категория трубопровода",
}

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

    @staticmethod
    def name_object(code):
        """Return text for object_code_t field."""
        return COMMON[code]

    @staticmethod
    def defekts_dict():
        """Return dict of available defekts types."""
        return DEFEKTS
