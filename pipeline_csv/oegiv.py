"""Inspection Viewer app behavior."""
from . import ObjectClass, TypeHorWeld
from .csvfile import row, File as FileBase


class TypeMarker:
    """Types of marker."""

    VALVE = 0
    MARKER = 1
    MAGNET = 2
    OTVOD = 3
    TROYNIK = 4
    CASE_START = 5
    CASE_END = 6
    REPAIR = 7
    LOAD = 8
    TURN_START = 9
    TURN_END = 10
    FEATURE = 11
    CURVE_SECTION = 12
    TURN_SEGMENT = 13


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

LINEOBJ = {
  TypeMarker.VALVE: "Кран",
  TypeMarker.MARKER: "Маркер",
  TypeMarker.MAGNET: "Маркер магнитный",
  TypeMarker.OTVOD: "Отвод-врезка",
  TypeMarker.TROYNIK: "Тройник",
  TypeMarker.CASE_START: "Патрон начало",
  TypeMarker.CASE_END: "Патрон конец",
  TypeMarker.REPAIR: "Место ремонта",
  TypeMarker.LOAD: "Пригруз",
  TypeMarker.TURN_START: "Отвод (поворот) начало",
  TypeMarker.TURN_END: "Отвод (поворот) конец",
  TypeMarker.FEATURE: "Особенность",
  TypeMarker.CURVE_SECTION: "Гнутая секция",
  TypeMarker.TURN_SEGMENT: "Сегмент поворота",
}

DEFAULT_MARKERS = [
  TypeMarker.VALVE,
  TypeMarker.MARKER,
  TypeMarker.MAGNET,
]

REVERSE_MARKER = {
  TypeMarker.CASE_START: TypeMarker.CASE_END,
  TypeMarker.CASE_END: TypeMarker.CASE_START,
  TypeMarker.TURN_START: TypeMarker.TURN_END,
  TypeMarker.TURN_END: TypeMarker.TURN_START,
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

    @staticmethod
    def lineobj_dict():
        """Return dict of available lineobject types."""
        return LINEOBJ

    @staticmethod
    def markers_default():
        """Return list of lineobject types that use as markers by default."""
        return DEFAULT_MARKERS

    @staticmethod
    def markers_reverse():
        """Return dict of markers for reverse."""
        return REVERSE_MARKER
