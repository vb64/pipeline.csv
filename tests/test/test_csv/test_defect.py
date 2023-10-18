"""Tests defect.py file.

make test T=test_csv/test_defect.py
"""
from . import TestCsv


class TestDefect(TestCsv):
    """Check defect.py file."""

    def setUp(self):
        """Make pipe for tests."""
        super().setUp()
        from pipeline_csv.csvfile import Stream
        from pipeline_csv.csvfile.tubes import Tube
        from pipeline_csv.csvfile.row import Row

        self.pipe = Tube(Row.as_weld(10), Stream(), '1')

    def test_props(self):
        """Check defekt properties."""
        from pipeline_csv import DefektSide
        from pipeline_csv.orientation import Orientation
        from pipeline_csv.oegiv import TypeDefekt, Row
        from pipeline_csv.csvfile.defect import Defect

        orient1 = Orientation(9, 10)
        orient2 = Orientation(5, 10)
        mp_orient = Orientation(11, 0)

        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', '15', orient1, orient2, mp_orient, 11, 'test defect'
        )
        assert row.orient_td == "9,10"
        assert row.orient_bd == "5,10"
        assert row.dist == 10

        assert self.pipe.dist == 10
        self.pipe.length = 12000
        self.pipe.thick = 120

        defect = Defect(row, self.pipe)
        assert 'Коррозия at ' in str(defect)
        assert defect.code == 0
        assert defect.is_metal_loss
        assert not defect.is_dent
        assert not defect.is_at_weld
        assert not defect.is_at_seam
