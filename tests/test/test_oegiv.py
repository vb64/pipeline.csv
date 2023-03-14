"""Module test_oegiv.py.

make test T=test_oegiv.py
"""
from . import TestIV


class TestOeg(TestIV):
    """Check orientation.py file."""

    @staticmethod
    def test_name():
        """Check name_* methods."""
        from pipeline_csv import ObjectClass, TypeHorWeld
        from pipeline_csv.oegiv import Row

        assert Row.name_seam(TypeHorWeld.HORIZONTAL) == "Продольный шов"
        assert Row.name_object(ObjectClass.WELD) == "Шов"
        assert len(Row.markers_reverse()) == 4
        assert len(Row.markers_default()) == 3
