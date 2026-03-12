"""Root class for testing ASME methods."""
from .. import TestMethod


def inch(val, suff=1):
    """Return inches as mm with optional multiplier."""
    return float(val) * 25.4 * suff


class TestAsme(TestMethod):
    """Base class for tests ASME methods."""

    def setUp(self):
        """Set up test data."""
        super().setUp()

        from pipeline_csv.integrity.material import PipeMaterial
        from pipeline_csv.csvfile import Stream
        from pipeline_csv.csvfile.row import Depth
        from pipeline_csv.csvfile.tubes import Tube
        from pipeline_csv import DefektSide
        from pipeline_csv.orientation import Orientation
        from pipeline_csv.oegiv import TypeDefekt, Row as BaseRow

        class Row(BaseRow):
            """Row with mm depth."""

            depth_units = Depth.HundredthsOfMillimeter

        self.material_en = PipeMaterial(
          "Steel",
          52000  # SMYS psi
        )
        self.pressure_en = 900  # pressure psi

        self.pipe_en = Tube(Row.as_weld(10), Stream(diameter=inch(56)), None)
        assert self.pipe_en.diameter == inch(56)  # diameter 56 inches
        self.pipe_en.length = inch(440)  # length inches
        self.pipe_en.thick_mm = inch(0.63)  # wall thickness inches

        self.pipe_en.add_object(
          Row.as_defekt(
            inch(40),  # the defect starts at a distance of 40 inches from the beginning of the pipe
            TypeDefekt.CORROZ,
            DefektSide.INSIDE,
            inch(4),  # defect length 4 inches
            inch(1),  # width
            str(inch(0.039, 100)),  # defect depth 0.039 inches
            # along the circumference of the pipe, the defect begins
            # at 10 arc minutes from the top of the pipe
            Orientation.from_minutes(10),
            # the size of the defect along the circumference is 20 arc minutes
            Orientation.from_minutes(10 + 20),
            None,  # MPoint orient
            None,  # MPoint dist
            ''  # comment
          )
        )
        self.defect_en = self.pipe_en.defects[-1]

        self.material_ru = PipeMaterial(
          "Сталь",
          295  # предел текучести Мпа
        )
        self.pressure_ru = 7  # рабочее давление Мпа

        self.pipe_ru = Tube(Row.as_weld(10), Stream(diameter=1420), None)
        assert self.pipe_ru.diameter == 1420  # диаметр 1420 мм
        self.pipe_ru.length = 11200  # длина 11.2 метра
        self.pipe_ru.thick_mm = 16

        self.pipe_ru.add_object(
          Row.as_defekt(
            1000,  # дефект начинается на расстоянии 1 метра от начала трубы
            TypeDefekt.CORROZ,
            DefektSide.INSIDE,
            100,  # длина дефекта 100 мм
            10,  # ширина дефекта 10 мм
            str(1 * 100),  # глубина дефекта 1 мм
            # по окружности трубы дефект начинается на 10 угловых минут от верхней точки трубы
            Orientation.from_minutes(10),
            # размер дефекта по окружности составляет 20 угловых минут
            Orientation.from_minutes(10 + 20),
            None,  # MPoint orient
            None,  # MPoint dist
            ''  # comment
          )
        )
        self.defect_ru = self.pipe_ru.defects[-1]
