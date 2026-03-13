"""Test b31g_2012.py module.

make test T=test_integrity/test_method/test_asme/test_b31g_2012.py
"""
import pytest
from . import TestAsme, inch


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

        defect.depth_mm = 8
        defect.length = 200
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

    def test_en(self):
        """Code from README.md 2012."""
        pipe = self.pipe_en
        defect = self.defect_en

        from pipeline_csv.integrity.method.asme.b31g_2012 import Context, ErrMaterialSMTSNotDefined

        with pytest.raises(ErrMaterialSMTSNotDefined) as err:
            Context(defect, self.material_en, self.pressure_en)
        assert 'SMTS not defined' in str(err.value)

        self.material_en.smts = 1.5 * self.material_en.smys
        # to inches
        Context.corrosion_rate = Context.corrosion_rate / 25.4

        asme = Context(defect, self.material_en, self.pressure_en)

        # defect depth less than 10% wall thickness, no danger.
        assert round(defect.depth_mm) == round(inch(0.039))
        assert defect.length == 101  # inch(4)
        assert pipe.thick_mm == 16  # inch(0.63)

        asme.maop = 1125
        assert asme.years() > 0
        # classic
        assert 0.7 < asme.erf() < 0.72
        # modified
        assert round(asme.erf(is_mod=True), 3) == 0.749

        asme.maop = 1
        assert asme.years() == Context.REPAIR_NOT_REQUIRED
        asme.maop = 900

        # the depth of the defect is more than 80% of the pipe wall thickness
        defect.depth_mm = inch(0.6)
        assert round(asme.erf(), 3) == 0.598

        # the depth of the defect is 50% of the pipe wall thickness
        defect.depth_mm = inch(0.31)
        assert defect.length == 101  # inch(4)
        assert 0.59 < asme.erf() < 0.60

        # a defect with a length of 30 inches and a depth of 50% of the pipe wall thickness
        defect.length = inch(30)
        assert asme.years() == 0
        assert asme.erf() >= 1

        assert asme.maop == 900
        # assert round(asme.safe_pressure, 2) == 653.71
        asme.maop = 500
        asme.is_explain = True
        assert asme.years() == 0


class Tests2012(TestAsme):
    """Class B31G_2012 methods."""

    def setUp(self):
        """Set up test data."""
        super().setUp()
        from pipeline_csv.integrity.method.asme.b31g_2012 import Context

        self.material_en.smts = 1.5 * self.material_en.smys
        self.asme = Context(self.defect_en, self.material_en, self.pressure_en)

    def test_str(self):
        """Check method str."""
        assert 'ASME B31G' in str(self.asme)

    def test_s_flow(self):
        """Check method s_flow."""
        self.asme.material.smts = 1.01 * self.asme.material.smys

        assert self.asme.s_flow() == self.asme.material.smts

    def test_get_stress_fail_mod(self):
        """Check method get_stress_fail_mod."""
        assert round(self.asme.z_param, 3) == 0.448
        self.asme.anomaly.length = inch(50)
        assert round(self.asme.z_param, 3) == 70.871
        assert round(self.asme.get_stress_fail_mod(), 3) < 0  # == 54707.228

    def test_safe_pressure_zero(self):
        """Check method safe_pressure zero case."""
        save = self.asme.get_press_fail
        self.asme.get_press_fail = lambda is_mod: 0
        assert self.asme.erf() == 1
        self.asme.get_press_fail = save

    def test_leak_case(self):
        """Check REAL leak case."""
        from pipeline_csv.integrity.method.asme.b31g_2012 import Context

        self.pipe_ru.diameter = 273.0  # мм
        self.pipe_ru.thick_mm = 8
        self.material_ru.smys = 295.0  # Предел текучести МПа
        self.material_ru.smts = 500.0  # Предел прочности МПа

        self.defect_ru.length = 27  # мм
        self.defect_ru.row.depth_max = (self.pipe_ru.thick_mm / 100.0 * 54.8) * 100  # %%
        assert round(self.defect_ru.depth_mm, 2) == 4.38

        Context.corrosion_rate = 0.24  # мм/год
        maop = 4.0  # Мпа
        asme = Context(self.defect_ru, self.material_ru, maop)

        asme.is_explain = True
        assert round(asme.erf(), 3) == 0.186  # 0.224
        assert asme.years() == Context.REPAIR_NOT_REQUIRED
