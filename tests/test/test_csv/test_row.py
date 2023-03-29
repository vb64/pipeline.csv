"""Tests row.py file.

make test T=test_csv/test_row.py
"""
from . import TestCsv


class TestRow(TestCsv):
    """Check row.py file."""

    @staticmethod
    def test_set_geo():
        """Check set_geo."""
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import TypeDefekt, Row

        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '10', '10', '15', '', '', '', '', 'comment',
          latitude='111', longtitude='222', altitude='333'
        )
        assert row.latitude == '111'
        assert row.longtitude == '222'
        assert row.altitude == '333'

    def test_as_defekt(self):
        """Check as_defekt helpers."""
        from pipeline_csv import ObjectClass, DefektSide, Error
        from pipeline_csv.orientation import Orientation
        from pipeline_csv.oegiv import TypeDefekt, Row

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

        row = Row.as_defekt(
          10, TypeDefekt.CORROZ, DefektSide.INSIDE, '', '', '', orient1, orient2, mp_orient, 11, 'comment'
        )
        assert row.depth_max is None

    def test_as_seam(self):
        """Check as_seam helpers."""
        from pipeline_csv.csvfile.row import Row
        from pipeline_csv import TypeHorWeld, Error
        from pipeline_csv.orientation import Orientation

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

    def test_is(self):
        """Check  is_* helpers."""
        from pipeline_csv.csvfile.row import Row

        row = Row.as_weld(10)
        assert not row.is_metal_loss
        assert not row.is_dent
        assert not row.is_at_weld
        assert not row.is_at_seam
        assert not row.is_valve

    def test_as(self):
        """Check  as_* helpers."""
        from pipeline_csv.oegiv import Row, TypeMarker, LINEOBJ
        from pipeline_csv import Error

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
        assert row.marker == Row.get_bool(True)

        with self.assertRaises(Error) as context:
            Row.as_lineobj(10, 666, 'xxx', True, 'yyy')
        assert 'Wrong lineobj type: 666' in str(context.exception)

    @staticmethod
    def test_reverse_orient():
        """Check reverse_orient."""
        from pipeline_csv.csvfile.row import reverse_orient

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
        from pipeline_csv.oegiv import Row, TypeMarker
        from pipeline_csv import ObjectClass

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

    @staticmethod
    def test_reverse_comment():
        """Comment change on row reverse."""
        from pipeline_csv import ObjectClass
        from pipeline_csv.oegiv import Row

        row = Row()
        row.dist_od = '2'
        row.type_object = str(ObjectClass.MARKER)
        row.comments = 'влево'

        row.reverse(10)
        assert row.comments == 'вправо'

    @staticmethod
    def test_dict_default():
        """Check row default methods."""
        from pipeline_csv.csvfile.row import Row

        assert not Row.defekts_dict()
        assert not Row.lineobj_dict()
        assert not Row.markers_default()
        assert not Row.markers_reverse()
        assert not Row.comment_reverse()

        assert not Row.mloss_dict()
        assert not Row.dents_dict()
        assert not Row.atweld_dict()
        assert not Row.atseam_dict()
        assert not Row.valve_dict()
