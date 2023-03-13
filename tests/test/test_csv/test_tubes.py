"""Tubes interface.

make test T=test_csv/test_tubes.py
"""
import pytest
from . import TestCsv


class TestTubes(TestCsv):
    """Test tubes.py module."""

    def setUp(self):
        """Init tube tests."""
        TestCsv.setUp(self)
        from oeg_iv.csvfile import Stream
        from oeg_iv.csvfile.tubes import Tube
        from oeg_iv.csvfile.row import Row

        self.tube = Tube(Row.as_weld(10), Stream(), '1')

    @staticmethod
    def test_no_welds():
        """No welds in csv file."""
        from oeg_iv.csvfile import File

        ivc = File()
        warns = []
        assert not ivc.get_tubes(warns)

    def test_add_object(self):
        """Add object."""
        from oeg_iv import Error
        from oeg_iv.csvfile.row import Row

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
        from oeg_iv import TypeMarker, TypeDefekt, DefektSide
        from oeg_iv.csvfile.row import Row

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
        from oeg_iv import TypeHorWeld
        from oeg_iv.csvfile.row import Row

        assert self.tube.typ == TypeHorWeld.UNKNOWN

        self.tube.add_object(Row.as_seam(
          self.tube.dist + 10,
          TypeHorWeld.HORIZONTAL,
          '1,10', ''
        ))
        assert self.tube.typ == TypeHorWeld.HORIZONTAL
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
        from oeg_iv.csvfile.row import Row

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

        self.tube.finalize(self.tube.dist + 100, [])
        assert self.tube.category == '1'
