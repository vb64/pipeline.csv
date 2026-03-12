"""Test b31g_1991.py module.

make test T=test_integrity/test_method/test_asme/test_b31g_1991.py
"""
from . import TestAsme, inch


class TestsReadme1991(TestAsme):
    """Code from readme files."""

    def test_en(self):
        """Code from README.md 1991."""
        pipe = self.pipe_en
        defect = self.defect_en

        from pipeline_csv.integrity.method.asme.b31g_1991 import Context, State

        asme = Context(defect, self.material_en, self.pressure_en)

        # defect depth less than 10% wall thickness, no danger.
        assert round(defect.depth_mm) == round(inch(0.039))
        assert pipe.thick_mm == 16  # inch(0.63)
        assert asme.pipe_state(is_explain=True) == State.Ok
        assert '10%' in asme.explain()

        # the depth of the defect is more than 80% of the pipe wall thickness,
        # repair or replacement of the pipe is necessary.
        defect.row.depth_max = inch(0.6, 100)
        assert asme.pipe_state(is_explain=True) == State.Replace
        assert '80%' in asme.explain()

        # the depth of the defect is 50% of the pipe wall thickness, but the length of the defect
        # does not exceed its maximum allowable length.
        # the defect is not dangerous.
        defect.row.depth_max = inch(0.31, 100)
        assert defect.length == 101  # inch(4)
        assert round(asme.defect_max_length()) == 129
        assert asme.pipe_state() == State.Safe

        # a defect with a length of 20 inches and a depth of 50% of the pipe wall thickness
        # requires repair at the specified working pressure in the pipe.
        defect.length = inch(20)
        assert defect.length == inch(20)
        assert asme.pipe_state() == State.Repair

        # when the operating pressure is reduced to a safe value, the defect does not require repair.
        assert asme.maop == 900
        assert round(asme.safe_pressure, 2) == 700.56
        asme.maop = 700
        assert asme.pipe_state(is_explain=True) == State.Defected
        assert 'defect is not dangerous' in asme.explain()

    def test_ru(self):
        """Code from READMEru.md."""
        pipe = self.pipe_ru
        defect = self.defect_ru

        from pipeline_csv.integrity.method.asme.b31g_1991 import Context, State
        from pipeline_csv.csvfile.row import Depth

        assert defect.row.depth_units == Depth.HundredthsOfMillimeter

        asme = Context(defect, self.material_ru, self.pressure_ru)

        # глубина дефекта менее 10% толщины стенки трубы, опасности нет.
        assert defect.row.depth_max == 100
        assert defect.depth_percent == 6.25
        assert defect.depth_mm == 1
        assert pipe.thick_mm == 16
        assert asme.pipe_state() == State.Ok

        # глубина дефекта более 80% толщины стенки трубы, необходим ремонт или замена трубы.
        defect.row.depth_max = 15 * 100  # 15 mm
        assert defect.depth_mm == 15
        assert defect.depth_percent == 93.75
        assert asme.pipe_state() == State.Replace

        # глубина дефекта 50% от толщины стенки трубы, но длина дефекта не превышает его
        # максимально допустимую длину.
        # дефект не представляет опасности.
        defect.row.depth_max = 8 * 100  # 8 mm
        assert defect.depth_percent == 50.0
        assert defect.depth_mm == 8
        assert defect.length == 100

        assert asme.relative_depth == 50.0
        assert round(asme.get_b(), 5) == 0.75
        assert round(asme.diam_wall, 3) == 150.732

        assert round(asme.defect_max_length()) == 127
        assert asme.pipe_state() == State.Safe

        # дефект длиной 500 мм и глубиной 50% от толщины стенки трубы
        # требует ремонта при указанном рабочем давлении в трубе.
        defect.length = 500
        assert defect.length == 500
        assert asme.pipe_state() == State.Repair

        # при снижении рабочего давления до безопасной величины дефект не требует ремонта.
        assert asme.maop == 7
        assert round(asme.safe_pressure, 2) == 3.96
        asme.maop = 3.95

        from pipeline_csv.integrity.i18n import Lang

        lang_ru = asme.lang(Lang.Ru)
        assert asme.pipe_state(is_explain=lang_ru) == State.Defected
        assert 'Дефект не опасен.' in asme.explain()


