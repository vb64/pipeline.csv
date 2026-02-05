"""Test for README.md examples.

make test T=test_readme.py
"""
import os
from . import TestIV


def save_and_load(filecls, csv, fname):
    """Save and reload."""
    csv.to_file(fname)
    return filecls.from_file(fname)


def check_diam():
    """Check operation with pipeline diameter change."""
    from pipeline_csv.oegiv import File, Row

    csv_file = File(1200)

    csv_file.data += [
      Row.as_weld(0),
      Row.as_weld(1000),
      Row.as_diam(1001, 1200, 1400),
      Row.as_weld(2000),
      Row.as_weld(3000),
      Row.as_weld(4000),
    ]

    # 4 pipes
    pipes = list(csv_file.get_tubes())
    assert len(pipes) == 4

    # first pipe diameter 1200, no diameter change
    assert pipes[0].diameter == 1200
    assert pipes[0].is_diameter_change is None

    # second pipe diam change 1200 -> 1400
    assert pipes[1].diameter == 1200
    assert pipes[1].is_diameter_change == 1400

    # next two pipes diameter 1400, no diameter change
    assert pipes[2].diameter == 1400
    assert pipes[2].is_diameter_change is None
    assert pipes[3].diameter == 1400
    assert pipes[3].is_diameter_change is None

    fname = 'diam.csv'
    csv_file = save_and_load(File, csv_file, fname)
    # csv_file.to_file(fname)
    # csv_file = File.from_file(fname)

    # reverse data, save to file and reload
    csv_file.reverse()
    csv_file = save_and_load(File, csv_file, fname)

    pipes = list(csv_file.get_tubes())
    assert len(pipes) == 4

    # first two pipes has diameter 1400, no diameter change
    assert int(pipes[0].diameter) == 1400
    assert pipes[0].is_diameter_change is None
    assert int(pipes[1].diameter) == 1400
    assert pipes[1].is_diameter_change is None

    # Third pipe has diam change 1400 -> 1200
    assert int(pipes[2].diameter) == (1400)
    assert int(pipes[2].is_diameter_change) == 1200

    # last pipe diameter 1200, no diameter change
    assert int(pipes[3].diameter) == 1200
    assert pipes[3].is_diameter_change is None


def check_new():
    """Construct new csv file from scratch."""
    from pipeline_csv import TypeHorWeld, DefektSide
    from pipeline_csv.orientation import Orientation
    from pipeline_csv.oegiv import File
    from pipeline_csv.oegiv import TypeDefekt, Row

    csv_file = File(1000)

    # define tube at distance 1.0 m
    # length = 11.0 m, thick = 10.5 mm
    # with one seam with orientation 3 hour 00 minutes
    csv_file.data = [
      Row.as_weld(1000),
      Row.as_thick(1010, 105),
      Row.as_seam(1020, TypeHorWeld.HORIZONTAL, Orientation(3, 0), None),
      Row.as_weld(12000),
    ]

    # add defect to tube at distance 5.0 m from left tube weld
    # length = 20 mm, width = 10 mm, depth = 30% tube wall thickness
    # orientation from 4 hours 00 minutes to 5 hours 00 minutes
    # max depth point at 10 mm from left border of defect, orientation 4 hours 30 minutes
    # with comment 'metal loss'
    csv_file.data.append(Row.as_defekt(
      6000,
      TypeDefekt.CORROZ,
      DefektSide.INSIDE,
      '20', '10', '30',
      Orientation(4, 0), Orientation(5, 0),
      Orientation(4, 30), 6010,
      'metal loss'
    ))

    # save csv to file
    csv_file.to_file('example.csv')
    assert os.path.getsize('example.csv') > 0

    return csv_file


def check_reversing(csv_file):
    """Reversing the data."""
    from pipeline_csv.oegiv import File

    # create copy from saved file
    csv_copy = File.from_file('example.csv', 1000)

    # check distance of the last object in copy
    assert csv_copy.total_length == 12000
    assert len(csv_copy.data) == 6

    # check defect orientation
    defect_row = csv_copy.data[4]
    assert defect_row.is_defect
    assert defect_row.orient_td == '4,00'
    assert defect_row.orient_bd == '5,00'
    assert defect_row.mpoint_orient == '4,30'

    # reverse copy
    csv_copy.reverse()

    # relative position of defekt must change
    defect_row = csv_copy.data[2]
    assert defect_row.is_defect

    # defect orientation must be mirrored
    assert defect_row.orient_td == '7,00'
    assert defect_row.orient_bd == '8,00'
    assert defect_row.mpoint_orient == '7,30'

    # save reversed copy to file
    csv_file.to_file('reversed.csv')
    assert os.path.getsize('reversed.csv') > 0


