"""Tests totals.py file.

make test T=test_csv/test_statistics/test_totals.py
"""
from . import TestStatistics


def check_tube_property(prop, val, num, length):
    """Check TubeProperty with given val for num and length."""
    assert val in prop.data
    assert prop.data[val].number == num
    assert prop.data[val].length == length


class TestTotals(TestStatistics):
    """File totals.py."""

    def test_property_counter(self):
        """Check Totals class."""
        from pipeline_csv.csvfile.statistics.totals import Totals

        totals = Totals()
        assert not totals.markers
        assert "Tubes:" in str(totals)

        self.tube.length = 100
        totals.add_data(self.tube)

    def test_fill(self):
        """Check Totals.fill method."""
        from pipeline_csv.csvfile.statistics.totals import Totals
        from pipeline_csv import TypeHorWeld

        totals = Totals()
        warns = []
        totals.fill(self.csv_file, warns)

        assert not warns
        assert totals.start == 0
        assert totals.length == 426625
        assert len(totals.markers) == 5

        assert totals.liners.number == 14
        assert len(totals.liners.tubes) == 3
        assert len(totals.liners.data) == 3
        assert totals.liners.tubes_all() == 13

        assert totals.pipes.number == 41
        assert totals.pipes.length == totals.length

        assert totals.pipes.thick.number == totals.pipes.number
        assert totals.pipes.thick.length == totals.length

        prop = totals.pipes.thick
        assert len(prop.data) == 3
        check_tube_property(prop, 70, 22, 232232)  # 7 mm thick: 22 pipes length 232232 mm
        check_tube_property(prop, 90, 6, 63324)
        check_tube_property(prop, 100, 13, 131069)

        prop = totals.pipes.category
        assert len(prop.data) == 3
        check_tube_property(prop, '1', 5, 51980)  # 1 category: 5 pipes length 51980 mm
        check_tube_property(prop, '2', 11, 118773)
        check_tube_property(prop, '3', 25, 255872)

        prop = totals.pipes.types
        assert len(prop.data) == 1
        check_tube_property(prop, TypeHorWeld.HORIZONTAL, totals.pipes.number, totals.length)

        assert totals.defects.number == 75