class TestsCrvlBas(TestAsme):
    """Examples from CRVL.BAS."""

    def setUp(self):  # pylint: disable=too-many-locals
        """All units as inches."""
        super().setUp()
        from pipeline_csv.integrity.material import PipeMaterial
        from pipeline_csv.integrity.method.asme.b31g_1991 import Context, State
        from pipeline_csv.csvfile.row import Depth
        from pipeline_csv.csvfile import Stream
        from pipeline_csv.csvfile.tubes import Tube
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import TypeDefekt, Row as BaseRow
        from pipeline_csv.orientation import Orientation

        class Row(BaseRow):
            """Row with mm depth."""

            depth_units = Depth.HundredthsOfMillimeter

        self.state = State

        maop = 910  # Lbs/sq.in.
        diam = inch(30)
        wallthick = inch(0.438)
        smys = 52000  # Lbs/sq.in.

        self.material = PipeMaterial("Steel", smys)
        self.pipe = Tube(Row.as_weld(50), Stream(diameter=diam), None)
        assert self.pipe.diameter == diam
        self.pipe.length = inch(440)  # length inches
        self.pipe.thick_mm = wallthick

        depth = inch(0.1, 100)
        length = inch(7.5)

        self.pipe.add_object(
          Row.as_defekt(
            inch(40),  # the defect starts at a distance of 40 inches from the beginning of the pipe
            TypeDefekt.CORROZ,
            DefektSide.INSIDE,
            length,  # defect length 4 inches
            inch(1),  # width
            str(depth),  # defect depth 0.039 inches
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
        self.defect = self.pipe.defects[-1]
        self.asme = Context(self.defect, self.material, maop)

    def test_example1(self):
        """Example 1."""
        assert not self.asme.is_ok
        assert not self.asme.is_replace
        assert round(self.asme.get_a(self.defect.length), 3) == 1.7
        assert round(self.asme.get_safe_pressure()) == 1091
        assert round(self.asme.defect_max_length(), 3) == 207.587  # inch(8.216)
        assert self.asme.pipe_state() == self.state.Safe

        self.defect.row.depth_max = inch(0.249, 100)
        assert round(self.asme.defect_max_length(), 3) == 67.41  # inch(2.663)
        assert self.asme.pipe_state() == self.state.Defected

    def test_example2(self):
        """Example 2."""
        self.material.smys = 35000
        self.pipe.diameter = inch(20)
        self.pipe.thick_mm = inch(0.25)
        self.asme.maop = 400
        self.defect.row.depth_max = inch(0.18, 100)
        self.defect.length = inch(10)
        self.asme.design_factor = 0.5

        assert not self.asme.is_ok
        assert not self.asme.is_replace
        assert round(self.asme.defect_max_length(), 3) == 32.713  # inch(1.271)
        assert round(self.asme.get_a(self.defect.length), 3) == 3.666  # 3.993
        assert round(self.asme.get_design_pressure()) == 441
        assert round(self.asme.get_safe_pressure()) == 290  # 284
        assert self.asme.pipe_state() == self.state.Repair

        self.asme.maop = 285
        assert self.asme.pipe_state() == self.state.Defected
        assert not self.asme.is_ok
        assert not self.asme.is_replace
        assert round(self.asme.defect_max_length(), 2) == 32.71
        assert self.defect.length == 254
        assert self.asme.anomaly.length == 254
        assert round(self.asme.safe_pressure) == 290

    def test_example3(self):
        """Example 3."""
        self.pipe.diameter = inch(24)
        self.pipe.thick_mm = inch(0.432)
        self.defect.row.depth_max = inch(0.13, 100)
        self.asme.maop = 910
        self.defect.length = inch(30)

        assert round(self.asme.get_safe_pressure()) == 1040
        assert round(self.asme.defect_max_length(), 3) == 122.189  # inch(4.789) INFINITY ?
        assert round(self.asme.get_a(self.defect.length), 3) == 7.658
        assert round(self.asme.get_design_pressure()) == 1351

        self.defect.row.depth_max = inch(0.167, 100)
        assert round(self.asme.defect_max_length(), 3) == 90.703  # inch(3.557)

    def test_example4(self):
        """Example 4."""
        self.pipe.diameter = inch(24)
        self.pipe.thick_mm = inch(0.432)
        self.defect.row.depth_max = inch(0.3, 100)
        self.defect.length = inch(30)
        self.asme.maop = 910

        assert round(self.asme.get_a(self.defect.length), 3) == 7.658
        assert round(self.asme.get_design_pressure()) == 1351
        assert round(self.asme.get_safe_pressure()) == 457
        assert round(self.asme.defect_max_length(), 3) == 48.636  # inch(1.907)

        assert self.asme.pipe_state() == self.state.Repair
        assert round(self.asme.safe_pressure) == 457

        self.asme.maop = 452
        assert self.asme.pipe_state() == self.state.Defected

    def test_example5(self):
        """Example 5."""
        self.pipe.diameter = inch(24)
        self.pipe.thick_mm = inch(0.281)
        self.defect.row.depth_max = inch(0.08, 100)
        self.defect.length = inch(15)
        self.asme.maop = 731

        assert round(self.asme.get_a(self.defect.length), 3) == 4.766
        assert round(self.asme.get_design_pressure()) == 872
        assert round(self.asme.get_safe_pressure()) == 685

        assert self.asme.pipe_state() == self.state.Repair
        assert round(self.asme.safe_pressure) == 685

    def test_example6(self):
        """Example 6."""
        self.asme.maop = 1000
        self.pipe.diameter = inch(36)
        self.pipe.thick_mm = inch(0.5)
        self.defect.row.depth_max = inch(0.41, 100)
        self.defect.length = inch(100)

        assert self.asme.is_replace
        assert self.asme.pipe_state() == self.state.Replace

    def test_example7(self):
        """Example 7."""
        self.asme.maop = 877
        self.pipe.diameter = inch(12.625)
        self.pipe.thick_mm = inch(0.5)
        self.asme.material.smys = 35000
        self.asme.design_factor = 0.4
        self.defect.row.depth_max = inch(0.035, 100)
        self.defect.length = inch(3)

        assert self.asme.is_ok
        assert self.asme.pipe_state() == self.state.Ok

    def test_example8(self):
        """Example 8."""
        self.pipe.diameter = inch(24)
        self.pipe.thick_mm = inch(0.5)
        self.asme.material.smys = 42000
        self.asme.design_factor = 0.5
        self.asme.maop = 790
        self.defect.row.depth_max = inch(0.125, 100)
        self.defect.length = inch(12)

        assert round(self.asme.get_a(self.defect.length), 3) == 2.843


class TestsAsme1991(TestAsme):
    """Method asme b31g edition 1991."""

    def setUp(self):
        """Make functions tests data."""
        super().setUp()
        self.defect = self.defect_ru
        self.pipe = self.defect.pipe

        self.defect.row.depth_max = 1 * 100  # 1 mm
        self.defect.length = 100
        self.pipe.thick_mm = 10

    def test_context(self):
        """Check context method name."""
        from pipeline_csv.integrity.method.asme.b31g_1991 import Context

        asme = Context(self.defect, self.material_ru, self.pressure_ru)
        assert asme.name == "ASME B31G 1991"

    def test_pipe_state(self):
        """Check property pipe_state."""
        from pipeline_csv.integrity.method.asme.b31g_1991 import Context, State

        asme = Context(self.defect, self.material_ru, self.pressure_ru)
        assert asme.pipe_state() == State.Ok

        self.defect.row.depth_max = 9 * 100  # 9 mm
        assert asme.pipe_state() == State.Replace

        self.defect.row.depth_max = 5 * 100  # 5 mm
        assert asme.pipe_state() == State.Safe

    def test_get_b(self):
        """Check function get_b."""
        from pipeline_csv.integrity.method.asme.b31g_1991 import Context

        self.defect.row.depth_max = 1.5 * 100  # 1.5 mm

        asme = Context(self.defect, self.material_ru, self.pressure_ru)
        assert round(asme.relative_depth, 1) == 15.0
        assert round(asme.get_b(), 1) == 4.0

        self.defect.row.depth_max = 5 * 100  # 5 mm
        assert round(asme.relative_depth, 1) == 50.0
        assert round(asme.get_b(), 1) == 0.8

    def test_defect_max_length(self):
        """Check function defect_max_length."""
        from pipeline_csv.integrity.method.asme.b31g_1991 import Context

        self.defect.row.depth_max = 1.5 * 100  # 1.5 mm
        asme = Context(self.defect, self.material_ru, self.pressure_ru)

        assert round(asme.defect_max_length(), 1) == 533.9

        self.defect.row.depth_max = 5 * 100  # 5 mm
        assert round(asme.defect_max_length(), 1) == 100.1

    def test_lang(self):
        """Check function lang."""
        from pipeline_csv.integrity.i18n import Lang
        from pipeline_csv.integrity.method.asme.b31g_1991 import Context

        asme = Context(self.defect, self.material_ru, self.pressure_ru)
        assert len(asme.lang(Lang.Ru)) > 1
