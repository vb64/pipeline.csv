"""Tubes interface.

make test T=test_csv/test_tubes.py
"""
from math import pi
import pytest
from . import TestCsv


class TestTubes(TestCsv):
    """Test tubes.py module."""

    def setUp(self):
        """Init tube tests."""
        TestCsv.setUp(self)
        from pipeline_csv.csvfile import Stream
        from pipeline_csv.csvfile.tubes import Tube
        from pipeline_csv.csvfile.row import Row

        stream = Stream(diameter=700)
        self.tube = Tube(Row.as_weld(10), stream, '1')

    def test_str(self):
        """Method str."""
        assert 'Tube diam ' in str(self.tube)

    def test_min_diam(self):
        """Check min_diam."""
        self.tube.min_diam = '100'
        assert self.tube.min_diam == '100'

    @staticmethod
    def test_no_welds():
        """No welds in csv file."""
        from pipeline_csv.csvfile import File

        ivc = File(1400)
        warns = []
        assert not ivc.get_tubes(warns)

    def test_add_object(self):
        """Add object."""
        from pipeline_csv import Error
        from pipeline_csv.csvfile.row import Row

        with pytest.raises(Error) as err:
            self.tube.add_object(Row.as_weld(11))
        assert 'Tube at dist 10 has wrong row:' in str(err.value)

    def test_geo(self):
        """Geo data."""
        self.tube.set_geo(10, 11, 12)
        assert self.tube.latitude == 10
        assert self.tube.longtitude == 11
        assert self.tube.altitude == 12

    def test_radius(self):
        """Curve radius."""
        assert self.tube.radius == ''
        self.tube.set_radius('100')
        assert self.tube.radius == '100'

    def test_number(self):
        """Tube number."""
        assert self.tube.number == '1'
        self.tube.row.object_name = ' 123 '
        assert self.tube.number == '123'

    def test_summary(self):
        """Tube summary."""
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import TypeMarker, TypeDefekt, Row

        assert self.tube.summary == ''

        self.tube.add_object(Row.as_lineobj(
          self.tube.dist + 10,
          TypeMarker.VALVE,
          'V1',
          True,
          'Valve comment'
        ))

        self.tube.add_object(Row.as_defekt(
          str(self.tube.dist + 20),
          TypeDefekt.CORROZ, DefektSide.OUTSIDE,
          '10', '10', '10',
          '100', '200', '150', str(self.tube.dist + 25),
          'Coroz1 comment'
        ))
        self.tube.add_object(Row.as_defekt(
          str(self.tube.dist + 30),
          TypeDefekt.CORROZ, DefektSide.OUTSIDE,
          '8', '8', '8',
          '100', '200', '150', str(self.tube.dist + 35),
          'Coroz2 comment'
        ))

        assert ': 1' in self.tube.summary
        assert ': 2' in self.tube.summary

    def test_typ(self):
        """Pipe type."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.csvfile.row import Row

        assert self.tube.typ == TypeHorWeld.UNKNOWN

        self.tube.add_object(Row.as_seam(
          self.tube.dist + 10,
          TypeHorWeld.HORIZONTAL,
          '1,10', ''
        ))
        assert self.tube.typ == TypeHorWeld.HORIZONTAL
        assert self.tube.seam1.as_minutes == 70
        assert self.tube.seam2 is None
        assert self.tube.seam_info == '1,10'

        self.tube.seams = []
        self.tube.add_object(Row.as_seam(
          self.tube.dist + 10,
          TypeHorWeld.SECOND,
          '1,10', '7,10'
        ))
        assert self.tube.typ == TypeHorWeld.SECOND
        assert self.tube.seam_info == '1,10 / 7,10'

        self.tube.seams = []
        self.tube.add_object(Row.as_seam(
          self.tube.dist + 10,
          TypeHorWeld.NO_WELD,
          '1,10', '7,10'
        ))
        assert self.tube.typ == TypeHorWeld.NO_WELD
        assert self.tube.seam_info == ''

        self.tube.seams = []
        self.tube.add_object(Row.as_seam(
          self.tube.dist + 10,
          TypeHorWeld.SPIRAL,
          '1,10', ''
        ))
        self.tube.add_object(Row.as_seam(
          self.tube.dist + 20,
          TypeHorWeld.SPIRAL,
          '6,10', ''
        ))
        assert self.tube.typ == TypeHorWeld.SPIRAL
        assert self.tube.seam_info == '1,10 / 6,10'

    def test_category(self):
        """Pipe category."""
        from pipeline_csv.csvfile.row import Row

        assert self.tube.category is None
        assert self.tube.stream.category is None
        assert not self.tube.is_category_change

        self.tube.add_object(Row.as_category(
          self.tube.dist + 10,
          '1',
        ))

        assert self.tube.is_category_change
        assert self.tube.stream.category == '1'

        self.tube.add_object(Row.as_category(
          self.tube.dist + 20,
          '1',
        ))

        assert self.tube.stream.category == '1'

        self.tube.finalize(self.tube.dist + 100)
        assert self.tube.category == '1'

    def test_features(self):
        """Method features."""
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import TypeMarker, TypeDefekt, Row

        self.tube.lineobjects = []
        self.tube.defects = []

        self.tube.add_object(Row.as_defekt(
          str(self.tube.dist + 25),
          TypeDefekt.CORROZ, DefektSide.OUTSIDE,
          '10', '10', '10',
          '100', '200', '150', str(self.tube.dist + 25),
          'Coroz1 comment'
        ))
        self.tube.add_object(Row.as_lineobj(
          self.tube.dist + 20,
          TypeMarker.VALVE,
          'V1',
          True,
          'Valve comment'
        ))

        features = list(self.tube.features())
        assert len(features) == 2
        assert features[0].is_lineobj
        assert features[1].is_defect

    def test_thickness(self):
        """Check property is_thick_change."""
        from pipeline_csv.oegiv import File
        from pipeline_csv.oegiv import Row

        csv_file = File(1400)
        csv_file.data = [
          Row.as_weld(10),
          Row.as_thick(11, 105),
          Row.as_weld(1000),
          Row.as_thick(1011, 105),
          Row.as_weld(2000),
          Row.as_weld(3000),
          Row.as_thick(3011, 120),
          Row.as_weld(4000),
        ]

        fname = self.build('thickness.csv')
        csv_file.to_file(fname)
        csv_file = File.from_file(fname, 1400)
        pipes = list(csv_file.get_tubes())

        assert len(pipes) == 4
        assert pipes[0].is_thick_change is None
        assert pipes[1].is_thick_change is None
        assert pipes[2].is_thick_change is None
        assert pipes[3].is_thick_change == 105

    def test_minutes2mm(self):
        """Check minutes2mm method."""
        circle = int(self.tube.diameter * pi)
        assert self.tube.minutes2mm(720) == circle
        assert self.tube.minutes2mm(720 / 2) == int(circle / 2)
        assert self.tube.minutes2mm(720 / 4) == int(circle / 4)
        assert self.tube.minutes2mm(0) == 0

    def test_diam(self):
        """Check property is_diameter_change."""
        from pipeline_csv.oegiv import File
        from pipeline_csv.oegiv import Row

        csv_file = File()
        csv_file.data = [

          Row.as_weld(10),
          Row.as_diam(11, "", 1200),

          Row.as_weld(1000),
          Row.as_diam(1011, 1200, 1000),
          Row.as_diam(1012, 1200, 1000),

          Row.as_weld(2000),

          Row.as_weld(3000),
          Row.as_diam(3011, 1000, 1400),

          Row.as_weld(4000),
        ]

        fname = self.build('diam_change.csv')
        csv_file.to_file(fname)
        csv_file = File.from_file(fname)
        pipes = list(csv_file.get_tubes())

        assert len(pipes) == 4

        assert pipes[0].diameter == '1200'
        assert pipes[0].is_diameter_change is None

        assert pipes[1].diameter == '1200'
        assert pipes[1].is_diameter_change == '1000'

        assert pipes[2].diameter == '1000'
        assert pipes[2].is_diameter_change is None

        assert pipes[3].diameter == '1000'
        assert pipes[3].is_diameter_change == '1400'

        csv_file.reverse()

        fname = self.build('diam_change_reverse.csv')
        csv_file.to_file(fname)
        csv_file = File.from_file(fname)
        pipes = list(csv_file.get_tubes())

        assert len(pipes) == 4

        assert pipes[0].diameter == '1400'
        assert pipes[0].is_diameter_change is None

        assert pipes[1].diameter == '1400'
        assert pipes[1].is_diameter_change is None

        assert pipes[2].diameter == '1400'
        assert pipes[2].is_diameter_change == '1000'

        assert pipes[3].diameter == '1000'
        assert pipes[3].is_diameter_change == '1200'

    def test_diam_reverse(self):
        """Check reversed diameter changes."""
        from pipeline_csv.oegiv import File
        from pipeline_csv.oegiv import Row

        csv_file = File()
        csv_file.data = [

          Row.as_weld(10),
          Row.as_diam(11, "", 1200),

          Row.as_weld(1000),
          Row.as_weld(2000),
          Row.as_weld(3000),
          Row.as_weld(4000),
        ]

        fname = self.build('diam_reverse.csv')
        csv_file.to_file(fname)
        csv_file = File.from_file(fname)
        pipes = list(csv_file.get_tubes())

        assert len(pipes) == 4
        assert pipes[3].diameter == '1200'
        assert pipes[3].is_diameter_change is None

        csv_file.reverse()
        csv_file.to_file(fname)
        csv_file = File.from_file(fname)
        pipes = list(csv_file.get_tubes())

        assert len(pipes) == 4
        assert pipes[0].diameter == '1200'
        assert pipes[0].is_diameter_change is None
