"""Test method module.

make test T=test_integrity/test_method/test_init.py
"""
import pytest
from . import TestMethod


class TestsContext(TestMethod):
    """Class Context."""

    def setUp(self):
        """Make pipe for tests."""
        super().setUp()

        from pipeline_csv.integrity.method import Context
        from pipeline_csv.integrity.material import PipeMaterial

        self.asme = Context(
          self.make_defect(self.pipe.dist + 1, 10, None, None, None, 10),
          PipeMaterial("Сталь3", 250),
          100  # pressure
        )

    def test_explain(self):
        """Function explain."""
        from pipeline_csv.integrity.method import Context

        assert Context.name in str(self.asme)

        assert self.asme.explain() == ''
        self.asme.explain_text = ['xx', 'yy']
        assert self.asme.explain() == 'xxyy'

        self.asme.add_explain(['zz'])
        assert self.asme.explain() == 'xxyyzz'

        self.asme.is_explain = True
        self.asme.add_explain(['zz'])
        assert self.asme.explain() == 'xxyyzzzz'

    def test_lang(self):
        """Method lang."""
        with pytest.raises(NotImplementedError) as err:
            self.asme.lang('xxx')
        assert '.lang' in str(err.value)
