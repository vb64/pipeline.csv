"""Tests i18n.py file.

make test T=test_integrity/test_i18n.py
"""
from . import TestIntegrity


class MockContext:
    """Mocked Context class."""

    is_explain = None


class TestI18n(TestIntegrity):
    """File i18n.py."""

    def test_load_po(self):
        """Check load_po function."""
        from pipeline_csv.integrity.i18n import load_po

        data = load_po(self.fixture('ru.po'))
        assert len(data) > 1

    def test_fgettext(self):
        """Check fake_gettext function."""
        from pipeline_csv.integrity.i18n import fake_gettext

        assert fake_gettext('xxx', MockContext()) == 'xxx'