def check_join(csv_file):
    """Append to initial CSV empty pipe with length = 10.0 m and reversed copy from the file."""
    csv_file.join([10000, 'reversed.csv'])
    assert csv_file.total_length == 28000
    assert len(csv_file.data) == 12


def check_transform(csv_file):
    """Compress distances and length of all objects in half."""
    from pipeline_csv.oegiv import File

    csv_file.dist_modify([[0, 0], [28000, 14000]])
    assert csv_file.total_length == 14000

    # save file with compress distances
    csv_file.to_file('transformed.csv')
    assert os.path.getsize('transformed.csv') > 0

    # load new copy
    csv_trans = File.from_file('transformed.csv', 1000)

    # iterate by tubes
    warnings = []
    current_dist = 0
    for i in csv_trans.get_tubes(warnings):
        assert i.dist >= current_dist
        current_dist = i.dist
        tube = i

    assert not warnings  # ignored diam change before first weld

    # set geodata for tube
    assert tube.latitude == ''
    assert tube.longtitude == ''
    assert tube.altitude == ''

    tube.set_geo(10, 11, 12)

    assert tube.latitude == 10
    assert tube.longtitude == 11
    assert tube.altitude == 12

    csv_trans.to_file('geo.csv')
    assert os.path.getsize('geo.csv') > 0

    # load from saved file and check geodata from last pipe
    csv_geo = File.from_file('geo.csv', 1000)
    last_tube = list(csv_geo.get_tubes(warnings))[-1]

    assert last_tube.latitude == '10'
    assert last_tube.longtitude == '11'
    assert last_tube.altitude == '12'


def check_defect():
    """Check Defect class."""
    from pipeline_csv.oegiv import File
    from pipeline_csv.oegiv import TypeDefekt, Row
    from pipeline_csv.orientation import Orientation
    from pipeline_csv import TypeHorWeld, DefektSide

    # set pipeline diameter to 1000 mm
    csv = File(1000)

    # define one pipe at distance 1.0 m, length = 11.0 m
    # with one seam with orientation 3 hour 00 minutes
    # and one defect at distance 5.0 m from left tube weld.
    # defect length = 20 mm, width = 10 mm, depth = 30% tube wall thickness
    # orientation from 4 hours 00 minutes to 5 hours 00 minutes
    # max depth point at 10 mm from left border of defect, orientation 4 hours 30 minutes
    csv.data = [
      Row.as_weld(1000),
      Row.as_seam(1020, TypeHorWeld.HORIZONTAL, Orientation(3, 0), None),
      Row.as_defekt(
        6000,
        TypeDefekt.CORROZ, DefektSide.INSIDE,
        '20', '10', '30',
        Orientation(4, 0), Orientation(5, 0),
        Orientation(4, 30), 6010,
        'corrozion'
      ),
      Row.as_weld(12000),
    ]

    pipes = list(csv.get_tubes())
    assert len(pipes) == 1
    pipe = pipes[0]
    assert pipe.diameter == 1000

    # one defect at the pipe
    assert len(pipe.defects) == 1
    defect = pipe.defects[0]

    # defect is metal loss, not dent
    # defect is not located at the weld/seam
    assert defect.is_metal_loss
    assert not defect.is_dent
    assert not defect.is_at_weld
    assert not defect.is_at_seam

    # defect as point orientation is maximum depth point orientation at 4:30
    assert defect.orientation_point.as_minutes == 270

    # distance (mm) from maximum depth point to upstream weld
    assert defect.mp_left_weld == 5010

    # distance (mm) from maximum depth point to downstream weld
    assert defect.mp_right_weld == 5990

    # distance (mm) from maximum depth point to seam.
    assert defect.mp_seam == 392

    # distance (mm) from maximum depth point to nearest seam/weld.
    assert defect.mp_seam_weld == 392

    # distance (mm) from left defect border to upstream weld
    assert defect.to_left_weld == 5000

    # distance (mm) from right defect border to downstream weld
    assert defect.to_right_weld == 5980

    # distance (mm) from defect borders to seam
    assert defect.to_seam == 60

    # distance (mm) from defect borders to nearest seam/weld.
    assert defect.to_seam_weld == 60


class TestReadme(TestIV):
    """Example code for readme.md file."""

    @staticmethod
    def test_readme():
        """Readmi.md example code."""
        csv_file = check_new()
        check_reversing(csv_file)
        check_join(csv_file)
        check_transform(csv_file)
        check_defect()
        check_diam()

        for name in [
          'example.csv',
          'reversed.csv',
          'transformed.csv',
          'geo.csv',
          'diam.csv',
        ]:
            os.remove(name)

    @staticmethod
    def test_attr_list():
        """Function attr_list."""
        from pipeline_csv import attr_list, ObjectClass

        assert len(attr_list(ObjectClass)) == 7
