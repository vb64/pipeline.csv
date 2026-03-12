"""Test b31g_2012.py module.

make test T=test_integrity/test_method/test_asme/test_b31g_2012.py
"""
from . import TestAsme  # , inch


class TestsReadme2012(TestAsme):
    """Code from readme files."""

    def test_ru(self):
        """Code from READMEru.md 2012."""
        pipe = self.pipe_ru
        defect = self.defect_ru

        from pipeline_csv.integrity.method.asme.b31g_2012 import Context

        assert self.material_ru.smys == 295
        self.material_ru.smts = 420

        asme = Context(defect, self.material_ru, self.pressure_ru)

        assert defect.depth_mm == 1
        assert pipe.thick_mm == 16
        assert asme.design_factor == 1.0
        asme.maop = 8.5

        assert asme.years() > 1
        assert 0.94 < asme.erf() < 0.97

        asme.maop = 0.01
        assert asme.years() == Context.REPAIR_NOT_REQUIRED
        asme.maop = 20

        defect.row.depth_max = 8 * 100
        assert defect.depth_mm == 8

        defect.row.length = 200
        assert asme.years() == 0
        assert asme.erf() > 1

        # assert asme.maop == 7
        assert round(asme.safe_pressure, 2) > 6
        asme.maop = asme.safe_pressure - 0.1

        from pipeline_csv.integrity.i18n import Lang

        asme.is_explain = asme.lang(Lang.Ru)
        assert round(asme.erf(), 3) in [0.991, 0.984, 0.985]
        assert round(asme.safe_pressure, 1) in [11.5, 6.2, 6.5]
        assert asme.years() > 0

        asme.design_factor = 0.72

        assert round(asme.erf(), 3) == 1.377
        assert round(asme.safe_pressure, 1) in [8.3, 4.5, 4.7]
        assert asme.years() == 0
