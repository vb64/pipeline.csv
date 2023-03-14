"""Interfaces for InspectionViewer stuff."""


def attr_list(cls):
    """Return list of attributes values for class."""
    return [val for key, val in vars(cls).items() if not key.startswith('_')]


class Error(Exception):
    """IV exception."""

    pass


class ObjectClass:
    """Classes of csv objects."""

    WELD = 0
    MARKER = 1
    DEFEKT = 2
    THICK = 3
    HOR_WELD = 4
    PIPELINE_CATEGORY = 5


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


class TypeHorWeld:
    """Types of horizontal weld."""

    HORIZONTAL = 0
    SECOND = 1
    NO_WELD = 2
    SPIRAL = 3
    UNKNOWN = 4


class DefektSide:
    """Types of defekt location."""

    UNKNOWN = 0
    OUTSIDE = 1
    INSIDE = 2
    IN_WALL = 3


SEAMS = attr_list(TypeHorWeld)

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

DEFAULT_MARKERS = [
  TypeMarker.VALVE,
  TypeMarker.MARKER,
  TypeMarker.MAGNET,
]
