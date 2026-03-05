"""Test method module.

make test T=test_integrity/test_method/test_asme/test_init.py
"""
from . import TestAsme


class TestsInit(TestAsme):
    """Base Asme Context class."""

    def test_explain(self):
        """Function explain."""
        from pipeline_csv.integrity.method.asme import Context
        from pipeline_csv.integrity.material import PipeMaterial

        assert Context(
          self.make_defect(self.pipe.dist + 1, 10, None, None, None, 10),
          PipeMaterial("Сталь3", 250),
          100  # pressure
        )

    @staticmethod
    def test_lang():
        """Method lang."""
        from pipeline_csv.integrity.method.asme import Context
        from pipeline_csv.integrity.i18n import Lang

        assert len(Context.lang(Lang.Ru)) > 1
