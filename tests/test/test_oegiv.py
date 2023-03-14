"""Module test_oegiv.py.

make test T=test_oegiv.py
"""
from . import TestIV


class TestOeg(TestIV):
    """Check orientation.py file."""

    def test_name_seam(self):
        """Check name_seam method."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.oegiv import Row

        assert Row.name_seam(TypeHorWeld.HORIZONTAL) == "Продольный шов"
