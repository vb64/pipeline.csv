"""Module test_material.py.

make test T=test_material.py
"""
from . import TestIV


class TestMaterial(TestIV):
    """Check material.py file."""

    @staticmethod
    def test_material():
        """Check PipeMaterial class."""
        from pipeline_csv.material import PipeMaterial

        material = PipeMaterial("Сталь3", 250)
        assert material.name == "Сталь3"
        assert material.smys == 250
        assert material.smts is None
        assert material.toughness is None
        assert "Сталь3" in str(material)
