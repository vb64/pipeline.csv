"""Tests i18n.py file.

make test T=test_integrity/test_i18n.py
"""
from . import TestIntegrity


class TestI18n(TestIntegrity):
    """File i18n.py."""

    def test_load_po(self):
        """Check load_po function."""
        from pipeline_csv.integrity.i18n import load_po

        data = load_po(self.fixture('ru.po'))
        assert len(data) > 1
