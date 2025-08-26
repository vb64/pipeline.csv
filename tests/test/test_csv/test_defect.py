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

        stream = Stream(diameter=700)
        self.pipe = Tube(Row.as_weld(10), stream, '1')

    def make_defect(self, dist, length, orient1, orient2, mp_orient, mp_dist):
        """Make new defect."""
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import TypeDefekt, Row
        from pipeline_csv.csvfile.defect import Defect

        defect = Defect(
          Row.as_defekt(
            dist, TypeDefekt.CORROZ, DefektSide.INSIDE, str(length), '10', '15',
            orient1, orient2,
            mp_orient, mp_dist, ''
          ),
          self.pipe
        )
        self.pipe.defects.append(defect)

        return defect

    def test_depth(self):
        """Check depth_percent/depth_mm properties."""
        from pipeline_csv.csvfile.defect import Defect, Depth
        from pipeline_csv.oegiv import TypeDefekt, Row
        from pipeline_csv import DefektSide

        self.pipe.thick = 100  # 10 mm
        depth_percent = 50  # 5 mm

        mloss = Row.as_defekt(
          11, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', str(depth_percent),
          None, None,
          None, None, ''
        )
        assert mloss.depth_units == Depth.PercentWallThickness

        mloss_defekt = Defect(mloss, self.pipe)
        assert mloss_defekt.is_metal_loss
        assert not mloss_defekt.is_dent
        assert mloss_defekt.depth_percent == 50
        assert mloss_defekt.depth_mm == 5

        dent = Row.as_defekt(
          11, TypeDefekt.DENT, DefektSide.INSIDE, '10', '10', str(depth_percent),
          None, None,
          None, None, ''
        )
        assert dent.depth_units == Depth.PercentWallThickness

        dent_defekt = Defect(dent, self.pipe)
        assert not dent_defekt.is_metal_loss
        assert dent_defekt.is_dent
        assert dent_defekt.depth_percent == 50
        assert dent_defekt.depth_mm == 350

        mech = Row.as_defekt(
          11, TypeDefekt.MECHANIC, DefektSide.INSIDE, '10', '10', str(depth_percent),
          None, None,
          None, None, ''
        )
        assert mech.depth_units == Depth.PercentWallThickness

        mech_defekt = Defect(mech, self.pipe)
        assert not mech_defekt.is_metal_loss
        assert not mech_defekt.is_dent
        assert mech_defekt.depth_percent == 5.0
        assert mech_defekt.depth_mm == 5.0

        mloss.depth_units = Depth.HundredthsOfMillimeter
        mloss_defekt.row.depth_max = '500'  # 5 mm
        assert mloss_defekt.depth_mm == 5
        assert mloss_defekt.depth_percent == 50

        dent.depth_units = Depth.HundredthsOfMillimeter
        dent_defekt.row.depth_max = '35000'  # 350 mm
        assert dent_defekt.depth_mm == 350
        assert dent_defekt.depth_percent == 50

        mloss_defekt.row.depth_max = ''
        assert mloss_defekt.depth_percent is None
        assert mloss_defekt.depth_mm is None

    def test_props(self):  # pylint: disable=too-many-statements
        """Check defekt properties."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.orientation import Orientation
        from pipeline_csv.oegiv import Row

        assert self.pipe.dist == 10
        self.pipe.length = 12000

        defect = self.make_defect(
          10, 10,
          Orientation(9, 10), Orientation(5, 10),
          Orientation(11, 0), 11
        )

        assert defect.row.orient_td == "9,10"
        assert defect.row.orient_bd == "5,10"
        assert defect.row.dist == 10
        assert 'Коррозия at ' in str(defect)
        assert defect.code == 0
        assert defect.is_metal_loss
        assert not defect.is_dent
        assert not defect.is_at_weld
        assert not defect.is_at_seam

        assert defect.orient_mp.as_minutes == 660
        assert defect.length == 10
        assert defect.number_at_pipe == 1

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

        defect.row.length = ''
        assert defect.length == 0

    def test_no_orient(self):
        """Check defekt without orientations."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.oegiv import Row

        defect = self.make_defect(10, 10, None, None, None, 11)
        assert defect.orient1 is None
        assert defect.orient2 is None
        assert defect.to_seam is None

        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.HORIZONTAL,
          '2,0', ''
        ))
        assert defect.to_seam is None

    def test_seam1_inside(self):
        """Check seam1 inside defekt borders."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.oegiv import Row
        from pipeline_csv.orientation import Orientation

        assert not self.pipe.seams
        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.HORIZONTAL,
          '2,0', ''
        ))
        assert len(self.pipe.seams) == 1

        defect = self.make_defect(
          10, 10,
          Orientation(1, 0), Orientation(3, 0),
          None, 11
        )
        assert defect.to_seam == 0

    def test_seam2_inside(self):
        """Check seam2 inside defekt borders."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.oegiv import Row
        from pipeline_csv.orientation import Orientation

        assert not self.pipe.seams
        self.pipe.add_object(Row.as_seam(
          self.pipe.dist + 1,
          TypeHorWeld.SECOND,
          '2,0', '8,0'
        ))

        defect = self.make_defect(
          10, 10,
          Orientation(7, 0), Orientation(9, 0),
          None, 11
        )
        assert defect.to_seam == 0

        defect = self.make_defect(
          10, 10,
          Orientation(10, 0), Orientation(11, 0),
          None, 11
        )
        assert defect.to_seam == 120

    def test_one_seam(self):
        """Check pipe with one seam."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.oegiv import Row
        from pipeline_csv.orientation import Orientation

        self.pipe.add_object(Row.as_seam(self.pipe.dist + 1, TypeHorWeld.SECOND, '2,0', ''))
        defect = self.make_defect(11, 10, Orientation(8, 0), Orientation(9, 0), None, 11)
        assert defect.to_seam == 300

        self.pipe.length = 12000
        assert defect.to_seam_weld == 1

    def test_orientation_point(self):
        """Check orientation_point property."""
        from pipeline_csv.orientation import Orientation

        defect = self.make_defect(11, 10, Orientation(8, 0), Orientation(9, 0), None, 11)
        assert defect.orientation_point.as_minutes == int(8 * 60 + 60 / 2)

        defect = self.make_defect(11, 10, None, Orientation(9, 0), Orientation(8, 0), 11)
        assert defect.orientation_point.as_minutes == 8 * 60

        defect = self.make_defect(11, 10, None, Orientation(9, 0), None, 11)
        assert defect.orientation_point.as_minutes == 9 * 60

        defect = self.make_defect(11, 10, None, None, None, 11)
        assert defect.orientation_point is None
