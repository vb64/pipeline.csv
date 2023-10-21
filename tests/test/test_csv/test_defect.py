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

        Tube.diam = 700
        self.pipe = Tube(Row.as_weld(10), Stream(), '1')

    def test_props(self):  # pylint: disable=too-many-statements
        """Check defekt properties."""
        from pipeline_csv import DefektSide, TypeHorWeld
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

        assert defect.row.mpoint_dist == 11
        assert defect.mp_left_weld == 1
        assert defect.mp_right_weld == 11999

        defect.row.mpoint_dist = ''
        assert defect.mp_left_weld is None
        assert defect.mp_right_weld is None

        assert defect.row.mpoint_orient == '11,00'
        mpoint_orient = Orientation.from_csv(defect.row.mpoint_orient)
        assert mpoint_orient.hours == 11
        assert mpoint_orient.minutes == 0
        assert mpoint_orient.as_minutes == 660

        defect.row.mpoint_dist = 11
        assert not self.pipe.seams
        assert defect.mp_seam is None

        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.SPIRAL,
          '1,10', ''
        ))
        assert len(self.pipe.seams) == 1
        assert defect.mp_seam is None

        self.pipe.seams = []
        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.HORIZONTAL,
          '1,10', ''
        ))
        assert len(self.pipe.seams) == 1
        seam1 = Orientation.from_csv(self.pipe.seams[0].orient_td)
        assert seam1.hours == 1
        assert seam1.minutes == 10
        assert defect.mp_seam == 397

        self.pipe.seams = []
        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.SECOND,
          '11,10', '5,10'
        ))
        assert defect.mp_seam == 30
        assert defect.mp_seam_weld == 1

        self.pipe.seams = []
        assert defect.mp_seam_weld == 1

        assert defect.row.dist == 10
        assert defect.row.length == '10'

        assert defect.to_left_weld == 0
        assert defect.to_right_weld == 11990

    def test_no_orient(self):
        """Check defekt without orientations."""
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import TypeDefekt, Row
        from pipeline_csv.csvfile.defect import Defect

        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', '15', None, None, None, 11, 'comment'
        )
        defect = Defect(row, self.pipe)
        assert defect.orient1 is None
        assert defect.orient2 is None
        assert defect.to_seam is None

    def test_seam1_inside(self):
        """Check seam1 inside defekt borders."""
        from pipeline_csv import TypeHorWeld, DefektSide
        from pipeline_csv.oegiv import TypeDefekt, Row
        from pipeline_csv.csvfile.defect import Defect
        from pipeline_csv.orientation import Orientation

        assert not self.pipe.seams
        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.HORIZONTAL,
          '2,0', ''
        ))
        assert len(self.pipe.seams) == 1

        orient1 = Orientation(1, 0)
        orient2 = Orientation(3, 0)
        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', '15', orient1, orient2, None, 11, ''
        )
        defect = Defect(row, self.pipe)
        assert defect.to_seam == 0

    def test_seam2_inside(self):
        """Check seam2 inside defekt borders."""
        from pipeline_csv import TypeHorWeld, DefektSide
        from pipeline_csv.oegiv import TypeDefekt, Row
        from pipeline_csv.csvfile.defect import Defect
        from pipeline_csv.orientation import Orientation

        assert not self.pipe.seams
        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.SECOND,
          '2,0', '8,0'
        ))
        orient1 = Orientation(7, 0)
        orient2 = Orientation(9, 0)
        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', '15',
          orient1, orient2, None, 11, ''
        )
        defect = Defect(row, self.pipe)
        assert defect.to_seam == 0
