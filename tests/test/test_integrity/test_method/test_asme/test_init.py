"""Test method module.

make test T=test_integrity/test_method/test_asme/test_init.py
"""
from . import TestAsme


class TestsInit(TestAsme):
    """Base Asme Context class."""

    def setUp(self):
        """Make pipe for tests."""
        super().setUp()

        from pipeline_csv.integrity.method.asme import Context
        from pipeline_csv.integrity.material import PipeMaterial

        self.context = Context(
          self.make_defect(self.pipe.dist + 1, 10, None, None, None, 10),
          PipeMaterial("Сталь3", 250),
          100  # pressure
        )

    def test_lang(self):
        """Method lang."""
        from pipeline_csv.integrity.i18n import Lang

        assert len(self.context.lang(Lang.Ru)) > 1
