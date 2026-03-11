"""Test b31g_1991.py module.

make test T=test_integrity/test_method/test_asme/test_b31g_1991.py
"""
from . import TestAsme


class TestsReadme1991(TestAsme):
    """Code from readme files."""

    def test_en(self):
        """Code from README.md 1991."""
        pipe = self.pipe_en
        defect = self.defect_en

        from pipeline_csv.integrity.method.asme.b31g_1991 import Context, State

        asme = Context(defect, self.material_en, self.pressure_en)

        # defect depth less than 10% wall thickness, no danger.
        assert defect.depth_mm == 0.039
        assert pipe.thick == 0.63
        assert asme.pipe_state(is_explain=True) == State.Ok
        assert '10%' in asme.explain()

        # the depth of the defect is more than 80% of the pipe wall thickness,
        # repair or replacement of the pipe is necessary.
        defect.depth = 0.6
        assert asme.pipe_state(is_explain=True) == State.Replace
        assert '80%' in asme.explain()

        # the depth of the defect is 50% of the pipe wall thickness, but the length of the defect
        # does not exceed its maximum allowable length.
        # the defect is not dangerous.
        defect.depth = 0.31
        assert defect.length == 4
        assert round(asme.defect_max_length()) == 5
        assert asme.pipe_state() == State.Safe

        # a defect with a length of 20 inches and a depth of 50% of the pipe wall thickness
        # requires repair at the specified working pressure in the pipe.
        defect.length = 20
        assert asme.pipe_state() == State.Repair

        # when the operating pressure is reduced to a safe value, the defect does not require repair.
        assert pipe.maop == 900
        assert round(asme.safe_pressure, 2) == 700.68
        pipe.maop = 700
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
        assert defect.depth_mm == 1
        assert pipe.thick == 160
        assert asme.pipe_state() == State.Ok

        # глубина дефекта более 80% толщины стенки трубы, необходим ремонт или замена трубы.
        defect.row.depth_max = 15 * 100  # 15 mm
        assert asme.pipe_state() == State.Replace

        # глубина дефекта 50% от толщины стенки трубы, но длина дефекта не превышает его
        # максимально допустимую длину.
        # дефект не представляет опасности.
        defect.depth = 8 * 100  # 8 mm
        assert defect.length == 100

        assert round(asme.get_b(), 5) == 0.36295
        assert round(asme.diam_wall, 3) == 150.732
        assert round(1.12 * 150.732 * 0.36295) == 777

        assert round(asme.defect_max_length()) == 127
        assert asme.pipe_state() == State.Safe

        # дефект длиной 500 мм и глубиной 50% от толщины стенки трубы
        # требует ремонта при указанном рабочем давлении в трубе.
        defect.length = 500
        assert asme.pipe_state() == State.Repair

        # при снижении рабочего давления до безопасной величины дефект не требует ремонта.
        assert pipe.maop == 7
        assert round(asme.safe_pressure, 2) == 3.96
        pipe.maop = 3.95

        from pipeline_csv.integrity.i18n import Lang

        lang_ru = asme.lang(Lang.Ru)
        assert asme.pipe_state(is_explain=lang_ru) == State.Defected
        assert 'Дефект не опасен.' in asme.explain()
