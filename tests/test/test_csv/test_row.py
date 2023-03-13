"""Tests row.py file.

make test T=test_csv/test_row.py
"""
from . import TestCsv


class TestRow(TestCsv):
    """Check row.py file."""

    @staticmethod
    def test_set_geo():
        """Check set_geo."""
        from oeg_iv import TypeDefekt, DefektSide
        from oeg_iv.csvfile.row import Row

        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', '15', '', '', '', '', 'comment',
          latitude='111', longtitude='222', altitude='333'
        )
        assert row.latitude == '111'
        assert row.longtitude == '222'
        assert row.altitude == '333'

    def test_as_defekt(self):
        """Check as_defekt helpers."""
        from oeg_iv.csvfile.row import Row
        from oeg_iv import ObjectClass, TypeDefekt, DefektSide, Error
        from oeg_iv.orientation import Orientation

        orient1 = Orientation(9, 15)
        orient2 = Orientation(5, 15)
        mp_orient = Orientation(11, 0)

        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', '15', orient1, orient2, mp_orient, 11, 'comment'
        )
        assert row.type_object == ObjectClass.DEFEKT
        assert row.object_code == TypeDefekt.CORROZ
        assert row.orient_td == "9,15"
        assert row.orient_bd == "5,15"

        with self.assertRaises(Error) as context:
            Row.as_defekt(10, 999, 666, 10, 10, 15, orient1, orient2, orient1, 11, 'comment')
        assert 'Wrong defekt type: 999' in str(context.exception)

    def test_as_seam(self):
        """Check as_seam helpers."""
        from oeg_iv.csvfile.row import Row
        from oeg_iv import TypeHorWeld, Error
        from oeg_iv.orientation import Orientation

        orient1 = Orientation(10, 15)
        orient2 = Orientation(4, 15)

        row = Row.as_seam(10, TypeHorWeld.HORIZONTAL, orient1, orient2)
        assert row.is_seam
        assert row.object_code == TypeHorWeld.HORIZONTAL
        assert row.orient_td == "10,15"
        assert not row.orient_bd

        row = Row.as_seam(10, TypeHorWeld.SECOND, orient1, orient2)
        assert row.is_seam
        assert row.object_code == TypeHorWeld.SECOND
        assert row.orient_td == "10,15"
        assert row.orient_bd == "4,15"

        row = Row.as_seam(10, TypeHorWeld.NO_WELD, orient1, orient2)
        assert row.is_seam
        assert row.object_code == TypeHorWeld.NO_WELD
        assert not row.orient_td
        assert not row.orient_bd

        row = Row.as_seam(10, TypeHorWeld.SPIRAL, orient1, orient2)
        assert row.is_seam
        assert row.object_code == TypeHorWeld.SPIRAL
        assert row.orient_td == "10,15"
        assert not row.orient_bd

        with self.assertRaises(Error) as context:
            Row.as_seam(10, 99, orient1, orient2)
        assert 'Wrong seam type: 99' in str(context.exception)

    @staticmethod
    def test_as():
        """Check  as_* helpers."""
        from oeg_iv.csvfile.row import Row, iv_bool
        from oeg_iv import TypeMarker, LINEOBJ

        row = Row.as_weld(10)
        assert row.is_weld
        assert row.dist_od == 10

        row = Row.as_weld(10, custom_number='1xx')
        assert row.is_weld
        assert row.dist_od == 10
        assert len(row.object_name) == 3

        row = Row.as_thick(10, 105)
        assert row.is_thick
        assert row.depth_max == 105

        row = Row.as_category(10, 1)
        assert row.is_category
        assert row.depth_max == 1

        row = Row.as_lineobj(10, TypeMarker.VALVE, 'xxx', True, 'yyy')
        assert row.is_lineobj
        assert row.object_code == TypeMarker.VALVE
        assert row.object_code_t == LINEOBJ[TypeMarker.VALVE]
        assert row.object_name == 'xxx'
        assert row.comments == 'yyy'
        assert row.marker == iv_bool(True)

    @staticmethod
    def test_reverse_orient():
        """Check reverse_orient."""
        from oeg_iv.csvfile.row import reverse_orient

        assert reverse_orient("0") == '12,00'
        assert reverse_orient("12") == '12,00'
        assert reverse_orient("3,51") == '8,09'
        assert reverse_orient("3,09") == '8,51'

        assert reverse_orient("3,35") == '8,25'
        assert reverse_orient("3,47") == '8,13'
        assert reverse_orient("8,41") == '3,19'
        assert reverse_orient("9,11") == '2,49'

    @staticmethod
    def test_reverse():
        """Check row.reverse."""
        from oeg_iv.csvfile.row import Row
        from oeg_iv import ObjectClass, TypeMarker

        row = Row()
        row.dist_od = '2'
        row.type_object = str(ObjectClass.MARKER)
        row.object_code = str(TypeMarker.CASE_END)

        row.reverse(10)
        assert row.dist_od == '8'
        assert row.object_code == str(TypeMarker.CASE_START)

        row.reverse(10)
        assert row.dist_od == '2'
        assert row.object_code == str(TypeMarker.CASE_END)

        row.object_code = str(TypeMarker.TURN_END)

        row.reverse(10)
        assert row.dist_od == '8'
        assert row.object_code == str(TypeMarker.TURN_START)

        row.reverse(10)
        assert row.dist_od == '2'
        assert row.object_code == str(TypeMarker.TURN_END)
