"""Tests __init__.py file.

make test T=test_csv/test_init.py
"""
import os
import pytest
from . import TestCsv


class TestInit(TestCsv):  # pylint: disable=too-many-public-methods
    """File __init__.py."""

    def test_check_object(self):
        """Check check_object method."""
        from pipeline_csv import DefektSide
        from pipeline_csv.oegiv import File, TypeDefekt

        csv_file = File(1000)
        row = File.RowCls.as_defekt(
          6000,
          TypeDefekt.DENT,
          DefektSide.OUTSIDE,
          '', '', '',
          None, None,
          6010, None,
          'zero depth dent'
        )
        warns = []
        csv_file.check_object(row, self.tube, warns)
        assert len(warns) == 1
        assert 'Zero depth dent:' in warns[0]

    @staticmethod
    def test_format_floats():
        """Check format_floats function."""
        from pipeline_csv.csvfile import format_floats, FloatDelimiter

        data = [1, '2', 3.0]
        assert format_floats(data, FloatDelimiter.Point) == data
        assert format_floats(data, FloatDelimiter.Comma) == [1, '2', '3,0']

    def test_get_tubes(self):
        """Check get_tubes."""
        from pipeline_csv import TypeHorWeld
        from pipeline_csv.csvfile.row import Row
        from pipeline_csv.oegiv import File

        csv_file = File.at_folder(self.fixture(), 1400)
        assert len(csv_file.data) == 179

        csv_file = File.from_file(self.fixture('DefTable.csv'), 1400)
        assert len(csv_file.data) == 179

        csv_file.data.insert(0, Row.as_seam(0, TypeHorWeld.NO_WELD, '', ''))
        assert len(csv_file.data) == 180

        warns = []
        tubes = csv_file.get_tubes(warns)
        assert tubes
        assert len(warns) == 1

        tube = next(tubes)
        assert tube.dist == 0

        tube = next(tubes)
        assert tube.dist == 6924

        for tube in tubes:
            pass

        assert tube.dist == 416088
        assert len(warns) == 1

    @staticmethod
    def check_objects(objects, val_list):
        """Check compare objrcts list with expected values."""
        assert len(objects) == len(val_list)
        for item, vals in zip(objects, val_list):
            assert item.dist_od == vals[0]
            assert item.depth_max == vals[1]

    def test_min_diam(self):
        """Check file with min_diam fields."""
        from pipeline_csv.csvfile import File
        from pipeline_csv.csvfile.row import Row

        csv_file = File.from_file(self.fixture('min_diam.csv'), 1400)
        assert csv_file.data[-1].min_diam == '100'

        csv_file = File(1400)
        csv_file.data = [
          Row.as_weld(10, min_diam='200'),
        ]
        assert csv_file.data[-1].min_diam == '200'

    def test_dup_ids(self):
        """Check file with duplicated object IDs."""
        from pipeline_csv import Error
        from pipeline_csv.csvfile import File
        from pipeline_csv.csvfile.row import Row

        with pytest.raises(Error) as err:
            File.from_file(self.fixture('dup_ids.csv'), 1400)
        assert 'Duplicate object ID' in str(err.value)

        csv_file = File(1400)
        csv_file.data = [
          Row.as_weld(10, obj_id=333),
          Row.as_weld(1000, obj_id=333),
        ]

        with pytest.raises(Error) as err:
            csv_file.to_file(self.build('dup_ids.csv'))
        assert 'Duplicate object ID' in str(err.value)

    def test_no_thick_category(self):
        """Check reverse data file without thick and category objects."""
        from pipeline_csv.oegiv import File

        csv_file = File.from_file(self.fixture('no_thicks.csv'), 1400)
        assert len(csv_file.data) == 9

        csv_file.reverse()
        assert len(csv_file.data) == 9

    def test_no_welds(self):
        """Check reverse data file without welds."""
        from pipeline_csv.oegiv import File

        csv_file = File.from_file(self.fixture('no_welds.csv'), 1400)
        assert len(csv_file.data) == 2

        csv_file.reverse()
        assert len(csv_file.data) == 2

    def test_reverse(self):
        """Check reverse."""
        from pipeline_csv.oegiv import File

        csv_file = File.from_file(self.fixture('DefTable.csv'), 1400)
        assert len(csv_file.data) == 179

        expected = [
          ('1000', '1'),
          ('52428', '3'),
          ('308392', '2'),
        ]
        self.check_objects(csv_file.categories, expected)

        expected = [
          ('1300', '90'),
          ('63628', '70'),
          ('306232', '100'),
        ]
        self.check_objects(csv_file.thicks, expected)

        assert len(csv_file.data[0].values()) == len(File.COLUMN_HEADS)
        assert csv_file.total_length == 426625

        csv_file.reverse()

        assert len(csv_file.data) == 179
        assert csv_file.total_length == 426625

        expected = [
          ('0', ''),
          ('1', ''),
          ('2', '100'),
          ('3', '2'),
        ]
        self.check_objects(csv_file.data[:4], expected)

        fname = os.path.join('build', 'output.csv')
        if os.path.exists(fname):
            os.remove(fname)

        csv_file.to_file(fname)
        assert os.path.exists(fname)
        csv_file = File.from_file(fname, 1400)

        assert len(csv_file.data) == 180
        assert csv_file.total_length == 426625

        expected = [
          ('3', '2'),
          ('374197', '3'),
          ('425625', '1'),
        ]
        self.check_objects(csv_file.categories, expected)

        expected = [
          ('2', '100'),
          ('362997', '70'),
          ('425325', '90'),
        ]
        self.check_objects(csv_file.thicks, expected)

        os.remove(fname)

    def test_join(self):
        """Check join."""
        from pipeline_csv.oegiv import File

        fname = self.fixture('DefTable.csv')
        csv_file = File.from_file(fname, 1400)

        assert len(csv_file.data) == 179
        assert csv_file.total_length == 426625

        csv_file.join(['11000', fname])

        assert len(csv_file.data) == (179 * 2 + 1)
        assert csv_file.total_length == (426625 * 2 + 11000)

    def test_join_short(self):
        """Check join short file."""
        from pipeline_csv.oegiv import File

        fname = self.fixture('1.csv')
        csv_file = File.from_file(fname, 1400)

        assert len(csv_file.data) == 8
        assert csv_file.total_length == 8800

        csv_file.join(['11000', fname])

        assert len(csv_file.data) == (8 * 2 + 1)
        assert csv_file.total_length == (8800 * 2 + 11000)

        fname = os.path.join('build', '1.csv')
        if os.path.exists(fname):
            os.remove(fname)

        csv_file.to_file(fname)
        assert os.path.exists(fname)

    @staticmethod
    def test_transform_length_wrong():
        """Check transform_length with wrong data."""
        from pipeline_csv.csvfile import transform_length

        table = [[0, 0], [10, 5]]
        assert transform_length(0, '-', table, 0) == '-'

    @staticmethod
    def test_transform_length():
        """Check transform_length."""
        from pipeline_csv.csvfile import transform_length

        table = [[0, 0], [100, 50]]
        assert transform_length(10, '40', table, 0) == 20

    @staticmethod
    def test_transform_dist():
        """Check transform_dist."""
        from pipeline_csv.csvfile import transform_dist

        table = [[0, 0], [10, 5]]
        indx = 0

        new_indx, pos = transform_dist(0, table, indx)
        assert pos == 0
        assert new_indx == indx

        new_indx, pos = transform_dist(10, table, indx)
        assert pos == 5
        assert new_indx == indx

        new_indx, pos = transform_dist(4, table, indx)
        assert pos == 2
        assert new_indx == indx

        new_indx, pos = transform_dist(-10, table, indx)
        assert pos == -10
        assert new_indx == indx

        new_indx, pos = transform_dist(20, table, indx)
        assert pos == 15
        assert new_indx == indx

        table = [[2, 5], [10, 15]]
        indx = 0

        new_indx, pos = transform_dist(5, table, indx)
        assert pos == 9
        assert new_indx == indx

    def test_load_dist_modify(self):
        """Check load_dist_modify."""
        from pipeline_csv.oegiv import File

        table = File.load_dist_modify(self.fixture('unsorted_modifi.csv'))
        assert table[0] == [0, 0]
        assert table[-1] == [4656750, 4665340]

    def test_dist_modify(self):
        """Check dist_modify."""
        from pipeline_csv.oegiv import File
        from pipeline_csv import Error

        fname = self.fixture('infotech.csv')
        csv_file = File.from_file(fname, 1400)

        assert len(csv_file.data) == 30898
        assert csv_file.total_length == 130111900

        mname = self.fixture('dist_modifi.csv')
        table = File.load_dist_modify(mname)
        assert len(table) == 38

        assert int(csv_file.data[0].dist_od) == 0
        assert int(csv_file.data[-1].dist_od) == 130111900

        csv_file.dist_modify(table)

        assert int(csv_file.data[0].dist_od) == 0
        assert int(csv_file.data[-1].dist_od) == 130889155

        from pipeline_csv.csvfile.row import Row

        csv_file.data = [
          Row.as_thick(0, 105),
        ]
        table = [[10, 10], [50, 50]]

        with self.assertRaises(Error) as context:
            csv_file.dist_modify(table)
        assert 'dist 0 < node 10' in str(context.exception)

        csv_file.data = [
          Row.as_thick(20, 105),
        ]
        csv_file.dist_modify(table)
        assert csv_file.data[0].dist_od == 20

        csv_file.data = [
          Row.as_thick(150, 105),
        ]
        csv_file.dist_modify(table)
        assert csv_file.data[0].dist_od == 150

    @staticmethod
    def test_make_distances_unique():
        """Check make_distances_unique function."""
        from pipeline_csv.csvfile import File
        from pipeline_csv.csvfile.row import Row

        csv_file = File(1400)
        dist = 10
        dist_shift_mm = 2

        csv_file.data = [
          Row.as_weld(dist, ''),
          Row.as_weld(dist + 1000, ''),
          Row.as_thick(dist, 100),
        ]
        assert csv_file.data[0].dist_od == dist
        assert csv_file.data[-1].dist_od == dist

        assert csv_file.make_distances_unique(dist_shift_mm=dist_shift_mm) == 1
        assert csv_file.data[0].dist_od == dist
        assert csv_file.data[-1].dist_od == dist + dist_shift_mm

    def test_add_warn(self):
        """Check add_warn method."""
        from pipeline_csv.csvfile import File

        csv_file = File(1400)
        assert csv_file.add_warn('', None) is None
        warns = []
        assert len(csv_file.add_warn('', warns)) == 1
        assert len(warns) == 1

    def test_default_diameter(self):
        """Check File with and without default diameters."""
        from pipeline_csv.csvfile import File

        csv_file = File(1420)
        assert not csv_file.diameters

        csv_file = File()
        assert not csv_file.diameters

    def test_no_diam_reverse(self):
        """Reverse File without diameters change."""
        from pipeline_csv.csvfile import File
        from pipeline_csv.csvfile.row import Row

        csv_file = File()

        dist = 10
        csv_file.data = [
          Row.as_weld(dist, ''),
          Row.as_weld(dist + 1000, ''),
          Row.as_thick(dist, 100),
        ]

        assert not csv_file.diameters
        csv_file.reverse()
        assert not csv_file.diameters

    def test_last_pipe(self):
        """Check File.last_weld method."""
        from pipeline_csv.csvfile import Stream, File

        stream = Stream(diameter=700)
        stream.thick = 100

        csv_file = File(1420)
        pipe = csv_file.last_pipe(stream)
        assert pipe.length == 0
        assert len(pipe.features()) == 0
        assert pipe.thick == 100
        assert pipe.category is None

        from pipeline_csv.oegiv import File as FileIV

        csv_file = FileIV.from_file(self.fixture('1.csv'), 1400)
        stream.thick = 80

        pipe = csv_file.last_pipe(stream)
        assert pipe.length == 0
        assert len(pipe.features()) == 0
        assert pipe.thick == 80
        assert pipe.category is None
