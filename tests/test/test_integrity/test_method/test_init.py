"""Test method module.

make test T=test_integrity/test_method/test_init.py
"""
import pytest
from . import TestMethod


class TestsContext(TestMethod):
    """Class Context."""

    def test_explain(self):
        """Function explain."""
        from pipeline_csv.integrity.method import Context
        from pipeline_csv.integrity.material import PipeMaterial

        asme = Context(
          self.make_defect(self.pipe.dist + 1, 10, None, None, None, 10),
          PipeMaterial("Сталь3", 250),
          100  # pressure
        )
        assert Context.name in str(asme)

        assert asme.explain() == ''
        asme.explain_text = ['xx', 'yy']
        assert asme.explain() == 'xxyy'

        asme.add_explain(['zz'])
        assert asme.explain() == 'xxyy'

        asme.is_explain = True
        asme.add_explain(['zz'])
        assert asme.explain() == 'xxyyzz'

    @staticmethod
    def test_lang():
        """Method lang."""
        from pipeline_csv.integrity.method import Context

        with pytest.raises(NotImplementedError) as err:
            Context.lang('xxx')
        assert '.lang' in str(err.value)
