"""Interfaces for InspectionViewer stuff."""


def attr_list(cls):
    """Return list of attributes values for class."""
    return [val for key, val in vars(cls).items() if not key.startswith('_')]


class Error(Exception):
    """Package exception."""

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

DEFAULT_MARKERS = [
  TypeMarker.VALVE,
  TypeMarker.MARKER,
  TypeMarker.MAGNET,
]
